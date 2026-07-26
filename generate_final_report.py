"""Generate Pneumonia Detection Final Project Report PDF.

Recreated from generate_report.py (interim report) as the baseline —
same styles, cover layout, header/footer, and section conventions,
extended with Transfer Learning, Deployment, and final results.
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

ROOT   = os.path.dirname(os.path.abspath(__file__))
SRC    = os.path.join(ROOT, "src")
ASSETS = os.path.join(SRC, "report_assets")
OUT    = os.path.join(ROOT, "Pneumonia_Detection_Final_Report.pdf")

APP_URL   = "http://localhost:8501"
MODEL_URL = "https://huggingface.co/dvsreddy/pneumonia-detection-model"

# ---------------------------------------------------------------------------
# Styles (identical to interim baseline)
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
    textColor=colors.HexColor("#1a3a5c"), spaceBefore=18, spaceAfter=6, borderPad=0,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=12, leading=16,
    textColor=colors.HexColor("#2c5f8a"), spaceBefore=12, spaceAfter=4,
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

# ---------------------------------------------------------------------------
# Helpers (identical to interim baseline)
# ---------------------------------------------------------------------------
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

def img(filename, width=None, height=None, base=None):
    path = os.path.join(base or SRC, filename)
    if not os.path.exists(path):
        return Spacer(1, 0)
    if width and not height:
        from PIL import Image as PILImage
        im = PILImage.open(path)
        w, h = im.size
        height = width * h / w
    return Image(path, width=width or 5 * inch, height=height or 3 * inch)

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"),
                      spaceAfter=4, spaceBefore=4)

def para(text, style=None):
    return Paragraph(text, style or body_style)

def section(number, title):
    return [rule(), Paragraph(f"{number}. {title}", h1_style)]

def subsection(label, title):
    return Paragraph(f"{label} {title}", h2_style)

# ---------------------------------------------------------------------------
# Header / Footer
# ---------------------------------------------------------------------------
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#1a3a5c"))
    canvas.rect(0, PAGE_H - 1.0 * cm, PAGE_W, 1.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H - 0.65 * cm,
                      "Pneumonia Detection — Final Project Report")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.65 * cm, "RSNA Challenge | 2026")
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 0.6 * cm, "Confidential | For Academic Use Only")
    canvas.drawRightString(PAGE_W - MARGIN, 0.6 * cm, f"Page {doc.page}")
    canvas.restoreState()

# ---------------------------------------------------------------------------
# Build content
# ---------------------------------------------------------------------------
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
        Paragraph("Final Project Report", subtitle_style),
        Spacer(1, 0.3 * cm),
        rule(),
        Spacer(1, 0.2 * cm),
        Paragraph("RSNA Pneumonia Detection Challenge", meta_style),
        Paragraph("Deep Learning · Transfer Learning · TensorFlow / Keras · Streamlit · Docker", meta_style),
        Paragraph("Apple M1 GPU (TensorFlow Metal) · Python 3.12", meta_style),
        Spacer(1, 0.3 * cm),
        rule(),
        Spacer(1, 0.5 * cm),
    ]

    meta_data = [
        ["Dataset", "RSNA Pneumonia Detection Challenge (Kaggle)"],
        ["Total Patients", "26,684 unique chest X-rays (DICOM format)"],
        ["Framework", "TensorFlow 2.16 / Keras — Apple M1 GPU"],
        ["Best Model", "ResNet50V2 fine-tuned — Test ROC-AUC 0.8546"],
        ["Web Application", f"Streamlit in Docker — {APP_URL}"],
        ["Model Registry", MODEL_URL],
        ["Submission Type", "Final Report"],
        ["Date", "July 2026"],
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
    story += [mt, Spacer(1, 0.5 * cm)]

    story += [Paragraph("Final Evaluation Rubric", h2_style)]
    rubric = [
        ["Section", "Key Deliverables", "Points"],
        ["Data Overview", "Import data · Check shape", "3"],
        ["Exploratory Data Analysis",
         "Sample images per class · Class imbalance · Observations", "3"],
        ["Data Preprocessing",
         "Grayscale · Before/after plots · Train/Val/Test split · Normalization", "4"],
        ["Model Building", "CNN from scratch · Training · Performance commentary", "5"],
        ["Transfer Learning",
         "≥2 pretrained CNNs · New architectures · Comparison · Best model · Serialize + inference", "30"],
        ["Model Deployment",
         "Streamlit/Gradio app · Docker packaging · Hugging Face + inference", "5"],
        ["Actionable Insights", "Key takeaways for the business", "4"],
        ["Business Report Quality", "Adhere to report checklist", "6"],
        ["Total", "", "60"],
    ]
    rt = Table(rubric, colWidths=[3.8 * cm, CONTENT_W - 5.4 * cm, 1.6 * cm], repeatRows=1)
    rt.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND",   (0, -1), (-1, -1), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",    (0, -1), (-1, -1), colors.white),
        ("FONTNAME",     (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTNAME",     (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#edf3fa")]),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("ALIGN",        (2, 0), (2, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
    ]))
    story += [rt, PageBreak()]

    # ── 1. Executive Summary ─────────────────────────────────────────────────
    story += section("1", "Executive Summary")
    story += [
        para(
            "This report documents the final phase of an automated pneumonia detection system "
            "built with deep learning on chest X-ray images in DICOM format, drawn from the "
            "<b>RSNA Pneumonia Detection Challenge</b> (26,684 unique patients, 22.5% pneumonia "
            "prevalence)."
        ),
        para(
            "The interim phase established a scratch-CNN baseline (<b>Test ROC-AUC 0.7853</b>). "
            "In this final phase, transfer learning with two ImageNet backbones — ResNet50V2 and "
            "EfficientNetB0, each trained frozen and then fine-tuned — lifted performance to a "
            "best of <b>ROC-AUC 0.8546 / PR-AUC 0.6432</b> (ResNet50V2, top 30 layers fine-tuned). "
            "At a validation-tuned decision threshold of 0.408, the deployed model detects "
            "<b>81.6% of pneumonia cases</b> (736 of 902 on the held-out test set) while its "
            "negative calls remain 93.2% precise."
        ),
        para(
            f"The best model is serialized, published to the Hugging Face Model Hub, and served "
            f"through a <b>Streamlit web application packaged in Docker</b>, deployed locally for "
            f"testing at <b>{APP_URL}</b> and verified end-to-end with live DICOM inference."
        ),
    ]

    # ── 2. Business Context ──────────────────────────────────────────────────
    story += section("2", "Business Context &amp; Problem Statement")
    story += [
        para(
            "Pneumonia is one of the leading causes of morbidity and mortality worldwide, "
            "disproportionately affecting children under five and elderly populations. "
            "The World Health Organization (WHO) identifies pneumonia as a significant driver of "
            "infectious-disease mortality globally."
        ),
        para("The gold-standard diagnostic pathway faces systemic bottlenecks:"),
        Paragraph("• <b>Radiologist scarcity</b> — in rural and resource-limited settings, skilled "
                  "radiologist access is severely constrained.", bullet_style),
        Paragraph("• <b>Human error and fatigue</b> — high patient loads and shift-based workflows "
                  "introduce variability and diagnostic error.", bullet_style),
        Paragraph("• <b>Delayed diagnosis</b> — waiting for specialist availability delays antibiotic "
                  "treatment, worsening outcomes and driving antibiotic overuse.", bullet_style),
        Spacer(1, 4),
        para(
            "Automated deep learning systems offer a scalable, consistent, low-cost complement to "
            "radiologist review — a <b>clinical decision-support tool</b> that flags high-risk "
            "cases for priority review rather than replacing the clinician."
        ),
    ]

    # ── 3. Objectives ────────────────────────────────────────────────────────
    story += section("3", "Objectives")
    story += [
        Paragraph("1. <b>Accurately classify</b> chest X-rays as pneumonia-positive or negative "
                  "using deep learning and transfer learning.", bullet_style),
        Paragraph("2. <b>Prioritise sensitivity</b> — tune the decision threshold so missed "
                  "pneumonia cases are minimised at clinically acceptable precision.", bullet_style),
        Paragraph("3. <b>Compare architectures rigorously</b> — scratch CNN vs frozen and "
                  "fine-tuned pretrained backbones, on identical splits and metrics.", bullet_style),
        Paragraph("4. <b>Deploy</b> the best model as a web application packaged in Docker with "
                  "the model published to a public registry.", bullet_style),
        Paragraph("5. <b>Deliver actionable business insights</b> for adoption as a screening/triage "
                  "tool in clinical workflows.", bullet_style),
    ]

    # ── 4. Dataset Description ───────────────────────────────────────────────
    story += section("4", "Dataset Description")
    story += [
        para(
            "<b>Source:</b> RSNA Pneumonia Detection Challenge (Kaggle). Chest X-rays are stored in "
            "<b>DICOM format</b> (.dcm), embedding patient metadata and raw pixel arrays in one file."
        ),
        subsection("4.1", "Three-Class Taxonomy"),
    ]
    taxonomy = [
        ["Class", "Binary Target", "Meaning"],
        ["Normal", "0", "Healthy lungs"],
        ["No Lung Opacity / Not Normal", "0",
         "Chest abnormality present (e.g., cardiomegaly, effusion)\nbut not pneumonia"],
        ["Lung Opacity", "1",
         "Pneumonia present — white/grey opacities in lung fields"],
    ]
    story += [
        tbl(taxonomy, [5.0 * cm, 2.5 * cm, CONTENT_W - 7.5 * cm]),
        Spacer(1, 4),
        para(
            "<i>The 'No Lung Opacity / Not Normal' class is the most diagnostically challenging — "
            "real pathology that visually resembles pneumonia, making the negative class "
            "heterogeneous and the decision boundary harder to learn.</i>"
        ),
    ]

    # ── 5. Data Overview ─────────────────────────────────────────────────────
    story += [PageBreak()] + section("5", "Data Overview")
    inv = [
        ["Asset", "Details"],
        ["data/stage_2_train_images.zip", "26,684 training DICOM files (~3.5 GB)"],
        ["data/stage_2_test_images.zip", "3,000 test DICOM files (~380 MB)"],
        ["stage_2_train_labels.csv", "30,227 rows × 4 columns"],
        ["stage_2_detailed_class_info.csv", "30,227 rows × 2 columns"],
    ]
    story += [tbl(inv, [6.5 * cm, CONTENT_W - 6.5 * cm]), Spacer(1, 6)]

    obs = [
        ["Metric", "Value"],
        ["Training CSV rows", "30,227"],
        ["Unique training patients", "26,684"],
        ["Image properties", "1024×1024, uint8, single-channel grayscale"],
        ["Pneumonia patients (deduplicated)", "6,012  (22.5%)"],
        ["No-pneumonia patients", "20,672  (77.5%)"],
    ]
    story += [tbl(obs, [8.0 * cm, CONTENT_W - 8.0 * cm]), Spacer(1, 4)]
    story += [
        para(
            "<b>Key finding — the raw CSV inflates pneumonia counts.</b> Pneumonia patients carry "
            "one row per bounding-box annotation (30,227 rows vs 26,684 patients). Deduplication to "
            "patient level before splitting is essential: true prevalence is <b>22.5%</b>, not the "
            "31.6% the raw CSV implies, and duplicate rows across splits would constitute data "
            "leakage."
        ),
    ]

    # ── 6. EDA ═══════════════════════════════════════════════════════════════
    story += section("6", "Exploratory Data Analysis")
    dist = [
        ["Class", "Patient Count", "% of Total"],
        ["No Lung Opacity / Not Normal", "11,821", "44.3%"],
        ["Normal", "8,851", "33.2%"],
        ["Lung Opacity (Pneumonia)", "6,012", "22.5%"],
        ["Total", "26,684", "100%"],
    ]
    story += [tbl(dist), Spacer(1, 6)]
    story += [
        img("class_imbalance.png", width=CONTENT_W * 0.75),
        Paragraph("Figure 1 — Patient-level class distribution (3.44:1 imbalance). A naive "
                  "always-negative classifier reaches 77.5% accuracy, which is why ROC-AUC, "
                  "PR-AUC, and recall drive all evaluation.", caption_style),
        img("sample_images_per_class.png", width=CONTENT_W),
        Paragraph(
            "Figure 2 — Representative X-rays. Left: Normal (clear lung fields). "
            "Centre: Not Normal (other pathology). Right: Lung Opacity / pneumonia "
            "(white opacities in lung fields).", caption_style),
        img("pixel_statistics_per_class.png", width=CONTENT_W),
        Paragraph(
            "Figure 3 — Mean pixel intensity per class: pneumonia images are measurably brighter "
            "due to opacity regions — confirmation that learnable signal exists.", caption_style),
    ]

    # ── 7. Preprocessing ─────────────────────────────────────────────────────
    story += [PageBreak()] + section("7", "Data Preprocessing")
    split = [
        ["Split", "Patients", "Pneumonia (Target=1)", "% Pneumonia"],
        ["Train",      "18,677", "4,208", "22.5%"],
        ["Validation",  "4,004",   "902", "22.5%"],
        ["Test",        "4,003",   "902", "22.5%"],
        ["Total",      "26,684", "6,012", "22.5%"],
    ]
    story += [
        subsection("7.1", "Stratified Patient-Level Split (70/15/15)"),
        tbl(split),
        Spacer(1, 4),
        para("Stratification preserves the 22.5% prevalence identically in every partition; "
             "splitting at patient level prevents leakage from duplicate bounding-box rows."),
        subsection("7.2", "Pipelines"),
        Paragraph("• <b>Scratch CNN</b>: DICOM → float32 → resize 128×128 → per-image "
                  "normalization to [0, 1] → (128, 128, 1).", bullet_style),
        Paragraph("• <b>Transfer models</b>: DICOM → resize 224×224 → grayscale tiled to 3 "
                  "channels → raw [0, 255] pixels; model-specific input scaling is embedded "
                  "inside each model graph (ResNet50V2: [-1, 1] Rescaling layer; EfficientNetB0: "
                  "internal rescaling), making the saved models fully self-contained.", bullet_style),
        Paragraph("• <b>Performance</b>: all 26,684 DICOMs are decoded once into a 1.3 GB uint8 "
                  "cache feeding a pure-TensorFlow input pipeline — epochs are compute-bound "
                  "rather than I/O-bound.", bullet_style),
        Paragraph("• <b>Class weights</b> {0: 0.6454, 1: 2.2192} make each missed pneumonia "
                  "case ~3.4× more costly during training.", bullet_style),
        Paragraph("• <b>Augmentation</b> (random horizontal flip, ±18° rotation, 10% zoom) is "
                  "embedded as model layers — active in training, no-ops at inference.", bullet_style),
    ]
    story += [
        img("preprocessing_before_after.png", width=CONTENT_W),
        Paragraph("Figure 4 — Preprocessing: original 1024×1024 DICOM (left) → resized, "
                  "normalised model input (right).", caption_style),
        img("augmentation_demo.png", width=CONTENT_W),
        Paragraph("Figure 5 — Augmentation samples: label-preserving transforms that expand the "
                  "effective training set.", caption_style),
    ]

    # ── 8. Model Building — scratch CNN ──────────────────────────────────────
    story += [PageBreak()] + section("8", "Model Building — CNN from Scratch (Baseline)")
    arch = [
        ["Component", "Value"],
        ["Architecture", "3 × (Conv2D → BatchNorm → MaxPool), filters 32/64/128"],
        ["Head", "GlobalAveragePooling2D → Dense(256, ReLU) → Dropout(0.5) → Sigmoid"],
        ["Parameters", "126,849 total"],
        ["Input", "128 × 128 × 1"],
        ["Training", "Adam 1e-3 · class weights · EarlyStopping(val_auc) · ReduceLROnPlateau"],
    ]
    story += [tbl(arch, [4.0 * cm, CONTENT_W - 4.0 * cm]), Spacer(1, 6)]
    story += [
        para(
            "The baseline trained for 5 epochs before early stopping; best weights (epoch 2, "
            "val AUC 0.7779) were restored automatically. On the held-out test set it achieved "
            "<b>ROC-AUC 0.7853</b> with overall accuracy 0.75 and macro-F1 0.68 — real "
            "discriminative signal, but recall at the default 0.5 threshold was clinically "
            "unusable, motivating both threshold calibration and transfer learning."
        ),
        img("training_history.png", width=CONTENT_W),
        Paragraph("Figure 6 — Scratch CNN training curves.", caption_style),
        img("evaluation_plots.png", width=CONTENT_W),
        Paragraph("Figure 7 — Scratch CNN test evaluation: ROC curve and confusion matrix.", caption_style),
        img("pr_curve_and_threshold.png", width=CONTENT_W),
        Paragraph("Figure 8 — Precision-recall and threshold sweep: recall is recoverable by "
                  "lowering the threshold — the insight that drives validation-tuned thresholds "
                  "in Section 9.", caption_style),
        img("misclassified_samples.png", width=CONTENT_W),
        Paragraph("Figure 9 — Misclassification analysis with Grad-CAM: false negatives are "
                  "dominated by subtle early-stage opacities; false positives largely come from "
                  "the 'Not Normal' negative sub-class.", caption_style),
    ]

    # ── 9. Transfer Learning ─────────────────────────────────────────────────
    story += [PageBreak()] + section("9", "Transfer Learning")
    story += [
        para(
            "Two ImageNet backbones were trained under an identical two-phase protocol on the "
            "same splits: <b>Phase 1</b> — frozen backbone, new classification head, LR 1e-3; "
            "<b>Phase 2</b> — top layers unfrozen (ResNet50V2: 30 layers / 14.9M parameters; "
            "EfficientNetB0: 20 layers / 1.7M), LR 1e-5, <b>BatchNorm kept frozen</b> to protect "
            "ImageNet statistics from catastrophic forgetting. Decision thresholds were selected "
            "on the <b>validation set</b> for an 85% sensitivity target — never on test data."
        ),
        subsection("9.1", "Results — Held-Out Test Set (4,003 patients)"),
    ]
    results = [
        ["Model", "ROC-AUC", "PR-AUC", "Recall", "Precision", "Threshold"],
        ["ResNet50V2 (Fine-Tuned) ★ selected", "0.8546", "0.6432", "0.816", "0.469", "0.408"],
        ["EfficientNetB0 (Fine-Tuned)", "0.8457", "0.6055", "0.847", "0.427", "0.305"],
        ["ResNet50V2 (Frozen)", "0.8391", "0.5996", "0.837", "0.426", "0.399"],
        ["EfficientNetB0 (Frozen)", "0.8366", "0.5848", "0.864", "0.410", "0.383"],
        ["CNN Scratch (baseline)", "0.7853", "—", "—", "—", "0.50"],
    ]
    rt2 = Table(results, colWidths=[6.2 * cm, 2.0 * cm, 2.0 * cm, 1.8 * cm, 2.0 * cm, 2.0 * cm],
                repeatRows=1)
    rt2.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND",   (0, 1), (-1, 1), colors.HexColor("#d4e8c2")),
        ("FONTNAME",     (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTNAME",     (0, 2), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 2), (-1, -1), [colors.white, colors.HexColor("#edf3fa")]),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("ALIGN",        (1, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story += [rt2, Spacer(1, 6)]
    story += [
        img("tl_model_comparison.png", width=CONTENT_W * 0.95, base=ASSETS),
        Paragraph("Figure 10 — Test ROC-AUC across all five models.", caption_style),
    ]

    story += [subsection("9.2", "Training Behaviour")]
    story += [
        img("tl_resnet_frozen_training.png", width=CONTENT_W * 0.9, base=ASSETS),
        Paragraph("Figure 11 — ResNet50V2 frozen: validation AUC plateaus near 0.839 — the "
                  "ceiling of fixed ImageNet features.", caption_style),
        img("tl_resnet_ft_training.png", width=CONTENT_W * 0.9, base=ASSETS),
        Paragraph("Figure 12 — ResNet50V2 fine-tuning: validation AUC climbs to 0.8617 (epoch 9) "
                  "with no catastrophic-forgetting collapse.", caption_style),
        img("tl_effnet_frozen_training.png", width=CONTENT_W * 0.9, base=ASSETS),
        Paragraph("Figure 13 — EfficientNetB0 frozen: slower, noisier convergence from the "
                  "smaller 328K-parameter head.", caption_style),
        img("tl_effnet_ft_training.png", width=CONTENT_W * 0.9, base=ASSETS),
        Paragraph("Figure 14 — EfficientNetB0 fine-tuning: smooth +0.9 AUC-point gain from only "
                  "1.67M trainable parameters.", caption_style),
    ]

    story += [subsection("9.3", "Key Observations")]
    story += [
        Paragraph("1. <b>Transfer learning is worth +5.1 to +6.9 AUC points</b> over the scratch "
                  "baseline; even frozen ImageNet features beat it decisively — at this data "
                  "scale, pretraining is not optional.", bullet_style),
        Paragraph("2. <b>Fine-tuning always helped</b>: ResNet +1.6 points, EfficientNet +0.9 — "
                  "gains scale with how much capacity is allowed to adapt.", bullet_style),
        Paragraph("3. <b>PR-AUC separates models more sharply than ROC-AUC</b> (5.8-point spread "
                  "vs 1.8). Best PR-AUC of 0.6432 is 2.9× the 0.225 random baseline at 22.5% "
                  "prevalence.", bullet_style),
        Paragraph("4. <b>Validation-tuned thresholds generalised</b>: the 85% validation "
                  "sensitivity target landed at 81.6–86.4% recall on test.", bullet_style),
        Paragraph("5. <b>Size-accuracy frontier</b>: ResNet50V2-FT wins absolute AUC (207 MB "
                  "artifact); EfficientNetB0-FT trails by ~1 point at 30 MB — the edge-device "
                  "alternative.", bullet_style),
    ]

    story += [subsection("9.4", "Best Model — Selection, Serialization &amp; Inference")]
    story += [
        para(
            "<b>ResNet50V2 fine-tuned</b> was selected: highest ROC-AUC and precision at "
            "comparable recall. The model was saved to <code>best_final_model.keras</code> "
            "(self-contained — augmentation and input scaling embedded), reloaded from disk, and "
            "verified on held-out test images:"
        ),
        img("tl_inference_demo.png", width=CONTENT_W * 0.95, base=ASSETS),
        Paragraph("Figure 15 — Inference with the reloaded model on six held-out X-rays "
                  "(3 pneumonia, 3 normal) at the 0.408 operating point.", caption_style),
    ]

    # ── 10. Deployment ───────────────────────────────────────────────────────
    story += [PageBreak()] + section("10", "Model Deployment")
    story += [
        para(
            f"The application is a <b>Streamlit web app packaged in Docker</b> and deployed "
            f"locally for testing at <b>{APP_URL}</b>. The trained model is published to the "
            f"Hugging Face Model Hub — <b>{MODEL_URL}</b> — which serves as the model registry: "
            f"the app uses its baked-in copy of the model and can fall back to downloading from "
            f"the Hub."
        ),
        para(
            "<b>Platform note:</b> Hugging Face now requires a PRO subscription to host "
            "application Spaces (Docker/Gradio return 402 Payment Required on the free tier, and "
            "the Streamlit SDK has been removed). PRO is not enabled, so <b>local Docker testing "
            "is the adopted deployment path</b>; a ready-made, PRO-gated Space deployment cell "
            "remains in the notebook for the future."
        ),
    ]
    stack = [
        ["Layer", "Technology", "Status"],
        ["Model registry", "Hugging Face Model Hub (free, public)", "Live"],
        ["Application", "Streamlit + TensorFlow (in-process inference)", "Live (local)"],
        ["Container", "Docker — python:3.12-slim, port 7860 → 8501", "Built & health-checked"],
        ["Cloud Space (optional)", "HF Docker Space", "Dormant — needs PRO"],
    ]
    story += [tbl(stack, [4.0 * cm, 8.0 * cm, CONTENT_W - 12.0 * cm]), Spacer(1, 6)]
    story += [
        img("app_screenshot.png", width=CONTENT_W * 0.92, base=ASSETS),
        Paragraph(f"Figure 16 — The deployed Streamlit application at {APP_URL}: upload panel, "
                  "adjustable decision threshold, and model documentation.", caption_style),
        img("app_prediction.png", width=CONTENT_W * 0.92, base=ASSETS),
        Paragraph("Figure 17 — Live inference on a pneumonia-positive DICOM: PNEUMONIA at 52.0% "
                  "confidence against the 0.35 screening threshold, with the clinical "
                  "decision-support disclaimer.", caption_style),
        subsection("10.1", "Reproducible Deployment Commands"),
        Paragraph("docker build -t pneumonia-detection .", code_style),
        Paragraph("docker run -d --name pneumonia-app -p 8501:7860 pneumonia-detection", code_style),
        Paragraph(f"open {APP_URL}", code_style),
    ]

    # ── 11. Key Findings & Business Implications ─────────────────────────────
    story += [PageBreak()] + section("11", "Key Findings &amp; Business Implications")
    bi = [
        ["Finding", "Business Impact"],
        ["81.6% pneumonia recall at validation-tuned threshold",
         "Deployable as triage: 4 of 5 pneumonia cases surfaced automatically for priority review"],
        ["93.2% precision on negative calls",
         "Safe queue de-prioritisation — a 'clear' flag from the model is trustworthy"],
        ["+6.9 AUC points from transfer learning",
         "Never train radiology models from scratch at this data scale; pretrained backbones are standard practice"],
        ["Thresholds are model-specific (0.305–0.408 tuned range)",
         "Threshold governance must be part of every retrain — a copied threshold silently changes sensitivity"],
        ["30 MB EfficientNet within ~1 AUC point of best",
         "Edge deployment (portable X-ray units, rural clinics) is viable with minimal accuracy loss"],
        ["Self-contained .keras artifact (preprocessing in-graph)",
         "Eliminates train/serve skew — a whole class of production incidents avoided"],
    ]
    story += [tbl(bi, [6.5 * cm, CONTENT_W - 6.5 * cm]), Spacer(1, 4)]
    story += [
        para(
            "<b>Recommended operating policy:</b> deploy as a screening/triage aid with the "
            "validation-derived threshold, require radiologist confirmation for all positive "
            "flags, and re-derive the threshold with clinical stakeholders whenever the model is "
            "retrained."
        ),
    ]

    # ── 12. Limitations & Future Work ────────────────────────────────────────
    story += section("12", "Limitations &amp; Future Work")
    story += [
        Paragraph("• <b>Single-site dataset</b> — RSNA data does not capture all scanner/protocol "
                  "variation; multi-site validation is required before clinical use.", bullet_style),
        Paragraph("• <b>224×224 input</b> still discards fine radiological texture from the "
                  "1024×1024 originals; 384px input is the next highest-yield experiment.", bullet_style),
        Paragraph("• <b>No explainability in the app yet</b> — Grad-CAM overlays (demonstrated in "
                  "the notebook) should ship in the UI for radiologist trust.", bullet_style),
        Paragraph("• <b>Ensembling untested</b> — ResNet + EfficientNet ensembling is a likely "
                  "+1–2 AUC-point gain.", bullet_style),
        Paragraph("• <b>Cloud hosting deferred</b> — the HF Space deployment activates with a PRO "
                  "subscription; alternatives (Streamlit Community Cloud via GitHub) were "
                  "descoped with the git pipeline.", bullet_style),
        Paragraph("• <b>Regulatory path</b> — clinical deployment requires FDA 510(k) (US) or "
                  "equivalent, with model cards, bias analysis, and failure-mode documentation.", bullet_style),
    ]

    # ── 13. Conclusion ───────────────────────────────────────────────────────
    story += section("13", "Conclusion")
    story += [
        para(
            "This final report completes the end-to-end machine learning lifecycle begun in the "
            "interim phase:"
        ),
        Paragraph("• <b>Data engineering</b> — leakage-safe patient-level splits, DICOM quirks "
                  "handled, and a cached input pipeline.", bullet_style),
        Paragraph("• <b>Modeling</b> — scratch CNN baseline (AUC 0.7853) → transfer learning with "
                  "correct fine-tuning hygiene → <b>ResNet50V2 at AUC 0.8546</b> with 81.6% "
                  "pneumonia recall at a validation-tuned threshold.", bullet_style),
        Paragraph("• <b>Deployment</b> — model published to the Hugging Face Model Hub, served by "
                  f"a Dockerised Streamlit app at <b>{APP_URL}</b>, verified with live DICOM "
                  "inference.", bullet_style),
        Spacer(1, 6),
        para(
            "The system meets its design goal: an automated, reproducible decision-support tool "
            "that surfaces four of five pneumonia cases for priority review while keeping "
            "negative calls reliable — a meaningful step toward faster, more consistent pneumonia "
            "diagnosis in resource-constrained settings."
        ),
        Spacer(1, 8),
        rule(),
        Spacer(1, 4),
        para(
            "<i>Notebook: <code>src/pneumonia_final.ipynb</code> | "
            "Best model: <code>best_final_model.keras</code> | "
            f"Model Hub: <code>{MODEL_URL}</code> | "
            f"Web app: <code>{APP_URL}</code></i>"
        ),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved → {OUT}")


if __name__ == "__main__":
    build()
