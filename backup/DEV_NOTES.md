# Developer Notes — Pneumonia Detection Project

## Interim Status: Complete ✅

---

## What Was Built

Single Jupyter notebook (`pneumonia_detection.ipynb`) covering the full interim pipeline:

```
Prerequisites → Data Overview → EDA → Preprocessing → CNN Training → Evaluation
```

Runs on **Python 3.12 + TensorFlow-macOS 2.16.2** (Apple Silicon M1). Kernel: `Python 3.12 (pneumonia)` in the `venv/` virtualenv.

---

## Environment Gotchas (Learned the Hard Way)

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| `pip install tensorflow` fails | No Python 3.14 wheels exist for TF | Use Python 3.12 via `brew install python@3.12` |
| `libmetal_plugin.dylib` crash | Both `tensorflow` and `tensorflow-macos` installed simultaneously | Uninstall both, reinstall only `tensorflow-macos==2.16.2 + tensorflow-metal==1.2.0` |
| numpy version conflict | TF 2.16 needs `numpy<2.0`; scipy/opencv want `numpy>=2.0` | Pin `numpy>=1.26,<2.0`, `opencv-python==4.9.0.80`, `scipy<1.14` |
| Jupyter cell edits disappearing | Jupyter auto-saves from in-memory state, overwriting external edits | Always **File → Close and Halt** before external edits; reopen to pick up changes |

**Working pinned versions:**
```
tensorflow-macos==2.16.2    tensorflow-metal==1.2.0
numpy>=1.26.0,<2.0.0        opencv-python==4.9.0.80
scipy<1.14                  pydicom>=3.0
```

---

## Data Quirks Discovered

### 1. Zip structure has macOS ghost files
```python
# Wrong — doubles the count to 53,368
files = [f for f in zf.namelist() if f.endswith(".dcm")]

# Correct — 26,684 real files
files = [f for f in zf.namelist()
         if f.endswith(".dcm") and not f.startswith("__MACOSX")]
```

### 2. Files inside zip have a directory prefix
```python
# Wrong — KeyError every time
zf.open(f"{patient_id}.dcm")

# Correct — build a lookup at load time
lookup = {os.path.basename(f).replace(".dcm", ""): f for f in files}
zf.open(lookup[patient_id])
# e.g. opens: stage_2_train_images/0004cfab-....dcm
```

### 3. CSV row count ≠ patient count
- `train_labels.csv` has **30,227 rows** but **26,684 unique patients**
- Pneumonia patients with multiple opacity regions get one row per bounding box
- Always deduplicate on `patientId` before splitting — otherwise the same patient leaks into train + test

```python
patient_df = (
    train_labels[["patientId", "Target"]]
    .drop_duplicates(subset="patientId")
    .merge(class_info.drop_duplicates(subset="patientId"), on="patientId")
)
# Result: 26,684 rows — 6,012 pneumonia (22.5%), not 9,555 (31.6%)
```

### 4. DICOM files need `force=True`
Some files in this dataset lack the standard DICM header. Without `force=True`, pydicom raises `InvalidDicomError` silently swallowed by try/except:
```python
dcm = pydicom.dcmread(path, force=True)  # always
```

### 5. Images are already grayscale
No RGB→grayscale step needed. `dcm.pixel_array` returns a `(H, W)` uint8 array. Just add a channel dim:
```python
img = dcm.pixel_array.astype(np.float32)
img = cv2.resize(img, (128, 128))
img = img / img.max()           # per-image norm → [0, 1]
img = img[..., np.newaxis]      # (128, 128, 1)
```

---

## Model: What Worked, What Didn't

### Architecture (Scratch CNN)
```
Input(128×128×1)
→ [Conv2D(32) → BN → MaxPool] × 3 (filters: 32 → 64 → 128)
→ GlobalAveragePooling2D
→ Dense(256, relu) → Dropout(0.5)
→ Dense(1, sigmoid)
```
~127K parameters. Trained on M1 GPU: ~110s/epoch.

### Results
| | Train | Val | Test |
|-|-------|-----|------|
| Best Epoch | 3 (of 6) | — | — |
| AUC | 0.764 | 0.762 | **0.768** |
| Accuracy | 69% | 77% | 78% |
| Pneumonia Recall | — | — | **0.01** |

**The recall problem:** Model predicts only 13 positives out of 4,003 test samples at threshold=0.5. This is expected behaviour for a class-imbalanced dataset at the default threshold — not a bug. The AUC of 0.77 shows the model *does* rank pneumonia cases higher; the threshold just needs calibrating.

### Class weights used
```python
# sklearn computed:
{0: 0.6454, 1: 2.2192}  # penalises missed pneumonia ~3.4× more
```
Even with these weights, 128×128 resolution loses too much texture to push recall high enough at threshold=0.5.

---

## tf.data Pipeline

