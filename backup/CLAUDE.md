# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pneumonia detection from chest X-ray images (DICOM format) using the RSNA Pneumonia Detection Challenge dataset. Binary classification: pneumonia-positive (Target=1) vs. pneumonia-negative (Target=0).

Three-class source labels (in `stage_2_detailed_class_info.csv`):
- `Normal` → Target=0
- `No Lung Opacity / Not Normal` → Target=0 (abnormal but not pneumonia — hardest class to separate)
- `Lung Opacity` → Target=1

All work lives in `pneumonia_detection.ipynb`. The project is phased: interim report (Sections 1–4) is complete; final report (transfer learning, deployment) is pending.

## Environment Setup

**Python 3.12 is required.** TensorFlow does not support Python 3.14 (the macOS system default). This project uses a local `venv`:

```bash
# First-time setup (Apple Silicon Mac)
brew install python@3.12
cd /Users/vsrdhoolla/learnings/pneumonia-detection
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv venv
source venv/bin/activate
pip install tensorflow-macos==2.16.2 tensorflow-metal==1.2.0
pip install "numpy>=1.26.0,<2.0.0" pydicom opencv-python==4.9.0.80
pip install pandas matplotlib seaborn "scikit-learn" "scipy<1.14" jupyter ipykernel
python -m ipykernel install --user --name=pneumonia-venv --display-name "Python 3.12 (pneumonia)"

# Every session
source venv/bin/activate

# Launch notebook
jupyter notebook pneumonia_detection.ipynb
# Then: Kernel → Change Kernel → "Python 3.12 (pneumonia)"
```

**Do not install the standard `tensorflow` package on this machine — it conflicts with `tensorflow-metal`.** Only `tensorflow-macos` + `tensorflow-metal` should be present.

## Data Facts (from actual execution)

| Item | Value |
|------|-------|
| `stage_2_train_labels.csv` rows | 30,227 (not unique — some patients have multiple bounding box rows) |
| Unique training patients | 26,684 |
| Pneumonia-positive patients | 6,012 (22.5%) — not 9,555; duplicates inflate raw CSV count |
| Training DICOM files | 26,684 |
| Test DICOM files | 3,000 |
| Image shape | 1024×1024, dtype=uint8, range [0, 255] |

**The zip contains `__MACOSX/` ghost metadata files** (macOS artifact), doubling the namelist count to 53,368. Always filter them out:
```python
files = [f for f in zf.namelist() if f.endswith(".dcm") and not f.startswith("__MACOSX")]
```

Files inside the zip are stored with a directory prefix: `stage_2_train_images/patient_id.dcm`. Build a lookup dict before reading:
```python
zip_lookup = {os.path.basename(f).replace(".dcm", ""): f for f in files}
# Then: zf.open(zip_lookup[patient_id])
```

## DICOM Reading

Always use `force=True` — many files in this dataset lack the standard DICM header:
```python
dcm = pydicom.dcmread(path, force=True)
img = dcm.pixel_array  # already 2D grayscale (H, W) — no RGB conversion needed
```

DICOM images are natively grayscale. Add a channel dimension for model input: `img[..., np.newaxis]` → shape `(H, W, 1)`.

## Notebook Structure

All sections are sequential and share state. Run top-to-bottom from a fresh kernel.

| Section | What it does |
|---------|-------------|
| Prerequisites | `pip install` cell with pinned versions |
| 1: Data Overview | Load CSVs, count DICOM files, inspect pixel shapes |
| 2: EDA | Patient-level dedup (`patient_df`), sample image grid, class imbalance charts |
| 3: Preprocessing | Extract zip → `data/train_images/`, stratified 70/15/15 split, `load_and_preprocess()` |
| 4: Model Building | `tf.data` pipeline, CNN from scratch, training with class weights, evaluation |

**Key variable dependencies:**
- `train_zip_lookup` (built in 1.3) is required by Section 2 image plots
- `patient_df` (built in 2.1) is required by Section 3 split
- `df_train`, `df_val`, `df_test` (built in 3.2) are required by Section 4
- Extracted images in `data/train_images/` are required by Section 3+ (one-time, ~3.5 GB)

## Preprocessing Decisions

- **Resize to 128×128** for the scratch CNN baseline (speed). Use 224×224 for pretrained backbones in the final report.
- **Per-image normalization**: `img / img.max()` → [0, 1]. Not global normalization, because pixel ranges vary by scanner (some max at 230, others at 255).
- **Stratified split at patient level** (not row level) to prevent the same patient appearing in both train and test.
- **Class weights**: `{0: 0.6454, 1: 2.2192}` — computed via `sklearn.utils.class_weight.compute_class_weight("balanced")`.

## Baseline CNN Results (Section 4)

- **Architecture**: 3× (Conv2D→BatchNorm→MaxPool) → GlobalAvgPool → Dense(256) → Dropout(0.5) → Sigmoid. Total: 126,849 params.
- **Best epoch**: 3 (of 6 before early stopping). Val AUC: 0.762.
- **Test AUC: 0.7676**. Pneumonia recall: 0.01 (only 13/902 positives detected at threshold=0.5).
- **Root cause of low recall**: At threshold=0.5 the model defaults to negative. AUC of 0.77 shows discriminative signal exists — a lower threshold (0.2–0.3) would recover recall at the cost of precision.
- **Saved model**: `best_cnn_model.keras` (best val_auc checkpoint).

## Final Report Roadmap

- Transfer learning: VGG16, ResNet50, EfficientNetB0 with 224×224 input
- Freeze backbone → train head → unfreeze last N layers for fine-tuning
- Compare all models by AUC-ROC and pneumonia recall
- Serialize best model, deploy via Streamlit/Gradio app
- Package with Docker; deploy to Hugging Face Spaces
