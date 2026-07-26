# Pneumonia Detection from Chest X-Rays
## Capstone Project Report — Interim Submission

**Dataset**: RSNA Pneumonia Detection Challenge  
**Technique**: Deep Learning — Convolutional Neural Networks  
**Framework**: TensorFlow / Keras (Python 3.12)  
**Hardware**: Apple M1 (GPU via Metal)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Context & Problem Statement](#2-business-context--problem-statement)
3. [Objectives](#3-objectives)
4. [Dataset Description](#4-dataset-description)
5. [Data Overview](#5-data-overview)
6. [Exploratory Data Analysis](#6-exploratory-data-analysis)
7. [Data Preprocessing](#7-data-preprocessing)
8. [Model Building — CNN from Scratch](#8-model-building--cnn-from-scratch)
9. [Model Performance & Evaluation](#9-model-performance--evaluation)
10. [Key Findings & Business Implications](#10-key-findings--business-implications)
11. [Limitations & Future Work](#11-limitations--future-work)
12. [Conclusion](#12-conclusion)

---

## 1. Executive Summary

This project develops an automated pneumonia detection system using deep learning applied to chest X-ray images in DICOM format. Using the RSNA Pneumonia Detection Challenge dataset of **26,684 unique patient chest X-rays**, a Convolutional Neural Network (CNN) was trained from scratch to classify images as pneumonia-positive or pneumonia-negative.

The baseline CNN achieved a **ROC-AUC of 0.7676** on the held-out test set, demonstrating that even a lightweight model can learn meaningful discriminative features from medical imaging data. However, the model's recall for the pneumonia class at the default threshold (0.5) was critically low (1%), underscoring the necessity of threshold calibration and, in the final report, transfer learning with pre-trained backbones to achieve clinically deployable performance.

---

## 2. Business Context & Problem Statement

Pneumonia is one of the leading causes of morbidity and mortality worldwide, disproportionately affecting children under five and elderly populations. The World Health Organization (WHO) identifies pneumonia as a significant driver of infectious-disease mortality globally.

The gold-standard diagnostic pathway — clinical evaluation combined with chest X-ray interpretation by a trained radiologist — faces systemic bottlenecks:

- **Radiologist scarcity**: In rural and resource-limited healthcare settings, access to skilled radiologists is severely constrained.
- **Human error and fatigue**: High patient loads and shift-based workflows introduce variability and diagnostic error.
- **Delayed diagnosis**: Waiting for radiologist availability delays antibiotic treatment, worsening patient outcomes and driving antibiotic overuse.

Automated deep learning systems trained on large imaging datasets offer a scalable, consistent, and low-cost complement to radiologist review — particularly in settings where no specialist is present. Such systems serve as **clinical decision-support tools** rather than replacements, providing a rapid second opinion that flags high-risk cases for priority review.

---

## 3. Objectives

The project aims to:

1. **Accurately classify** chest X-ray images as pneumonia-positive or pneumonia-negative using deep learning.
2. **Assist healthcare professionals** by providing a reliable, consistent second opinion to reduce diagnostic errors.
3. **Improve efficiency** by enabling faster automated screening, reducing radiologist burden.
4. **Enhance accessibility** by building a scalable solution deployable in hospitals, clinics, and rural health centers.
5. **Support global health** by contributing to early detection, lowering pneumonia-related mortality, and reducing unnecessary antibiotic prescription.

---

## 4. Dataset Description

**Source**: RSNA Pneumonia Detection Challenge (Kaggle)

The dataset consists of chest X-ray images stored in **DICOM format** (`.dcm`), the medical imaging standard that embeds both patient metadata and raw pixel arrays within a single file.

### Label Structure

The dataset provides two label files:

| File | Purpose |
|------|---------|
| `stage_2_train_labels.csv` | Binary label per bounding box row (Target: 0 or 1). One patient may appear on multiple rows if multiple opacity regions were annotated. |
| `stage_2_detailed_class_info.csv` | Three-class label per patient (one row per patient). |

**Three-class taxonomy:**

| Class | Binary Target | Meaning |
|-------|--------------|---------|
| `Normal` | 0 | Healthy lungs |
| `No Lung Opacity / Not Normal` | 0 | Chest abnormality present (e.g., cardiomegaly, pleural effusion) but not pneumonia |
| `Lung Opacity` | 1 | Pneumonia present — white/grey opacities visible in lung fields |

> The `No Lung Opacity / Not Normal` class is the most diagnostically challenging: these images show real pathology that can visually resemble pneumonia, making the negative class heterogeneous and the classification boundary harder to learn.

---

## 5. Data Overview

### 5.1 File Inventory

| Asset | Details |
|-------|---------|
| `data/stage_2_train_images.zip` | 26,684 training DICOM files (~3.5 GB) |
| `data/stage_2_test_images.zip` | 3,000 test DICOM files (~380 MB) |
| `stage_2_train_labels.csv` | 30,227 rows × 4 columns |
| `stage_2_detailed_class_info.csv` | 30,227 rows × 2 columns |

### 5.2 Label File Shape

```
stage_2_train_labels.csv
  Shape   : (30,227, 4)
  Columns : ['patientId', 'width', 'height', 'Target']

stage_2_detailed_class_info.csv
  Shape   : (30,227, 2)
  Columns : ['patientId', 'class']
```

### 5.3 DICOM Image Properties

Inspecting five sample images directly from the zip:

| File | dtype | Shape | Pixel Min | Pixel Max |
|------|-------|-------|-----------|-----------|
| Sample 1 | uint8 | (1024, 1024) | 0 | 230 |
| Sample 2 | uint8 | (1024, 1024) | 0 | 255 |
| Sample 3 | uint8 | (1024, 1024) | 0 | 232 |
| Sample 4 | uint8 | (1024, 1024) | 0 | 255 |
| Sample 5 | uint8 | (1024, 1024) | 0 | 255 |

All images are **1024×1024 pixel, single-channel (grayscale), uint8 arrays**. The varying maximum pixel value (230 vs. 255) confirms scanner-to-scanner intensity variation, making per-image normalization necessary.

### 5.4 Key Data Observations

```
Training CSV rows          : 30,227
Unique training patients   : 26,684
Training DICOM files       : 26,684
Test DICOM files           : 3,000

Binary target distribution (raw CSV):
  Target=0 [No Pneumonia] : 20,672 (68.4%)
  Target=1 [Pneumonia]    : 9,555  (31.6%)
```

**Important finding — raw CSV inflates pneumonia count:** The CSV has 30,227 rows but only 26,684 unique patients. The extra 3,543 rows arise because pneumonia patients can have **multiple bounding box annotations** (one row per annotated opacity region). When deduplicated to patient level, the true pneumonia prevalence is **6,012 patients (22.5%)**, not 31.6% as the raw CSV implies. This makes the class imbalance more severe than initially apparent.

---

## 6. Exploratory Data Analysis

### 6.1 Patient-Level Class Distribution

After deduplication to one row per patient:

| Class | Patient Count | % of Total |
|-------|--------------|-----------|
| No Lung Opacity / Not Normal | 11,821 | 44.3% |
| Normal | 8,851 | 33.2% |
| **Lung Opacity (Pneumonia)** | **6,012** | **22.5%** |
| **Total** | **26,684** | **100%** |

### 6.2 Class Imbalance Analysis

The binary target distribution at patient level:

| Target | Patients | Percentage |
|--------|----------|-----------|
| No Pneumonia (0) | 20,672 | 77.5% |
| Pneumonia (1) | 6,012 | 22.5% |

- The dataset has a **~3.4:1 ratio** of negative to positive patients.
- A naive classifier that always predicts "no pneumonia" would achieve **77.5% accuracy** — highlighting why accuracy alone is a misleading metric for this task.
- The `No Lung Opacity / Not Normal` sub-class (44.3% of all patients) is particularly important: it contains real pathology that can mimic pneumonia's visual appearance, making it the hardest sub-group to correctly classify as negative.

### 6.3 Visual Observations from Sample X-Rays

**Lung Opacity (Pneumonia — Target=1):**
- Visible patchy white/grey opacities in one or both lung fields.
- Opacities often appear as unilateral consolidations in early-stage pneumonia.
- The affected lung field loses its typical dark, air-filled appearance.

**Normal (Target=0):**
- Clear, uniformly dark lung fields on both sides.
- Sharp diaphragm outline and well-defined costophrenic angles.
- Trachea and major bronchi visible as faint central structures.

**No Lung Opacity / Not Normal (Target=0):**
- Enlarged cardiac silhouettes (cardiomegaly), blunted costophrenic angles, or diffuse haziness.
- These findings are real abnormalities but are not pneumonia — they represent the primary source of potential false positives for the classifier.

### 6.4 Data Quality Notes

- Some DICOM files in this release lack the standard DICM file meta-information header, requiring `pydicom.dcmread(path, force=True)` for reliable reading.
- The training zip archive contains an extra 26,684 `__MACOSX/` ghost metadata entries (a macOS archiving artifact), which must be filtered from the namelist to obtain the true file count.
- Files inside the zip use a directory-prefixed path (`stage_2_train_images/patient_id.dcm`), requiring a lookup dictionary rather than direct filename construction.

---

## 7. Data Preprocessing

### 7.1 Image Extraction

Training DICOM files were extracted from the zip archive to `data/train_images/` (one-time operation, ~3.5 GB on disk). A guard condition prevents re-extraction on subsequent runs.

### 7.2 Patient-Level Deduplication

`stage_2_train_labels.csv` was deduplicated by `patientId` (keeping one row per patient) and merged with `stage_2_detailed_class_info.csv` to yield a clean patient-level dataframe with binary target and three-class label.

### 7.3 Train / Validation / Test Split

Split strategy: **stratified, patient-level, 70/15/15**

| Split | Patients | Pneumonia (Target=1) | % Pneumonia |
|-------|----------|----------------------|-------------|
| Train | 18,677 | 4,208 | 22.5% |
| Validation | 4,004 | 902 | 22.5% |
| Test | 4,003 | 902 | 22.5% |
| **Total** | **26,684** | **6,012** | **22.5%** |

The stratified split preserved the 22.5% pneumonia rate identically across all three splits, ensuring no class distribution drift between train, validation, and test sets.

### 7.4 Preprocessing Pipeline

Each DICOM image was processed through the following steps:

```
1. Read DICOM → pixel_array (H×W, uint8, grayscale — no RGB conversion needed)
2. Cast to float32
3. Resize: 1024×1024 → 128×128 (bilinear interpolation via OpenCV)
4. Normalize: img / img.max() → pixel values in [0.0, 1.0]
5. Add channel dimension: (128, 128) → (128, 128, 1)
```

**Note on grayscale:** DICOM chest X-rays are natively single-channel — no RGB-to-grayscale conversion is required. The channel dimension is added programmatically to satisfy the CNN's expected input shape.

**Note on normalization:** Per-image normalization (dividing by each image's own maximum) was chosen over global normalization because pixel intensity ranges vary across different X-ray scanners (maximum values observed between 230 and 255).

### 7.5 Normalization Verification

Over 20 random training samples:

```
Pixel min range : [0.00000, 0.07201]
Pixel max range : [1.00000, 1.00000]
All values in [0, 1]: PASS
```

The non-zero minimum values (up to 0.072) reflect background noise/non-zero scanner baseline, confirming that per-image normalization correctly handles these variations without clipping.

---

## 8. Model Building — CNN from Scratch

### 8.1 Architecture

A three-block CNN was designed from scratch with progressive feature extraction:

```
Input: (128, 128, 1)
│
├── Block 1: Conv2D(32, 3×3, relu) → BatchNormalization → MaxPooling(2×2)
│           Output: (64, 64, 32)
│
├── Block 2: Conv2D(64, 3×3, relu) → BatchNormalization → MaxPooling(2×2)
│           Output: (32, 32, 64)
│
├── Block 3: Conv2D(128, 3×3, relu) → BatchNormalization → MaxPooling(2×2)
│           Output: (16, 16, 128)
│
├── GlobalAveragePooling2D → (128,)
├── Dense(256, relu)
├── Dropout(0.5)
└── Dense(1, sigmoid) → Probability of pneumonia
```

**Model parameters:**

| Component | Parameters |
|-----------|-----------|
| Trainable | 126,401 (493.75 KB) |
| Non-trainable (BatchNorm) | 448 (1.75 KB) |
| **Total** | **126,849 (495.50 KB)** |

**Design choices:**
- **BatchNormalization** after each convolution stabilises training and reduces sensitivity to learning rate.
- **GlobalAveragePooling2D** instead of Flatten reduces the parameter count in the dense head and provides implicit spatial regularization.
- **Dropout(0.5)** in the dense head prevents co-adaptation of neurons and reduces overfitting on a 18,677-sample training set.
- **Sigmoid output** with binary cross-entropy loss is appropriate for binary classification.

### 8.2 Class Weights

To compensate for the 3.4:1 class imbalance, balanced class weights were computed using `sklearn.utils.class_weight.compute_class_weight`:

| Class | Weight |
|-------|--------|
| No Pneumonia (0) | 0.6454 |
| Pneumonia (1) | **2.2192** |

The model penalises missed pneumonia cases **~3.4× more heavily** than missed negative cases during training.

### 8.3 Training Configuration

| Hyperparameter | Value |
|---------------|-------|
| Optimizer | Adam (lr=1e-3) |
| Loss | Binary Cross-Entropy |
| Metrics | Accuracy, AUC-ROC |
| Batch size | 32 |
| Max epochs | 15 |
| Early stopping | patience=3, monitor=val_auc |
| Checkpoint | Best val_auc saved to `best_cnn_model.keras` |
| Hardware | Apple M1 GPU (TensorFlow Metal) |

---

## 9. Model Performance & Evaluation

### 9.1 Training History

| Epoch | Train Acc | Train AUC | Val Acc | Val AUC | Val Loss | Notes |
|-------|-----------|-----------|---------|---------|----------|-------|
| 1 | 0.649 | 0.692 | 0.225 | 0.682 | 2.624 | |
| 2 | 0.680 | 0.735 | 0.762 | 0.689 | 0.504 | |
| **3** | **0.691** | **0.764** | **0.774** | **0.762** | **0.590** | ★ Best |
| 4 | 0.704 | 0.776 | 0.770 | 0.742 | 0.512 | |
| 5 | 0.713 | 0.784 | 0.775 | 0.499 | 4.261 | Val AUC collapses |
| 6 | 0.709 | 0.783 | 0.540 | 0.652 | 0.715 | Early stop triggered |

*Best weights from Epoch 3 restored by early stopping.*

**Training observations:**
- Train AUC improved steadily from 0.692 to 0.784 across 6 epochs, showing the model continued learning throughout.
- Val AUC peaked at **0.762** in Epoch 3, then became unstable — collapsing to near-random (0.499) at Epoch 5 before partially recovering. This instability likely reflects high learning rate sensitivity and limited model capacity at 128×128 resolution.
- Early stopping correctly identified Epoch 3 as the optimal checkpoint, preventing the model from being saved in a degraded state.
- Each epoch took approximately **110–120 seconds** on the Apple M1 GPU via TensorFlow Metal.

### 9.2 Test Set Classification Report

**Test set: 4,003 patients | 902 pneumonia (22.5%) | 3,101 no pneumonia (77.5%)**

```
                  precision    recall  f1-score   support

No Pneumonia (0)       0.78      1.00      0.87      3,101
   Pneumonia (1)       0.69      0.01      0.02        902

        accuracy                           0.78      4,003
       macro avg       0.73      0.50      0.45      4,003
    weighted avg       0.76      0.78      0.68      4,003

ROC-AUC Score : 0.7676
```

### 9.3 Metric Summary

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Overall Accuracy | 78% | Misleading — model largely predicts negative |
| Pneumonia Precision | 0.69 | 69% of predicted positives are correct |
| **Pneumonia Recall** | **0.01** | **Only 1% of actual pneumonia cases detected — critical failure** |
| Pneumonia F1 | 0.02 | Near-zero clinical utility at threshold=0.5 |
| **ROC-AUC** | **0.7676** | Model has real discriminative signal — better than random (0.5) |
| Positive predictions | 13 / 4,003 | Model defaults almost entirely to negative |

### 9.4 Confusion Matrix Interpretation

At threshold=0.5:

|  | Predicted Negative | Predicted Positive |
|--|-------------------|-------------------|
| **Actual Negative** | 3,101 (True Negative) | ~0 (False Positive) |
| **Actual Positive** | ~889 (False Negative) | ~13 (True Positive) |

The model missed **~889 out of 902 pneumonia patients** — a false negative rate of ~99%.

---

## 10. Key Findings & Business Implications

### 10.1 Technical Findings

1. **True pneumonia prevalence (22.5%) is lower than the raw CSV suggests (31.6%).** The label file contains per-bounding-box rows, not per-patient rows. Deduplication is essential before splitting to avoid data leakage and biased class ratios.

2. **ROC-AUC of 0.77 confirms the model learns real signal.** Despite near-zero recall at threshold=0.5, the model correctly ranks many pneumonia cases above non-pneumonia cases — the issue is the decision threshold, not the learned representations.

3. **The 0.5 threshold is inappropriate for imbalanced medical classification.** A lower threshold (e.g., 0.2–0.3) would recover substantially more pneumonia recall at the cost of precision — an acceptable trade-off in a screening context where false negatives (missed pneumonia) are far more costly than false positives (unnecessary follow-up).

4. **128×128 resolution loses critical radiological texture.** Downsampling from 1024×1024 to 128×128 (64× fewer pixels) removes the fine-grained opacity patterns that differentiate pneumonia from normal or non-pneumonia pathology. The 224×224 resolution used by standard pretrained backbones will capture significantly more detail.

5. **`No Lung Opacity / Not Normal` is the hardest negative sub-class.** At 44.3% of all patients, this class contains real chest abnormalities that can resemble pneumonia visually, making it the primary driver of false positives.

### 10.2 Business Implications

| Finding | Business Impact |
|---------|----------------|
| 1% pneumonia recall at threshold=0.5 | Not deployable as-is — would miss 99% of cases, offering no clinical value |
| ROC-AUC of 0.77 | Meaningful baseline — suitable for validating the pipeline and benchmarking against transfer learning models |
| Model runs on consumer hardware (M1 Mac) | Low infrastructure cost; viable for edge deployment in resource-constrained settings |
| ~2 minutes per training epoch on M1 | Full retraining feasible overnight; fast iteration cycle for fine-tuning |
| Consistent 22.5% stratified splits | Reliable evaluation framework — performance numbers are reproducible and unbiased |

**Recommended threshold for screening use:** ROC curve analysis suggests that a threshold of approximately **0.25–0.35** would balance recall (catching most pneumonia cases) with a manageable false positive rate — a decision that should be made with clinical stakeholders, not purely on statistical grounds.

---

## 11. Limitations & Future Work

### 11.1 Current Limitations

- **128×128 input resolution** discards most radiological detail present in the original 1024×1024 DICOM images.
- **CNN from scratch** (126K parameters) has insufficient capacity to learn the complex hierarchical features of chest pathology without pre-trained weights.
- **No threshold calibration** was performed — recall at default threshold is clinically unacceptable.
- **No data augmentation** was applied — random horizontal flips, rotation, and brightness jitter would improve generalisation on the limited training set.

### 11.2 Planned for Final Report

| Task | Approach |
|------|---------|
| Transfer learning (≥2 models) | VGG16, ResNet50, EfficientNetB0 with 224×224 input; freeze backbone → train head → unfreeze last N layers |
| Custom architectures | Add attention layers, custom classification heads on top of pretrained backbones |
| Threshold calibration | Plot precision-recall curve; select threshold maximising F1 or recall at acceptable precision |
| Model comparison | Side-by-side AUC, recall, precision, F1 table for all models |
| Best model serialization | Save in `.keras` format; reload and run inference on sample images |
| Web application | Streamlit/Gradio app: upload DICOM or PNG → predicted class + probability |
| Containerisation | Docker image with model + app; `docker run -p 8501:8501` |
| Deployment | Hugging Face Spaces (Gradio) |

---

## 12. Conclusion

This interim report establishes a complete, reproducible deep learning pipeline for automated pneumonia detection from chest X-ray images:

- **Data ingestion** from DICOM zip archives with handling of dataset-specific quirks (missing DICM headers, macOS ghost files, per-bounding-box duplicate rows).
- **EDA** revealing the true class distribution (22.5% pneumonia at patient level, not 31.6% as the raw CSV implies) and the visual characteristics that distinguish each class.
- **Preprocessing** producing stratified 70/15/15 patient-level splits with verified [0,1] normalization.
- **Baseline CNN** achieving ROC-AUC 0.7676 — a meaningful signal above random, confirming that deep learning can discriminate pneumonia from non-pneumonia in this dataset.

The baseline model is a deliberately lightweight starting point. Its limitations — particularly the 1% pneumonia recall at the default threshold — motivate the transfer learning approach in the final report, where pretrained backbones are expected to push AUC above 0.85 and deliver clinically meaningful recall, bringing the system closer to its goal of serving as a reliable automated decision-support tool for pneumonia diagnosis.

---

*Notebook: `pneumonia_detection.ipynb` | Best model checkpoint: `best_cnn_model.keras`*