```python
def make_dataset(df, shuffle=False):
    ds = tf.data.Dataset.from_tensor_slices(
        (df["patientId"].values, df["Target"].values.astype(np.float32))
    )
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df), seed=42)
    return (ds
        .map(tf_load_wrapper, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(32)
        .prefetch(tf.data.AUTOTUNE))
```

`tf.py_function` wraps the pydicom read. Confirmed output: `(32, 128, 128, 1)` batches, pixel range `[0.0, 1.0]`.

---

## Next Steps — Final Report

### Priority order

#### 1. Threshold calibration (quick win, no retraining)
Load `best_cnn_model.keras`, plot precision-recall curve on val set, pick threshold that gives recall ≥ 0.70 at acceptable precision. This alone may make the scratch CNN usable as a baseline.

#### 2. Transfer learning (main deliverable — 30 pts)
Two models minimum. Suggested order:

```
Model A: EfficientNetB0  (lightest, fastest, best accuracy/param ratio)
Model B: ResNet50        (strong baseline, well-studied)
Optional: VGG16          (heavier, good for comparison)
```

**Input change required:** Resize to **224×224** (ImageNet standard). Update `IMG_SIZE = (224, 224)` and rebuild `tf.data` datasets.

**Freeze strategy:**
```python
base = tf.keras.applications.EfficientNetB0(
    include_top=False, weights="imagenet", input_shape=(224, 224, 3)
)
# Phase 1: freeze all backbone layers, train head only (5–10 epochs)
base.trainable = False

# Phase 2: unfreeze last 20–30 layers, fine-tune with lr=1e-5
for layer in base.layers[-30:]:
    layer.trainable = True
```

**Grayscale → RGB:** Pretrained models expect 3 channels. Replicate the single channel:
```python
img_rgb = tf.image.grayscale_to_rgb(img)  # (224, 224, 1) → (224, 224, 3)
```

#### 3. Custom architectures on pretrained backbones
Add attention or extra dense layers on top:
```python
x = base.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation="relu")(x)
x = BatchNormalization()(x)
x = Dropout(0.4)(x)
out = Dense(1, activation="sigmoid")(x)
```

#### 4. Model comparison table
Build a summary DataFrame across all models:

| Model | Params | AUC | Recall@0.3 | F1 | Train Time |
|-------|--------|-----|------------|-----|-----------|
| CNN Scratch | 127K | 0.768 | TBD | 0.02 | ~11 min |
| EfficientNetB0 | ~5M | — | — | — | — |
| ResNet50 | ~25M | — | — | — | — |

Pick best model based on **recall** (clinical priority) and AUC. Document rationale.

#### 5. Serialization + inference
```python
best_model.save("final_model.keras")
loaded = tf.keras.models.load_model("final_model.keras")
# Run inference on 5 test images, display image + predicted probability
```

#### 6. Streamlit app (skeleton)
```python
# app.py
import streamlit as st
import tensorflow as tf, pydicom, cv2, numpy as np

model = tf.keras.models.load_model("final_model.keras")

uploaded = st.file_uploader("Upload chest X-ray (DICOM or PNG)")
if uploaded:
    # read → preprocess → predict → display
    prob = model.predict(img[np.newaxis])[0][0]
    st.write(f"Pneumonia probability: {prob:.1%}")
    st.write("Positive" if prob > 0.35 else "Negative")
```

```bash
streamlit run app.py
```

#### 7. Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt final_model.keras app.py ./
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

```bash
docker build -t pneumonia-detection .
docker run -p 8501:8501 pneumonia-detection
```

#### 8. Hugging Face Spaces
- Create a Space with Gradio SDK
- Upload `final_model.keras` + `app.py` (use `gr.Interface` instead of Streamlit for HF Spaces)
- Set `requirements.txt` with pinned versions

---

## File Map

```
pneumonia-detection/
├── pneumonia_detection.ipynb   # All interim + final report code
├── best_cnn_model.keras        # Best scratch CNN checkpoint (val_auc=0.762)
├── venv/                       # Python 3.12 virtualenv (not committed)
├── data/
│   ├── stage_2_train_images.zip
│   ├── stage_2_test_images.zip
│   ├── stage_2_train_labels.csv
│   ├── stage_2_detailed_class_info.csv
│   └── train_images/           # Extracted DICOMs (26,684 .dcm files)
├── sample_images_per_class.png
├── class_imbalance.png
├── preprocessing_before_after.png
├── training_history.png
├── evaluation_plots.png
├── CAPSTONE_REPORT.md          # Formal project report
├── DEV_NOTES.md                # This file
└── CLAUDE.md                   # AI assistant context
```

---

## Quick Reference

```bash
# Activate env
source venv/bin/activate

# Launch notebook with correct kernel
jupyter notebook pneumonia_detection.ipynb
# → Kernel → Python 3.12 (pneumonia) → Restart & Run All

# Check what's installed
pip list | grep -E "tensorflow|numpy|keras|cv2|pydicom"

# Verify TF + Metal working
python -c "import tensorflow as tf; print(tf.config.list_physical_devices())"
# Should show: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```
