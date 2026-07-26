#!/usr/bin/env bash
# deploy_hf.sh — Publish the trained model to the Hugging Face Model Hub.
#
# Note: HF Docker/Gradio Spaces now require a PRO subscription, so the app is
# hosted on Streamlit Community Cloud instead (auto-deploys from GitHub).
# Only the model artifact lives on Hugging Face — in a free public model repo.
#
# Prerequisites:
#   pip install huggingface_hub
#   Trained model saved as best_final_model.keras (run src/pneumonia_final.ipynb)
#
# Usage:
#   source .env && bash deploy_hf.sh

set -euo pipefail

: "${HF_TOKEN:?HF_TOKEN not set — source .env first}"
: "${HF_USERNAME:?HF_USERNAME not set — source .env first}"

MODEL_REPO="${HF_USERNAME}/pneumonia-detection-model"

echo "==> Publishing model to Hugging Face Model Hub: ${MODEL_REPO}"

python - <<PYTHON
from huggingface_hub import HfApi
import os, sys

api  = HfApi(token=os.environ["HF_TOKEN"])
repo = os.environ["HF_USERNAME"] + "/pneumonia-detection-model"

api.create_repo(repo_id=repo, repo_type="model", private=False, exist_ok=True)
print(f"Model repo ready: https://huggingface.co/{repo}")

if not os.path.exists("best_final_model.keras"):
    sys.exit("best_final_model.keras not found — run src/pneumonia_final.ipynb first.")

api.upload_file(
    path_or_fileobj="best_final_model.keras",
    path_in_repo="best_final_model.keras",
    repo_id=repo, repo_type="model",
)
print("Uploaded: best_final_model.keras")
print(f"\nDone. The Streamlit app downloads the model from {repo} at startup.")
PYTHON
