"""Generate the Pneumonia Detection Interim BUSINESS Report PDF.

Structured per the business-report guidelines: every section explains
What we did / Why we did it / What we observed / What we concluded.
No source code — outputs, visualizations, observations, and rationale only.
All numbers are taken from the executed src/pneumonia_interim.ipynb.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "src")
OUT  = os.path.join(ROOT, "Pneumonia_Detection_Interim_Business_Report.pdf")

# ---------------------------------------------------------------------------
# Styles (project report template)
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle", parent=styles["Title"], fontSize=22, leading=28,
    textColor=colors.HexColor("#1a3a5c"), spaceAfter=6, alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"], fontSize=13, leading=18,
    textColor=colors.HexColor("#2c5f8a"), spaceAfter=4, alignment=TA_CENTER,
)
meta_style = ParagraphStyle(
    "Meta", parent=styles["Normal"], fontSize=10, leading=14,
    textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=2,
)
h1_style = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontSize=14, leading=18,
    textColor=colors.HexColor("#1a3a5c"), spaceBefore=18, spaceAfter=6,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=11.5, leading=15,
    textColor=colors.HexColor("#2c5f8a"), spaceBefore=10, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"], fontSize=10, leading=15,
    textColor=colors.HexColor("#222222"), spaceAfter=6, alignment=TA_JUSTIFY,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style, leftIndent=18, bulletIndent=6, spaceAfter=3,
)
code_style = ParagraphStyle(
    "Code", parent=styles["Code"], fontSize=8, leading=12,
    backColor=colors.HexColor("#f5f5f5"), leftIndent=12, rightIndent=12,
    spaceBefore=4, spaceAfter=4, textColor=colors.HexColor("#333333"),
)
caption_style = ParagraphStyle(
    "Caption", parent=styles["Normal"], fontSize=9, leading=12,
    textColor=colors.HexColor("#555555"), alignment=TA_CENTER,
    spaceAfter=8, spaceBefore=2,
)

PAGE_W, PAGE_H = A4
MARGIN = 1.2 * cm
CONTENT_W = PAGE_W - 2 * MARGIN

TBLSTYLE_BASE = TableStyle([
    ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
    ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",     (0, 0), (-1, 0), 9),
    ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",     (0, 1), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#edf3fa")]),
    ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
    ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
    ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",   (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ("LEFTPADDING",  (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
])

def tbl(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TBLSTYLE_BASE)
    return t

def img(filename, width=None):
    path = os.path.join(SRC, filename)
    if not os.path.exists(path):
        return Spacer(1, 0)
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    width = width or 5 * inch
    return Image(path, width=width, height=width * h / w)

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"),
                      spaceAfter=4, spaceBefore=4)

def para(text, style=None):
    return Paragraph(text, style or body_style)

def section(number, title):
    return [rule(), Paragraph(f"{number}. {title}", h1_style)]

def guideline(label):
    """The What/Why/Observed/Conclusions sub-headers required by the guidelines."""
    return Paragraph(label, h2_style)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#1a3a5c"))
    canvas.rect(0, PAGE_H - 1.0 * cm, PAGE_W, 1.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H - 0.65 * cm,
                      "Pneumonia Detection — Interim Business Report")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.65 * cm, "RSNA Challenge | 2026")
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 0.6 * cm, "Confidential | For Academic Use Only")
    canvas.drawRightString(PAGE_W - MARGIN, 0.6 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.4 * cm, bottomMargin=1.2 * cm,
    )
    story = []

    # ── Cover ────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 1.8 * cm),
        Paragraph("Pneumonia Detection from Chest X-Rays", title_style),
        Paragraph("Interim Business Report", subtitle_style),
        Spacer(1, 0.3 * cm),
        rule(),
        Spacer(1, 0.2 * cm),
        Paragraph("RSNA Pneumonia Detection Challenge", meta_style),
        Paragraph("Deep Learning · Convolutional Neural Networks · TensorFlow / Keras", meta_style),
        Paragraph("Apple M1 GPU (TensorFlow Metal) · Python 3.12", meta_style),
        Spacer(1, 0.3 * cm),
        rule(),
        Spacer(1, 0.5 * cm),
    ]

    meta_data = [
        ["Dataset", "RSNA Pneumonia Detection Challenge (Kaggle)"],
        ["Total Patients", "26,684 unique chest X-rays (DICOM format)"],
        ["Framework", "TensorFlow 2.16 / Keras — Apple M1 GPU"],
        ["Baseline Result", "Scratch CNN — Test ROC-AUC 0.8353, pneumonia recall 0.84"],
        ["Submission Type", "Interim Business Report"],
        ["Date", "July 2026"],
        ["Companion Notebook", "src/pneumonia_interim.ipynb (all outputs reproduced here)"],
    ]
    mt = Table(meta_data, colWidths=[3.8 * cm, CONTENT_W - 3.8 * cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), colors.HexColor("#edf3fa")),
        ("FONTNAME",     (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",     (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 10),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story += [mt, Spacer(1, 0.4 * cm)]

    story += [Paragraph("Interim Evaluation Rubric — Coverage Map", h2_style)]
    rubric = [
        ["Rubric Section", "Points", "Covered In"],
        ["Data Overview — import data, check shape", "6", "Section 3"],
        ["EDA — samples per class, imbalance, observations", "8", "Section 4"],
        ["Preprocessing — grayscale, before/after, split, normalization", "10", "Section 5"],
        ["Model Building — CNN from scratch, training, performance", "10", "Section 6"],
        ["Business Report Quality", "6", "Whole document"],
        ["Total", "40", ""],
    ]
    rt = Table(rubric, colWidths=[CONTENT_W - 5.4 * cm, 1.8 * cm, 3.6 * cm], repeatRows=1)
    rt.setStyle(TBLSTYLE_BASE)
    story += [rt, Spacer(1, 0.3 * cm)]
    story += [
        para(
            "<i>Per the business-report guidelines, every section below is organised into four "
            "parts: <b>What we did</b>, <b>Why we did it</b>, <b>What we observed</b>, and "
            "<b>What we concluded</b>. No source code is included — key outputs are reproduced "
            "as captured results and figures from the companion notebook.</i>"
        ),
        PageBreak(),
    ]

    # ── 1. Executive Summary ─────────────────────────────────────────────────
    story += section("1", "Executive Summary")
    story += [
        para(
            "This interim report covers the first phase of building an automated pneumonia "
            "detection system from chest X-rays: data understanding, exploratory analysis, "
            "preprocessing, and a convolutional neural network (CNN) trained from scratch as a "
            "baseline."
        ),
        para(
            "Working from <b>26,684 DICOM chest X-rays</b> (RSNA Pneumonia Detection Challenge), "
            "we established that true pneumonia prevalence is <b>22.5%</b> — not the 31.6% the "
            "raw label file suggests — built leakage-safe stratified splits, and trained a "
            "126,849-parameter CNN with class weighting. The baseline achieved "
            "<b>Test ROC-AUC 0.8353</b> and, importantly for a screening tool, "
            "<b>84% pneumonia recall</b> at the default decision threshold — the class-weighted "
            "loss shifted the model toward the clinically safer operating point."
        ),
        para(
            "These results validate the full pipeline and set a strong baseline for the final "
            "phase, where transfer learning with pretrained backbones, threshold governance, and "
            "deployment as a web application will complete the system."
        ),
    ]

    # ── 2. Business Context ──────────────────────────────────────────────────
    story += section("2", "Business Context &amp; Objectives")
    story += [
        para(
            "Pneumonia is a leading cause of death worldwide, disproportionately affecting "
            "children under five and the elderly. Diagnosis relies on chest X-ray interpretation "
            "by radiologists — a scarce resource, particularly in rural and resource-constrained "
            "settings. Fatigue and high patient loads introduce diagnostic variability; delayed "
            "reads delay antibiotic treatment."
        ),
        para(
            "<b>The business goal</b> is a decision-support system that automatically flags "
            "likely pneumonia cases for priority radiologist review — increasing throughput and "
            "consistency without removing the clinician from the loop. For such a screening "
            "tool, <b>missing a pneumonia case (false negative) is far costlier than a false "
            "alarm</b>; this asymmetry drives every modelling decision in this report."
        ),
    ]

    # ── 3. Data Overview ─────────────────────────────────────────────────────
    story += [PageBreak()] + section("3", "Data Overview")

    story += [guideline("3.1 What we did")]
    story += [
        para(
            "We imported the three data sources, checked their shapes, and audited the "
            "relationship between label rows, patients, and image files:"
        ),
        Paragraph("=== stage_2_train_labels.csv ===        Shape: (30,227 rows × 4 columns)", code_style),
        Paragraph("=== stage_2_detailed_class_info.csv === Shape: (30,227 rows × 2 columns)", code_style),
        Paragraph("=== stage_2_train_images.zip ===        26,684 DICOM files (~3.5 GB)", code_style),
    ]

    story += [guideline("3.2 Why we did it")]
    story += [
        para(
            "Every downstream number — class balance, split sizes, evaluation metrics — depends "
            "on knowing exactly what one 'sample' is. A mismatch between 30,227 label rows and "
            "26,684 image files signals duplication that must be resolved before any analysis, "
            "or prevalence statistics and train/test splits would be silently wrong."
        ),
    ]

    story += [guideline("3.3 What we observed")]
    obs = [
        ["Metric", "Value"],
        ["Label CSV rows", "30,227"],
        ["Unique patients / DICOM files", "26,684"],
        ["Duplicate rows (multi-box pneumonia patients)", "3,543"],
        ["Pneumonia patients after deduplication", "6,012  (22.5%)"],
        ["Raw-CSV pneumonia share (misleading)", "31.6%"],
        ["Image properties", "1024×1024, uint8, single-channel grayscale"],
        ["Pixel maxima across samples", "230–255 (scanner-dependent)"],
    ]
    story += [tbl(obs, [9.0 * cm, CONTENT_W - 9.0 * cm]), Spacer(1, 4)]
    story += [
        para(
            "Pneumonia-positive patients appear on one row per annotated opacity region, so the "
            "raw CSV overstates pneumonia prevalence. Images are natively grayscale (X-ray "
            "physics — no colour information exists), and maximum pixel intensity varies by "
            "scanner."
        ),
    ]

    story += [guideline("3.4 What we concluded")]
    story += [
        Paragraph("• All analysis must happen at <b>patient level</b> — labels deduplicated to "
                  "one row per patient before any split or statistic.", bullet_style),
        Paragraph("• True class imbalance is <b>3.44 : 1</b>, more severe than the raw file "
                  "implies — accuracy alone cannot be the success metric.", bullet_style),
        Paragraph("• Scanner-dependent intensity ranges require <b>per-image normalization</b> "
                  "rather than a single global scale.", bullet_style),
        Paragraph("• No RGB-to-grayscale conversion is needed; a channel dimension is added "
                  "programmatically for the CNN.", bullet_style),
    ]

    # ── 4. EDA ───────────────────────────────────────────────────────────────
    story += [PageBreak()] + section("4", "Exploratory Data Analysis")

    story += [guideline("4.1 What we did")]
    story += [
        para(
            "We visualised random X-rays from each of the three source classes, quantified the "
            "class distribution at patient level, and compared pixel-intensity statistics across "
            "classes (100 sampled patients per class)."
        ),
    ]

    story += [guideline("4.2 Why we did it")]
    story += [
        para(
            "Before modelling, we need evidence that (a) the classes are visually "
            "distinguishable — otherwise no classifier can succeed; (b) the imbalance is "
            "quantified — it dictates loss weighting and metric choice; and (c) simple global "
            "statistics carry signal — a sanity check that the task is learnable from pixels."
        ),
    ]

    story += [guideline("4.3 What we observed")]
    dist = [
        ["Class", "Patients", "% of Total"],
        ["No Lung Opacity / Not Normal", "11,821", "44.3%"],
        ["Normal", "8,851", "33.2%"],
        ["Lung Opacity (Pneumonia)", "6,012", "22.5%"],
    ]
    story += [tbl(dist), Spacer(1, 6)]
    story += [
        img("sample_images_per_class.png", width=CONTENT_W),
        Paragraph("Figure 1 — Random samples per class. Normal: dark, air-filled lung fields "
                  "with sharp costophrenic angles. Not Normal: real pathology (cardiomegaly, "
                  "effusions) without pneumonia. Lung Opacity: focal white opacities in lung "
                  "fields.", caption_style),
        img("class_imbalance.png", width=CONTENT_W * 0.8),
        Paragraph("Figure 2 — Class distribution: binary imbalance is 77.5% vs 22.5% (3.44:1). "
                  "A trivial always-negative classifier would score 77.5% accuracy while "
                  "detecting zero pneumonia.", caption_style),
        img("pixel_statistics_per_class.png", width=CONTENT_W * 0.9),
        Paragraph("Figure 3 — Mean pixel intensity by class: pneumonia images are measurably "
                  "brighter (opacities raise mean intensity); the 'Not Normal' class sits "
                  "between Normal and pneumonia.", caption_style),
    ]

    story += [guideline("4.4 What we concluded")]
    story += [
        Paragraph("• Visual signatures exist and align with radiology: the task is learnable "
                  "from pixels alone.", bullet_style),
        Paragraph("• The largest class (44.3%) is 'Not Normal' — pathology that mimics pneumonia "
                  "— so false positives will concentrate there; the negative class is "
                  "heterogeneous.", bullet_style),
        Paragraph("• Class weighting is required in the loss, and evaluation must lead with "
                  "ROC-AUC and pneumonia recall, not accuracy.", bullet_style),
        Paragraph("• The intensity-separation finding motivates the CNN: if global brightness "
                  "already separates classes weakly, learned spatial features should do far "
                  "better.", bullet_style),
    ]

    # ── 5. Preprocessing ─────────────────────────────────────────────────────
    story += [PageBreak()] + section("5", "Data Preprocessing")

    story += [guideline("5.1 What we did")]
    story += [
        Paragraph("• Extracted 26,684 DICOMs to disk (one-time, ~3.5 GB) with a resume-safe "
                  "guard.", bullet_style),
        Paragraph("• Confirmed images are natively grayscale; added the channel dimension "
                  "(H, W) → (H, W, 1).", bullet_style),
        Paragraph("• Resized 1024×1024 → 128×128 and normalised each image by its own maximum "
                  "to [0, 1].", bullet_style),
        Paragraph("• Split patients 70/15/15 (train/validation/test), stratified by the binary "
                  "target.", bullet_style),
        Paragraph("• Defined an augmentation policy (random horizontal flip, small rotation, "
                  "zoom) for training.", bullet_style),
    ]

    story += [guideline("5.2 Why we did it")]
    story += [
        Paragraph("• <b>128×128</b> trades radiological detail for speed — appropriate for a "
                  "baseline whose job is to validate the pipeline; pretrained backbones in the "
                  "final phase use 224×224.", bullet_style),
        Paragraph("• <b>Per-image normalization</b> neutralises the scanner-dependent intensity "
                  "ranges observed in Section 3 (maxima 230–255).", bullet_style),
        Paragraph("• <b>Patient-level, stratified splitting</b> guarantees no patient appears in "
                  "two partitions (leakage) and that each partition keeps the 22.5% prevalence, "
                  "making validation and test metrics directly comparable.", bullet_style),
        Paragraph("• <b>Augmentation</b> combats overfitting on 18,677 training images; chest "
                  "X-rays are bilaterally symmetric, so horizontal flips are label-preserving.", bullet_style),
    ]

    story += [guideline("5.3 What we observed")]
    story += [
        Paragraph("=== Dataset Split ===", code_style),
        Paragraph("Train      : 18,677 patients (70%) | Pneumonia: 4,208 (22.5%)", code_style),
        Paragraph("Validation :  4,004 patients (15%) | Pneumonia:   902 (22.5%)", code_style),
        Paragraph("Test       :  4,003 patients (15%) | Pneumonia:   902 (22.5%)", code_style),
        Paragraph("Patient-level split: no patient appears in both train and test.", code_style),
        Spacer(1, 4),
        img("preprocessing_before_after.png", width=CONTENT_W * 0.95),
        Paragraph("Figure 4 — Before/after preprocessing: the 1024×1024 original (left) retains "
                  "its diagnostic structure after 128×128 resize and normalization (right).", caption_style),
        img("augmentation_demo.png", width=CONTENT_W * 0.95),
        Paragraph("Figure 5 — Augmentation samples: each transform preserves the diagnostic "
                  "label while varying presentation.", caption_style),
    ]

    story += [guideline("5.4 What we concluded")]
    story += [
        Paragraph("• Stratification worked exactly: 22.5% pneumonia in all three partitions — "
                  "no distribution drift between validation and test.", bullet_style),
        Paragraph("• Normalization verified: all processed pixels lie in [0, 1]; non-zero minima "
                  "reflect scanner baseline noise, handled correctly without clipping.", bullet_style),
        Paragraph("• Visual inspection (Figure 4) confirms opacities remain visible at 128×128 — "
                  "the resolution is sufficient for a meaningful baseline.", bullet_style),
    ]

    # ── 6. Model Building ────────────────────────────────────────────────────
    story += [PageBreak()] + section("6", "Model Building — CNN from Scratch")

    story += [guideline("6.1 What we did")]
    arch = [
        ["Component", "Choice", "Rationale"],
        ["Backbone", "3 × (Conv2D → BatchNorm → MaxPool),\nfilters 32/64/128",
         "Progressive features: edges → textures → structures"],
        ["Head", "GlobalAveragePooling → Dense(256) →\nDropout(0.5) → Sigmoid",
         "GAP cuts parameters vs Flatten; Dropout fights overfitting"],
        ["Size", "126,849 parameters", "Deliberately lightweight baseline"],
        ["Loss", "Binary cross-entropy with class weights\n{0: 0.645, 1: 2.219}",
         "Each missed pneumonia costs ~3.4× more"],
        ["Training", "Adam 1e-3 · batch 32 · max 20 epochs ·\nEarlyStopping + ReduceLROnPlateau on val AUC",
         "Checkpoint keeps the best-validation model"],
    ]
    story += [tbl(arch, [3.4 * cm, 6.8 * cm, CONTENT_W - 10.2 * cm]), Spacer(1, 4)]

    story += [guideline("6.2 Why we did it")]
    story += [
        para(
            "A from-scratch CNN answers the question every stakeholder should ask before "
            "investing in larger models: <b>how much signal can a small, fast, fully-owned "
            "model extract?</b> It also establishes the honest baseline against which transfer "
            "learning must justify itself in the final phase. Class weighting encodes the "
            "clinical cost asymmetry directly into training rather than leaving it to "
            "after-the-fact threshold hacks."
        ),
    ]

    story += [guideline("6.3 What we observed — Training")]
    hist = [
        ["Epoch", "Val AUC", "Note"],
        ["1", "0.7402", "Initial convergence"],
        ["2", "0.7706", ""],
        ["4", "0.6579", "Dip — learning rate reduced to 5e-4"],
        ["8", "0.8060", "Recovery after LR reduction"],
        ["13", "0.8208", ""],
        ["16", "0.8266", ""],
        ["20", "0.8357", "★ Best — checkpoint saved"],
    ]
    story += [tbl(hist, [2.2 * cm, 2.6 * cm, CONTENT_W - 4.8 * cm]), Spacer(1, 4)]
    story += [
        para(
            "Validation AUC improved from 0.7402 to <b>0.8357</b> across 20 epochs "
            "(~110 s/epoch on Apple M1 GPU). The learning-rate schedule mattered: after the "
            "epoch-4 dip, ReduceLROnPlateau halved the rate and the model resumed steady "
            "improvement — augmentation kept the model from overfitting through all 20 epochs."
        ),
        img("training_history.png", width=CONTENT_W),
        Paragraph("Figure 6 — Training curves: loss falling and AUC rising on both train and "
                  "validation, with no divergence — a healthy fit.", caption_style),
    ]

    story += [guideline("6.4 What we observed — Test Set Evaluation")]
    story += [
        Paragraph("Test AUC : 0.8353          (4,003 patients: 902 pneumonia / 3,101 no pneumonia)", code_style),
        Paragraph("                  precision    recall  f1-score   support", code_style),
        Paragraph("No Pneumonia (0)       0.93      0.65      0.77      3101", code_style),
        Paragraph("   Pneumonia (1)       0.41      0.84      0.56       902", code_style),
        Paragraph("        accuracy                           0.70      4003", code_style),
        Spacer(1, 4),
        img("evaluation_plots.png", width=CONTENT_W),
        Paragraph("Figure 7 — Test evaluation: ROC curve (AUC 0.8353) and confusion matrix at "
                  "threshold 0.5.", caption_style),
        img("pr_curve_and_threshold.png", width=CONTENT_W),
        Paragraph("Figure 8 — Precision-recall curve and threshold sweep: the trade-off curve "
                  "clinical stakeholders will use to set the operating point.", caption_style),
        img("misclassified_samples.png", width=CONTENT_W),
        Paragraph("Figure 9 — Misclassification analysis with Grad-CAM heat-maps: false "
                  "negatives are dominated by subtle, early-stage opacities; false positives "
                  "come largely from the 'Not Normal' sub-class.", caption_style),
    ]

    story += [guideline("6.5 What we concluded")]
    story += [
        Paragraph("• <b>The baseline is clinically meaningful</b>: 84% of pneumonia cases are "
                  "caught (758 of 902), with a highly trustworthy negative class (93% "
                  "precision) — the profile a triage tool needs.", bullet_style),
        Paragraph("• <b>Class weighting worked as designed</b>: it moved the default operating "
                  "point toward recall, rather than leaving the model to default to the "
                  "majority class.", bullet_style),
        Paragraph("• <b>The cost is precision (0.41)</b>: roughly 6 in 10 pneumonia flags are "
                  "false alarms, mostly from the pneumonia-mimicking 'Not Normal' class — the "
                  "clear target for improvement.", bullet_style),
        Paragraph("• <b>Headroom is visible</b>: AUC 0.8353 from a 126K-parameter model at "
                  "128×128 suggests pretrained backbones at 224×224 can push both AUC and "
                  "precision higher — the central hypothesis for the final phase.", bullet_style),
    ]

    # ── 7. Conclusions & Next Steps ──────────────────────────────────────────
    story += [PageBreak()] + section("7", "Overall Conclusions &amp; Road Map")
    story += [
        para("<b>What this interim phase delivered:</b>"),
        Paragraph("• A verified, leakage-safe data pipeline from raw DICOM archives to "
                  "model-ready tensors, with the true 22.5% prevalence established.", bullet_style),
        Paragraph("• Evidence-based preprocessing decisions (per-image normalization, "
                  "patient-level stratified splits) — each justified by an observed property "
                  "of the data.", bullet_style),
        Paragraph("• A scratch-CNN baseline at <b>Test ROC-AUC 0.8353 with 84% pneumonia "
                  "recall</b> — already a usable screening profile, and an honest benchmark "
                  "for what follows.", bullet_style),
        Spacer(1, 6),
        para("<b>Road map for the final report:</b>"),
    ]
    roadmap = [
        ["Planned Work", "Expected Business Outcome"],
        ["Transfer learning: ResNet50V2 and EfficientNetB0,\nfrozen then fine-tuned, at 224×224",
         "Higher AUC and better precision at equal recall — fewer false alarms per detection"],
        ["Validation-tuned decision thresholds\n(85% sensitivity target)",
         "A defensible, documented operating point set on validation data, not guesswork"],
        ["Model comparison and selection",
         "A single best model chosen on clinical criteria, serialized for deployment"],
        ["Streamlit web app in Docker + model registry",
         "A reproducible, demonstrable tool any stakeholder can run and test"],
    ]
    story += [tbl(roadmap, [8.2 * cm, CONTENT_W - 8.2 * cm]), Spacer(1, 8)]
    story += [
        rule(),
        Spacer(1, 4),
        para("<i>Companion notebook: <code>src/pneumonia_interim.ipynb</code> | "
             "Model checkpoint: <code>best_cnn_model.keras</code> | "
             "All figures and outputs in this report are reproduced from the executed "
             "notebook.</i>"),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved → {OUT}")


if __name__ == "__main__":
    build()
