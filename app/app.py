"""
Pneumonia Detection — Streamlit App
Upload a chest X-ray (DICOM, PNG, or JPG) to get a pneumonia prediction.
"""
import io
import os

import cv2
import numpy as np
import pydicom
import streamlit as st
import tensorflow as tf
from huggingface_hub import hf_hub_download
from PIL import Image

# ── Constants ─────────────────────────────────────────────────────────────────
# Local model first (Docker image / dev checkout); falls back to downloading
# from the Hugging Face Model Hub (public repo, no token needed) — this is how
# Streamlit Community Cloud gets the model, since it only clones the git repo.
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "best_final_model.keras"),
)
MODEL_REPO = os.environ.get("MODEL_REPO", "dvsreddy/pneumonia-detection-model")
MODEL_FILENAME = "best_final_model.keras"
DEFAULT_THRESHOLD = 0.35

st.set_page_config(
    page_title="Pneumonia Detection",
    page_icon="🫁",
    layout="centered",
)


# ── Model loader (cached across sessions) ─────────────────────────────────────
@st.cache_resource(show_spinner="Loading model…")
def load_model(path: str) -> tf.keras.Model:
    if not os.path.exists(path):
        path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILENAME)
    return tf.keras.models.load_model(path)


# ── Image preprocessing ───────────────────────────────────────────────────────
def preprocess(img_array: np.ndarray, input_size: int, three_channel: bool) -> np.ndarray:
    """Match each model family's training contract.

    Transfer models (3-channel input) are self-contained: input rescaling lives
    inside the saved graph, so they expect raw pixels in [0, 255].
    The scratch CNN (1-channel input) was trained on per-image max-normalised
    images in [0, 1]. Scaling by the image max also handles 16-bit DICOMs.
    """
    img = cv2.resize(img_array.astype(np.float32), (input_size, input_size))
    mx = img.max()
    if three_channel:
        if mx > 0:
            img = img / mx * 255.0
        return np.repeat(img[..., np.newaxis], 3, axis=-1)
    if mx > 0:
        img = img / mx
    return img[..., np.newaxis]


def read_uploaded_file(uploaded_file) -> np.ndarray:
    raw = uploaded_file.read()
    if uploaded_file.name.lower().endswith(".dcm"):
        dcm = pydicom.dcmread(io.BytesIO(raw), force=True)
        return dcm.pixel_array.astype(np.float32)
    pil = Image.open(io.BytesIO(raw)).convert("L")
    return np.array(pil, dtype=np.float32)


# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🫁 Pneumonia Detection")
st.markdown(
    "Upload a chest X-ray image to detect pneumonia. "
    "Supported formats: **DICOM (.dcm)**, **PNG**, **JPG**."
)
st.divider()

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    threshold = st.slider(
        "Decision threshold",
        min_value=0.10,
        max_value=0.90,
        value=DEFAULT_THRESHOLD,
        step=0.05,
        help=(
            "Lower = more sensitive (fewer missed cases, more false alarms). "
            "Recommended for screening: 0.30–0.40."
        ),
    )
    st.caption(f"Model path: `{MODEL_PATH}`")

uploaded = st.file_uploader(
    "Upload chest X-ray",
    type=["dcm", "png", "jpg", "jpeg"],
    label_visibility="collapsed",
)

if uploaded is not None:
    # Load and display the raw image
    try:
        raw_img = read_uploaded_file(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()

    col_img, col_info = st.columns([1, 1])

    with col_img:
        display_img = (raw_img / raw_img.max() * 255).astype(np.uint8) if raw_img.max() > 0 else raw_img
        st.image(display_img, caption="Uploaded X-ray", use_container_width=True, clamp=True)

    # Load model and run inference (local file, else Hugging Face Model Hub)
    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        st.error(
            f"Could not load the model locally (`{MODEL_PATH}`) or from "
            f"`{MODEL_REPO}` on the Hugging Face Hub: {e}"
        )
        st.stop()
    input_size = model.input_shape[1]
    three_channel = model.input_shape[-1] == 3

    processed = preprocess(raw_img, input_size, three_channel)
    prob = float(model.predict(processed[np.newaxis, ...], verbose=0)[0][0])
    label = "PNEUMONIA" if prob >= threshold else "NORMAL"
    is_positive = label == "PNEUMONIA"

    with col_info:
        st.subheader("Result")

        if is_positive:
            st.error(f"**{label}**", icon="⚠️")
        else:
            st.success(f"**{label}**", icon="✅")

        st.metric("Confidence", f"{prob * 100:.1f}%")
        st.metric("Threshold used", f"{threshold:.2f}")
        st.progress(prob)

        st.caption(
            f"Model input: {input_size}×{input_size}×{'3' if three_channel else '1'}"
        )

    st.divider()
    st.info(
        "**Clinical note**: This tool is intended as a decision-support aid only. "
        "All results must be reviewed and confirmed by a qualified radiologist before clinical use.",
        icon="ℹ️",
    )

else:
    st.markdown(
        """
### How it works

1. **Upload** a chest X-ray (DICOM, PNG, or JPG)
2. The image is resized, normalized, and passed through a deep learning model
3. The model outputs the probability that pneumonia is present
4. A **threshold** (default 0.35) converts the probability to a binary prediction

### About the model

The deployed model is a fine-tuned CNN trained on the **RSNA Pneumonia Detection Challenge** dataset (26,684 chest X-rays). Transfer learning from ImageNet pretrained weights (ResNet50V2 or EfficientNetB0) is used to boost performance on the relatively small labelled medical imaging dataset.

| Metric | Value |
|--------|-------|
| Dataset | RSNA Pneumonia Detection Challenge |
| Training samples | 18,677 patients |
| Positive prevalence | 22.5% (pneumonia) |
| Primary metric | ROC-AUC |
"""
    )
