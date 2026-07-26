#!/usr/bin/env python3
"""
inference.py — Run pneumonia classification on a DICOM chest X-ray.

Usage:
    python inference.py path/to/patient.dcm
    python inference.py path/to/patient.dcm --threshold 0.35
    python inference.py path/to/patient.dcm --model my_model.joblib

The model file (best_model_pipeline.joblib) must be in the same directory
or specified via --model. It is a scikit-learn Pipeline produced by the
pneumonia_ml.ipynb notebook and saved with joblib.dump().
"""
import sys
import argparse
import numpy as np
import cv2
import pydicom
import joblib

FEATURE_IMG_SIZE = (64, 64)  # must match the size used during training
DEFAULT_MODEL    = "best_model_pipeline.joblib"
DEFAULT_THRESHOLD = 0.35     # lower than 0.5 to favour recall in screening


def extract_features(dcm_path: str) -> np.ndarray:
    """Load a DICOM file and return a flat feature vector (4101,).

    Features: 4096 pixel values (64×64, normalised) + 5 global statistics
    (mean, std, p25, p50, p75). Must be identical to training extraction.
    """
    dcm = pydicom.dcmread(dcm_path, force=True)
    img = dcm.pixel_array.astype(np.float32)
    img = cv2.resize(img, FEATURE_IMG_SIZE)
    mx  = img.max()
    if mx > 0:
        img = img / mx
    pixels = img.flatten()
    stats  = np.array([
        pixels.mean(),
        pixels.std(),
        np.percentile(pixels, 25),
        np.percentile(pixels, 50),
        np.percentile(pixels, 75),
    ])
    return np.concatenate([pixels, stats])


def predict(dcm_path: str, model_path: str, threshold: float) -> dict:
    """Return a prediction dict for one DICOM file."""
    pipeline = joblib.load(model_path)
    features = extract_features(dcm_path).reshape(1, -1)
    prob     = pipeline.predict_proba(features)[0][1]
    label    = "PNEUMONIA" if prob >= threshold else "NORMAL"
    return {
        "file":       dcm_path,
        "prob":       float(prob),
        "threshold":  threshold,
        "prediction": label,
        "model":      model_path,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Pneumonia detection from a DICOM chest X-ray (joblib model)"
    )
    parser.add_argument("dicom_path", help="Path to a .dcm file")
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"Decision threshold for positive class (default {DEFAULT_THRESHOLD}; "
             "lower = more sensitive, higher = more specific)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Path to joblib pipeline file (default: {DEFAULT_MODEL})"
    )
    args = parser.parse_args()

    result = predict(args.dicom_path, args.model, args.threshold)

    print()
    print("=" * 45)
    print("  PNEUMONIA DETECTION — INFERENCE RESULT")
    print("=" * 45)
    print(f"  File       : {result['file']}")
    print(f"  Model      : {result['model']}")
    print(f"  Prob       : {result['prob']:.4f}  ({result['prob']*100:.1f}%)")
    print(f"  Threshold  : {result['threshold']}")
    print(f"  Prediction : {result['prediction']}")
    print("=" * 45)
    print()
    return 0 if result["prediction"] == "NORMAL" else 1


if __name__ == "__main__":
    sys.exit(main())
