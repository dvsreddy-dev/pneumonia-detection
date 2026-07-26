"""Generate Pneumonia Detection Interim Project Report PDF."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BalancedColumns

SRC = "/Users/vsrdhoolla/learnings/pneumonia-detection/src"
OUT = "/Users/vsrdhoolla/learnings/pneumonia-detection/Pneumonia_Detection_Interim_Report.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=22,
    leading=28,
    textColor=colors.HexColor("#1a3a5c"),
    spaceAfter=6,
    alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=18,
    textColor=colors.HexColor("#2c5f8a"),
    spaceAfter=4,
    alignment=TA_CENTER,
)
meta_style = ParagraphStyle(
    "Meta",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
    spaceAfter=2,
)
h1_style = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#1a3a5c"),
    spaceBefore=18,
    spaceAfter=6,
    borderPad=0,
)
h2_style = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#2c5f8a"),
    spaceBefore=12,
    spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    textColor=colors.HexColor("#222222"),
    spaceAfter=6,
    alignment=TA_JUSTIFY,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=18,
    bulletIndent=6,
    spaceAfter=3,
)
code_style = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontSize=8,
    leading=12,
    backColor=colors.HexColor("#f5f5f5"),
    leftIndent=12,
    rightIndent=12,
    spaceBefore=4,
    spaceAfter=4,
    textColor=colors.HexColor("#333333"),
)
caption_style = ParagraphStyle(
    "Caption",
    parent=styles["Normal"],
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
    spaceAfter=8,
    spaceBefore=2,
)
note_style = ParagraphStyle(
    "Note",
    parent=body_style,
    textColor=colors.HexColor("#555555"),
    fontSize=9,
    leading=13,
    leftIndent=12,
    rightIndent=12,
)

# ---------------------------------------------------------------------------
# Helpers
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

def img(filename, width=None, height=None):
    path = os.path.join(SRC, filename)
    if not os.path.exists(path):
        return Spacer(1, 0)
    if width and not height:
        from PIL import Image as PILImage
        im = PILImage.open(path)
        w, h = im.size
        height = width * h / w
    return Image(path, width=width or 5*inch, height=height or 3*inch)

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"),
                      spaceAfter=4, spaceBefore=4)

def b(text):
    return f"<b>{text}</b>"

def para(text, style=None):
    return Paragraph(text, style or body_style)

def section(number, title):
    return [
        rule(),
        Paragraph(f"{number}. {title}", h1_style),
    ]

def subsection(label, title):
    return Paragraph(f"{label} {title}", h2_style)

# ---------------------------------------------------------------------------
# Header / Footer
# ---------------------------------------------------------------------------
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(colors.HexColor("#1a3a5c"))
    canvas.rect(0, PAGE_H - 1.0*cm, PAGE_W, 1.0*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H - 0.65*cm,
                      "Pneumonia Detection — Interim Project Report")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.65*cm, "RSNA Challenge | 2024")
    # Footer
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 0.6*cm, "Confidential | For Academic Use Only")
    canvas.drawRightString(PAGE_W - MARGIN, 0.6*cm, f"Page {doc.page}")
    canvas.restoreState()

# ---------------------------------------------------------------------------
# Build content
# ---------------------------------------------------------------------------
def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.4*cm,
        bottomMargin=1.2*cm,
    )

    story = []

    # ── Cover ────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 1.8*cm),
        Paragraph("Pneumonia Detection from Chest X-Rays", title_style),
        Paragraph("Interim Project Report", subtitle_style),
        Spacer(1, 0.3*cm),
        rule(),
        Spacer(1, 0.2*cm),
        Paragraph("RSNA Pneumonia Detection Challenge", meta_style),
        Paragraph("Deep Learning · Convolutional Neural Networks · TensorFlow / Keras", meta_style),
        Paragraph("Apple M1 GPU (TensorFlow Metal) · Python 3.12", meta_style),
        Spacer(1, 0.3*cm),
        rule(),
        Spacer(1, 0.5*cm),
    ]

    # Metadata table
    meta_data = [
        ["Dataset", "RSNA Pneumonia Detection Challenge (Kaggle)"],
        ["Total Patients", "26,684 unique chest X-rays (DICOM format)"],
        ["Framework", "TensorFlow 2.16 / Keras — Apple M1 GPU"],
        ["Submission Type", "Interim Report"],
        ["Date", "July 2026"],
        ["Sections", "Data Overview · EDA · Preprocessing · CNN Baseline"],
    ]
    mt = Table(meta_data, colWidths=[3.8*cm, CONTENT_W - 3.8*cm])
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
    story += [mt, Spacer(1, 0.5*cm)]

    # Scoring rubric
    story += [
        Paragraph("Interim Evaluation Rubric", h2_style),
    ]
    rubric = [
        ["Section", "Key Deliverables", "Points"],
        ["Data Overview", "Import data · Check shape · File inventory", "6"],
        ["Exploratory Data Analysis",
         "Sample images per class · Class imbalance · Observations", "8"],
        ["Data Preprocessing",
         "Grayscale conversion · Before/after plots · Train/Val/Test split · Normalization", "10"],
        ["Model Building",
         "CNN from scratch · Training · Performance commentary", "10"],
        ["Business Report Quality", "Adhere to report checklist", "6"],
        ["Total", "", "40"],
    ]
    rt = Table(rubric, colWidths=[3.8*cm, CONTENT_W - 5.4*cm, 1.6*cm], repeatRows=1)
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
            "This report documents the interim phase of an automated pneumonia detection system "
            "built using deep learning applied to chest X-ray images in DICOM format. "
            "The dataset is drawn from the <b>RSNA Pneumonia Detection Challenge</b> (Kaggle), "
            "comprising <b>26,684 unique patient chest X-rays</b>."
        ),
        para(
            "A Convolutional Neural Network (CNN) was trained from scratch to classify images as "
            "pneumonia-positive or pneumonia-negative, establishing a reproducible baseline. "
            "The model achieved a <b>ROC-AUC of 0.7676</b> on the held-out test set, demonstrating "
            "meaningful discriminative signal. However, pneumonia recall at the default 0.5 threshold "
            "was critically low (1%), motivating threshold calibration and, in the final report, "
            "transfer learning with pretrained backbones."
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
        Paragraph(
            "• <b>Radiologist scarcity</b> — In rural and resource-limited settings, skilled radiologist "
            "access is severely constrained.", bullet_style),
        Paragraph(
            "• <b>Human error and fatigue</b> — High patient loads and shift-based workflows "
            "introduce variability and diagnostic error.", bullet_style),
        Paragraph(
            "• <b>Delayed diagnosis</b> — Waiting for specialist availability delays antibiotic treatment, "
            "worsening patient outcomes and driving antibiotic overuse.", bullet_style),
        Spacer(1, 4),
        para(
            "Automated deep learning systems trained on large imaging datasets offer a scalable, "
            "consistent, and low-cost complement to radiologist review. Such systems serve as "
            "<b>clinical decision-support tools</b> — providing a rapid second opinion that flags "
            "high-risk cases for priority review, rather than replacing the clinician."
        ),
    ]

    # ── 3. Objectives ────────────────────────────────────────────────────────
    story += section("3", "Objectives")
    story += [
        para("The project aims to:"),
        Paragraph("1. <b>Accurately classify</b> chest X-ray images as pneumonia-positive or "
                  "pneumonia-negative using deep learning.", bullet_style),
        Paragraph("2. <b>Assist healthcare professionals</b> by providing a reliable, consistent "
                  "second opinion to reduce diagnostic errors.", bullet_style),
        Paragraph("3. <b>Improve efficiency</b> by enabling faster automated screening, "
                  "reducing radiologist burden.", bullet_style),
        Paragraph("4. <b>Enhance accessibility</b> by building a scalable solution deployable in "
                  "hospitals, clinics, and rural health centers.", bullet_style),
        Paragraph("5. <b>Support global health</b> by contributing to early detection, lowering "
                  "pneumonia-related mortality, and reducing unnecessary antibiotic prescription.", bullet_style),
    ]

    # ── 4. Dataset Description ───────────────────────────────────────────────
    story += section("4", "Dataset Description")
    story += [
        para(
            "<b>Source:</b> RSNA Pneumonia Detection Challenge (Kaggle). The dataset consists of "
            "chest X-ray images stored in <b>DICOM format</b> (.dcm), the medical imaging standard "
            "embedding both patient metadata and raw pixel arrays in a single file."
        ),
        subsection("4.1", "Label Structure"),
    ]
    label_tbl = [
        ["File", "Purpose"],
        ["stage_2_train_labels.csv",
         "Binary label per bounding box row (Target: 0 or 1). A patient may appear on\nmultiple rows if multiple opacity regions were annotated."],
        ["stage_2_detailed_class_info.csv",
         "Three-class label per patient (one row per patient)."],
    ]
    story += [tbl(label_tbl, [5.0*cm, CONTENT_W - 5.0*cm]), Spacer(1, 6)]

    story += [subsection("4.2", "Three-Class Taxonomy")]
    taxonomy = [
        ["Class", "Binary Target", "Meaning"],
        ["Normal", "0", "Healthy lungs"],
        ["No Lung Opacity / Not Normal", "0",
         "Chest abnormality present (e.g., cardiomegaly, pleural effusion)\nbut not pneumonia"],
        ["Lung Opacity", "1",
         "Pneumonia present — white/grey opacities visible in lung fields"],
    ]
    story += [
        tbl(taxonomy, [5.0*cm, 2.5*cm, CONTENT_W - 7.5*cm]),
        Spacer(1, 4),
        para(
            "<i>Note: The 'No Lung Opacity / Not Normal' class is the most diagnostically "
            "challenging — these images show real pathology that can visually resemble pneumonia, "
            "making the negative class heterogeneous and the classification boundary harder to learn.</i>",
        ),
    ]

    # ── 5. Data Overview ─────────────────────────────────────────────────────
    story += [PageBreak()] + section("5", "Data Overview")
    story += [subsection("5.1", "File Inventory")]
    inv = [
        ["Asset", "Details"],
        ["data/stage_2_train_images.zip", "26,684 training DICOM files (~3.5 GB)"],
        ["data/stage_2_test_images.zip", "3,000 test DICOM files (~380 MB)"],
        ["stage_2_train_labels.csv", "30,227 rows × 4 columns"],
        ["stage_2_detailed_class_info.csv", "30,227 rows × 2 columns"],
    ]
    story += [tbl(inv, [6.5*cm, CONTENT_W - 6.5*cm]), Spacer(1, 6)]

    story += [subsection("5.2", "DICOM Image Properties")]
    story += [
        para("Inspecting five sample images directly from the zip archive:"),
    ]
    dicom_tbl = [
        ["File", "dtype", "Shape", "Pixel Min", "Pixel Max"],
        ["Sample 1", "uint8", "(1024, 1024)", "0", "230"],
        ["Sample 2", "uint8", "(1024, 1024)", "0", "255"],
        ["Sample 3", "uint8", "(1024, 1024)", "0", "232"],
        ["Sample 4", "uint8", "(1024, 1024)", "0", "255"],
        ["Sample 5", "uint8", "(1024, 1024)", "0", "255"],
    ]
    story += [tbl(dicom_tbl), Spacer(1, 4)]
    story += [
        para(
            "All images are <b>1024×1024 pixel, single-channel (grayscale), uint8 arrays</b>. "
            "The varying maximum pixel value (230 vs. 255) confirms scanner-to-scanner intensity "
            "variation, making per-image normalization necessary."
        ),
    ]

    story += [subsection("5.3", "Key Data Observations")]
    obs = [
        ["Metric", "Value"],
        ["Training CSV rows", "30,227"],
        ["Unique training patients", "26,684"],
        ["Training DICOM files", "26,684"],
        ["Test DICOM files", "3,000"],
        ["Target=0 [No Pneumonia] — raw CSV", "20,672 (68.4%)"],
        ["Target=1 [Pneumonia]   — raw CSV", "9,555  (31.6%)"],
        ["Pneumonia patients (deduplicated)", "6,012  (22.5%)"],
    ]
    story += [tbl(obs, [8.0*cm, CONTENT_W - 8.0*cm]), Spacer(1, 4)]
    story += [
        para(
            "<b>Important finding — raw CSV inflates pneumonia count.</b> "
            "The CSV has 30,227 rows but only 26,684 unique patients. The extra 3,543 rows arise "
            "because pneumonia patients can have <b>multiple bounding box annotations</b> "
            "(one row per annotated opacity region). When deduplicated to patient level, "
            "the true pneumonia prevalence is <b>6,012 patients (22.5%)</b>, not 31.6% as the "
            "raw CSV implies. This makes the class imbalance more severe than initially apparent."
        ),
    ]

    # ── 6. Exploratory Data Analysis ─────────────────────────────────────────
    story += [PageBreak()] + section("6", "Exploratory Data Analysis")
    story += [subsection("6.1", "Patient-Level Class Distribution")]
    story += [
        para("After deduplicating to one row per patient:"),
    ]
    dist = [
        ["Class", "Patient Count", "% of Total"],
        ["No Lung Opacity / Not Normal", "11,821", "44.3%"],
        ["Normal", "8,851", "33.2%"],
        ["Lung Opacity (Pneumonia)", "6,012", "22.5%"],
        ["Total", "26,684", "100%"],
    ]
    story += [tbl(dist), Spacer(1, 6)]

    story += [subsection("6.2", "Class Imbalance Analysis")]
    imb = [
        ["Target", "Patients", "Percentage"],
        ["No Pneumonia (0)", "20,672", "77.5%"],
        ["Pneumonia (1)",    "6,012",  "22.5%"],
    ]
    story += [
        tbl(imb, [5.0*cm, 4.0*cm, CONTENT_W - 9.0*cm]),
        Spacer(1, 4),
        para(
            "The dataset has a <b>~3.4:1 ratio</b> of negative to positive patients. "
            "A naive classifier that always predicts 'no pneumonia' would achieve <b>77.5% accuracy</b> — "
            "highlighting why accuracy alone is a misleading metric for this task."
        ),
    ]

    # Class imbalance plot
    story += [
        Spacer(1, 6),
        img("class_imbalance.png", width=CONTENT_W * 0.75),
        Paragraph("Figure 1 — Patient-level class distribution", caption_style),
    ]

    # Sample images
    story += [
        subsection("6.3", "Sample X-Ray Images per Class"),
        img("sample_images_per_class.png", width=CONTENT_W),
        Paragraph(
            "Figure 2 — Representative chest X-rays. Left: Normal (clear lung fields). "
            "Centre: No Lung Opacity / Not Normal (other pathology). Right: Lung Opacity / Pneumonia "
            "(visible white opacities).",
            caption_style,
        ),
    ]

    story += [subsection("6.4", "Visual Observations")]
    story += [
        Paragraph("<b>Lung Opacity (Pneumonia — Target=1):</b>", bullet_style),
        Paragraph("• Visible patchy white/grey opacities in one or both lung fields.", bullet_style),
        Paragraph("• Opacities appear as unilateral consolidations in early-stage pneumonia.", bullet_style),
        Paragraph("• The affected lung field loses its typical dark, air-filled appearance.", bullet_style),
        Spacer(1, 4),
        Paragraph("<b>Normal (Target=0):</b>", bullet_style),
        Paragraph("• Clear, uniformly dark lung fields on both sides.", bullet_style),
        Paragraph("• Sharp diaphragm outline and well-defined costophrenic angles.", bullet_style),
        Spacer(1, 4),
        Paragraph("<b>No Lung Opacity / Not Normal (Target=0):</b>", bullet_style),
        Paragraph("• Enlarged cardiac silhouettes, blunted costophrenic angles, or diffuse haziness.", bullet_style),
        Paragraph("• Real abnormalities but not pneumonia — the primary source of potential false positives.", bullet_style),
    ]

    story += [subsection("6.5", "Pixel Statistics per Class")]
    story += [
        img("pixel_statistics_per_class.png", width=CONTENT_W),
        Paragraph(
            "Figure 3 — Mean pixel intensity and standard deviation per class. "
            "Pneumonia images tend to show slightly higher mean intensity due to opacity regions.",
            caption_style,
        ),
    ]

    story += [
        subsection("6.6", "Data Quality Notes"),
        Paragraph("• Some DICOM files lack the standard DICM header — <code>force=True</code> is required.", bullet_style),
        Paragraph("• The training zip contains an extra 26,684 <code>__MACOSX/</code> ghost entries "
                  "(macOS artifact) that must be filtered.", bullet_style),
        Paragraph("• Files use a directory-prefixed path inside the zip, requiring a lookup dictionary "
                  "rather than direct filename construction.", bullet_style),
    ]

    # ── 7. Data Preprocessing ────────────────────────────────────────────────
    story += [PageBreak()] + section("7", "Data Preprocessing")

    story += [
        subsection("7.1", "Image Extraction"),
        para(
            "Training DICOM files were extracted from the zip archive to <code>data/train_images/</code> "
            "(one-time operation, ~3.5 GB on disk). A guard condition prevents re-extraction on "
            "subsequent runs."
        ),
        subsection("7.2", "Patient-Level Deduplication"),
        para(
            "<code>stage_2_train_labels.csv</code> was deduplicated by <code>patientId</code> "
            "(keeping one row per patient) and merged with <code>stage_2_detailed_class_info.csv</code> "
            "to yield a clean patient-level dataframe with binary target and three-class label."
        ),
        subsection("7.3", "Train / Validation / Test Split"),
        para("Split strategy: <b>stratified, patient-level, 70/15/15</b>"),
    ]
    split = [
        ["Split", "Patients", "Pneumonia (Target=1)", "% Pneumonia"],
        ["Train",      "18,677", "4,208", "22.5%"],
        ["Validation",  "4,004",   "902", "22.5%"],
        ["Test",        "4,003",   "902", "22.5%"],
        ["Total",      "26,684", "6,012", "22.5%"],
    ]
    story += [
        tbl(split),
        Spacer(1, 4),
        para(
            "The stratified split preserved the 22.5% pneumonia rate identically across all three splits, "
            "ensuring no class distribution drift between train, validation, and test sets."
        ),
        subsection("7.4", "Preprocessing Pipeline"),
        para("Each DICOM image was processed through the following steps:"),
        Paragraph("1. Read DICOM → pixel_array (H×W, uint8, grayscale — no RGB conversion needed)", bullet_style),
        Paragraph("2. Cast to float32", bullet_style),
        Paragraph("3. Resize: 1024×1024 → 128×128 (bilinear interpolation via OpenCV)", bullet_style),
        Paragraph("4. Normalize: img / img.max() → pixel values in [0.0, 1.0]", bullet_style),
        Paragraph("5. Add channel dimension: (128, 128) → (128, 128, 1)", bullet_style),
        Spacer(1, 4),
        para(
            "<b>Note on grayscale:</b> DICOM chest X-rays are natively single-channel — no "
            "RGB-to-grayscale conversion is required. The channel dimension is added programmatically "
            "to satisfy the CNN's expected input shape."
        ),
        para(
            "<b>Note on normalization:</b> Per-image normalization (dividing by each image's own "
            "maximum) was chosen over global normalization because pixel intensity ranges vary "
            "across different X-ray scanners (maximum values observed between 230 and 255)."
        ),
    ]

    # Preprocessing before/after plot
    story += [
        img("preprocessing_before_after.png", width=CONTENT_W),
        Paragraph(
            "Figure 4 — Preprocessing pipeline: original 1024×1024 DICOM (left) → "
            "128×128 normalised grayscale (right).",
            caption_style,
        ),
    ]

    story += [
        subsection("7.5", "Normalization Verification"),
        para("Over 20 random training samples:"),
        Paragraph("Pixel min range : [0.00000, 0.07201]", code_style),
        Paragraph("Pixel max range : [1.00000, 1.00000]", code_style),
        Paragraph("All values in [0, 1] : PASS", code_style),
        Spacer(1, 4),
        para(
            "The non-zero minimum values (up to 0.072) reflect background noise / non-zero scanner "
            "baseline, confirming that per-image normalization correctly handles these variations "
            "without clipping."
        ),
        subsection("7.6", "Augmentation"),
        img("augmentation_demo.png", width=CONTENT_W),
        Paragraph(
            "Figure 5 — Data augmentation samples: random horizontal flip, slight rotation, "
            "and brightness jitter applied during training to improve generalization.",
            caption_style,
        ),
    ]

    # ── 8. Model Building ────────────────────────────────────────────────────
    story += [PageBreak()] + section("8", "Model Building — CNN from Scratch")
    story += [
        subsection("8.1", "Architecture"),
        para(
            "A three-block CNN was designed from scratch with progressive feature extraction, "
            "doubling the number of filters at each block:"
        ),
    ]
    arch = [
        ["Layer / Block", "Output Shape", "Details"],
        ["Input",                      "(128, 128, 1)", ""],
        ["Block 1 — Conv2D",           "(128, 128, 32)", "32 filters, 3×3, ReLU"],
        ["Block 1 — BatchNormalization","(128, 128, 32)", ""],
        ["Block 1 — MaxPooling2D",     "(64, 64, 32)",   "2×2"],
        ["Block 2 — Conv2D",           "(64, 64, 64)",   "64 filters, 3×3, ReLU"],
        ["Block 2 — BatchNormalization","(64, 64, 64)",  ""],
        ["Block 2 — MaxPooling2D",     "(32, 32, 64)",   "2×2"],
        ["Block 3 — Conv2D",           "(32, 32, 128)",  "128 filters, 3×3, ReLU"],
        ["Block 3 — BatchNormalization","(32, 32, 128)", ""],
        ["Block 3 — MaxPooling2D",     "(16, 16, 128)",  "2×2"],
        ["GlobalAveragePooling2D",     "(128,)",          "Spatial aggregation"],
        ["Dense",                      "(256,)",          "ReLU"],
        ["Dropout",                    "(256,)",          "rate = 0.5"],
        ["Dense (output)",             "(1,)",            "Sigmoid — P(pneumonia)"],
    ]
    story += [tbl(arch, [5.5*cm, 3.5*cm, CONTENT_W - 9.0*cm]), Spacer(1, 6)]

    params = [
        ["Component", "Parameters"],
        ["Trainable", "126,401 (493.75 KB)"],
        ["Non-trainable (BatchNorm)", "448 (1.75 KB)"],
        ["Total", "126,849 (495.50 KB)"],
    ]
    story += [tbl(params, [7.0*cm, CONTENT_W - 7.0*cm]), Spacer(1, 6)]

    story += [
        para("<b>Design choices:</b>"),
        Paragraph("• <b>BatchNormalization</b> after each convolution stabilises training and reduces "
                  "sensitivity to learning rate.", bullet_style),
        Paragraph("• <b>GlobalAveragePooling2D</b> instead of Flatten reduces the parameter count "
                  "in the dense head and provides implicit spatial regularization.", bullet_style),
        Paragraph("• <b>Dropout(0.5)</b> in the dense head prevents co-adaptation of neurons "
                  "and reduces overfitting on an 18,677-sample training set.", bullet_style),
        Paragraph("• <b>Sigmoid output</b> with binary cross-entropy loss is appropriate for "
                  "binary classification.", bullet_style),
        subsection("8.2", "Class Weights"),
        para(
            "To compensate for the 3.4:1 class imbalance, balanced class weights were computed "
            "using <code>sklearn.utils.class_weight.compute_class_weight</code>:"
        ),
    ]
    cw = [
        ["Class", "Weight"],
        ["No Pneumonia (0)", "0.6454"],
        ["Pneumonia (1)",    "2.2192"],
    ]
    story += [
        tbl(cw, [6.0*cm, CONTENT_W - 6.0*cm]),
        Spacer(1, 4),
        para(
            "The model penalises missed pneumonia cases <b>~3.4× more heavily</b> than missed "
            "negative cases during training."
        ),
        subsection("8.3", "Training Configuration"),
    ]
    cfg = [
        ["Hyperparameter", "Value"],
        ["Optimizer",       "Adam (lr = 1e-3)"],
        ["Loss",            "Binary Cross-Entropy"],
        ["Metrics",         "Accuracy, AUC-ROC"],
        ["Batch size",      "32"],
        ["Max epochs",      "15"],
        ["Early stopping",  "patience=3, monitor=val_auc"],
        ["Checkpoint",      "Best val_auc saved to best_cnn_model.keras"],
        ["Hardware",        "Apple M1 GPU (TensorFlow Metal)"],
    ]
    story += [tbl(cfg, [5.0*cm, CONTENT_W - 5.0*cm])]

    # ── 9. Model Performance ─────────────────────────────────────────────────
    story += [PageBreak()] + section("9", "Model Performance &amp; Evaluation")

    story += [subsection("9.1", "Training History")]
    hist = [
        ["Epoch", "Train Acc", "Train AUC", "Val Acc", "Val AUC", "Val Loss", "Notes"],
        ["1", "0.649", "0.692", "0.225", "0.682", "2.624", ""],
        ["2", "0.680", "0.735", "0.762", "0.689", "0.504", ""],
        ["3", "0.691", "0.764", "0.774", "0.762", "0.590", "★ Best"],
        ["4", "0.704", "0.776", "0.770", "0.742", "0.512", ""],
        ["5", "0.713", "0.784", "0.775", "0.499", "4.261", "Val AUC collapses"],
        ["6", "0.709", "0.783", "0.540", "0.652", "0.715", "Early stop"],
    ]
    ht = Table(hist, repeatRows=1)
    ht.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND",   (0, 4), (-1, 4), colors.HexColor("#d4e8c2")),
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#edf3fa")]),
        ("BACKGROUND",   (0, 4), (-1, 4), colors.HexColor("#d4e8c2")),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story += [ht, Spacer(1, 4)]
    story += [
        para("Best weights from Epoch 3 restored by early stopping (highlighted in green)."),
        Paragraph("• Train AUC improved steadily from 0.692 → 0.784 across 6 epochs.", bullet_style),
        Paragraph("• Val AUC peaked at <b>0.762</b> in Epoch 3, then became unstable — likely "
                  "reflecting high learning rate sensitivity and limited model capacity at 128×128.", bullet_style),
        Paragraph("• Each epoch took approximately <b>110–120 seconds</b> on Apple M1 GPU "
                  "via TensorFlow Metal.", bullet_style),
    ]

    # Training history plot
    story += [
        Spacer(1, 6),
        img("training_history.png", width=CONTENT_W),
        Paragraph("Figure 6 — Training and validation accuracy / AUC across epochs.", caption_style),
    ]

    story += [subsection("9.2", "Test Set Classification Report")]
    story += [
        para("<b>Test set: 4,003 patients | 902 pneumonia (22.5%) | 3,101 no pneumonia (77.5%)</b>"),
    ]
    cr = [
        ["Class", "Precision", "Recall", "F1-Score", "Support"],
        ["No Pneumonia (0)", "0.78", "1.00", "0.87", "3,101"],
        ["Pneumonia (1)",    "0.69", "0.01", "0.02",   "902"],
        ["Accuracy",        "",     "",     "0.78",  "4,003"],
        ["Macro avg",       "0.73", "0.50", "0.45",  "4,003"],
        ["Weighted avg",    "0.76", "0.78", "0.68",  "4,003"],
    ]
    story += [tbl(cr), Spacer(1, 4)]

    story += [subsection("9.3", "Metric Summary")]
    ms = [
        ["Metric", "Value", "Interpretation"],
        ["Overall Accuracy",    "78%",    "Misleading — model largely predicts negative"],
        ["Pneumonia Precision", "0.69",   "69% of predicted positives are correct"],
        ["Pneumonia Recall",    "0.01",   "Only 1% of actual pneumonia cases detected — critical failure"],
        ["Pneumonia F1",        "0.02",   "Near-zero clinical utility at threshold=0.5"],
        ["ROC-AUC",             "0.7676", "Model has real discriminative signal (above random 0.5)"],
        ["Positive predictions","13 / 4,003", "Model defaults almost entirely to negative"],
    ]
    story += [tbl(ms, [4.5*cm, 2.0*cm, CONTENT_W - 6.5*cm]), Spacer(1, 4)]
    story += [
        para(
            "The model missed <b>~889 out of 902 pneumonia patients</b> at threshold=0.5 — "
            "a false negative rate of ~99%. However, the ROC-AUC of 0.7676 confirms the model "
            "does rank pneumonia cases above non-pneumonia cases; the issue is the decision "
            "threshold, not the learned representations."
        ),
    ]

    # Evaluation plots
    story += [
        Spacer(1, 6),
        img("evaluation_plots.png", width=CONTENT_W),
        Paragraph(
            "Figure 7 — Evaluation plots: ROC curve (AUC=0.7676), confusion matrix at threshold=0.5, "
            "and precision-recall curve.",
            caption_style,
        ),
    ]

    # PR curve
    story += [
        img("pr_curve_and_threshold.png", width=CONTENT_W),
        Paragraph(
            "Figure 8 — Precision-Recall curve and threshold analysis. "
            "A threshold of ~0.25–0.35 recovers substantially more recall at manageable precision.",
            caption_style,
        ),
    ]

    # Misclassified
    story += [
        img("misclassified_samples.png", width=CONTENT_W),
        Paragraph(
            "Figure 9 — Misclassified samples. False negatives (top) tend to show subtle or "
            "early-stage opacities. False positives (bottom) often come from the "
            "'No Lung Opacity / Not Normal' sub-class.",
            caption_style,
        ),
    ]

    # ── 10. Key Findings & Business Implications ──────────────────────────────
    story += [PageBreak()] + section("10", "Key Findings &amp; Business Implications")

    story += [subsection("10.1", "Technical Findings")]
    story += [
        Paragraph(
            "1. <b>True pneumonia prevalence (22.5%) is lower than the raw CSV implies (31.6%).</b> "
            "The label file contains per-bounding-box rows, not per-patient rows. "
            "Deduplication before splitting is essential to avoid biased class ratios.", bullet_style),
        Paragraph(
            "2. <b>ROC-AUC of 0.77 confirms the model learns real signal.</b> "
            "Despite near-zero recall at threshold=0.5, the model correctly ranks many pneumonia "
            "cases above non-pneumonia cases — the issue is the threshold, not the representations.", bullet_style),
        Paragraph(
            "3. <b>The 0.5 threshold is inappropriate for imbalanced medical classification.</b> "
            "A lower threshold (0.2–0.3) would recover substantially more recall at the cost of "
            "precision — an acceptable trade-off in a screening context where false negatives are "
            "far more costly than false positives.", bullet_style),
        Paragraph(
            "4. <b>128×128 resolution loses critical radiological texture.</b> "
            "Downsampling from 1024×1024 to 128×128 (64× fewer pixels) removes fine-grained "
            "opacity patterns. The 224×224 resolution used by standard pretrained backbones "
            "will capture significantly more detail.", bullet_style),
        Paragraph(
            "5. <b>'No Lung Opacity / Not Normal' is the hardest negative sub-class.</b> "
            "At 44.3% of all patients, this class contains real chest abnormalities that can "
            "resemble pneumonia visually, making it the primary driver of false positives.", bullet_style),
    ]

    story += [subsection("10.2", "Business Implications")]
    bi = [
        ["Finding", "Business Impact"],
        ["1% pneumonia recall at threshold=0.5",
         "Not deployable as-is — would miss 99% of cases, offering no clinical value"],
        ["ROC-AUC of 0.77",
         "Meaningful baseline — validates the pipeline and benchmarks against transfer learning"],
        ["Runs on consumer hardware (M1 Mac)",
         "Low infrastructure cost; viable for edge deployment in resource-constrained settings"],
        ["~2 minutes per training epoch on M1",
         "Full retraining feasible overnight; fast iteration cycle for fine-tuning"],
        ["Consistent 22.5% stratified splits",
         "Reliable evaluation framework — performance numbers are reproducible and unbiased"],
    ]
    story += [
        tbl(bi, [5.5*cm, CONTENT_W - 5.5*cm]),
        Spacer(1, 4),
        para(
            "<b>Recommended threshold for screening use:</b> ROC curve analysis suggests that a "
            "threshold of approximately <b>0.25–0.35</b> would balance recall with a manageable "
            "false positive rate — a decision that should be made with clinical stakeholders, "
            "not purely on statistical grounds."
        ),
    ]

    # ── 11. Limitations & Future Work ────────────────────────────────────────
    story += section("11", "Limitations &amp; Future Work")

    story += [subsection("11.1", "Current Limitations")]
    story += [
        Paragraph("• <b>128×128 input resolution</b> discards most radiological detail present "
                  "in the original 1024×1024 DICOM images.", bullet_style),
        Paragraph("• <b>CNN from scratch</b> (126K parameters) has insufficient capacity to learn "
                  "complex hierarchical features without pre-trained weights.", bullet_style),
        Paragraph("• <b>No threshold calibration</b> was performed — recall at the default "
                  "threshold is clinically unacceptable.", bullet_style),
        Paragraph("• <b>No data augmentation</b> was applied during training.", bullet_style),
    ]

    story += [subsection("11.2", "Planned for Final Report")]
    fw = [
        ["Task", "Approach"],
        ["Transfer learning (≥2 models)",
         "VGG16, ResNet50, EfficientNetB0 with 224×224 input; freeze backbone → train head → "
         "unfreeze last N layers"],
        ["Custom architectures",
         "Add attention layers and custom classification heads on pretrained backbones"],
        ["Threshold calibration",
         "Plot precision-recall curve; select threshold maximising F1 or recall at acceptable precision"],
        ["Model comparison",
         "Side-by-side AUC, recall, precision, F1 table for all models"],
        ["Best model serialization",
         "Save in .keras format; reload and run inference on sample images"],
        ["Web application",
         "Streamlit/Gradio app: upload DICOM or PNG → predicted class + probability"],
        ["Containerisation",
         "Docker image with model + app; docker run -p 8501:8501"],
        ["Deployment",
         "Hugging Face Spaces (Gradio)"],
    ]
    story += [tbl(fw, [4.5*cm, CONTENT_W - 4.5*cm])]

    # ── 12. Conclusion ────────────────────────────────────────────────────────
    story += section("12", "Conclusion")
    story += [
        para(
            "This interim report establishes a complete, reproducible deep learning pipeline for "
            "automated pneumonia detection from chest X-ray images:"
        ),
        Paragraph("• <b>Data ingestion</b> from DICOM zip archives with handling of dataset-specific "
                  "quirks (missing DICM headers, macOS ghost files, per-bounding-box duplicate rows).", bullet_style),
        Paragraph("• <b>EDA</b> revealing the true class distribution (22.5% pneumonia at patient "
                  "level, not 31.6% as the raw CSV implies) and the visual characteristics that "
                  "distinguish each class.", bullet_style),
        Paragraph("• <b>Preprocessing</b> producing stratified 70/15/15 patient-level splits with "
                  "verified [0,1] normalization.", bullet_style),
        Paragraph("• <b>Baseline CNN</b> achieving ROC-AUC 0.7676 — a meaningful signal above "
                  "random, confirming that deep learning can discriminate pneumonia from "
                  "non-pneumonia in this dataset.", bullet_style),
        Spacer(1, 6),
        para(
            "The baseline model is a deliberately lightweight starting point. Its limitations — "
            "particularly the 1% pneumonia recall at the default threshold — motivate the transfer "
            "learning approach in the final report, where pretrained backbones are expected to push "
            "AUC above 0.85 and deliver clinically meaningful recall, bringing the system closer to "
            "its goal of serving as a reliable automated decision-support tool for pneumonia diagnosis."
        ),
        Spacer(1, 8),
        rule(),
        Spacer(1, 4),
        para(
            "<i>Notebook: <code>src/pneumonia_interim.ipynb</code> | "
            "Best model checkpoint: <code>src/best_cnn_model.keras</code></i>"
        ),
    ]

    # Build
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF saved → {OUT}")


if __name__ == "__main__":
    build()
