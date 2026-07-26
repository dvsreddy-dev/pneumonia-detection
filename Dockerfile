FROM python:3.12-slim

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer-cached)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/app.py .

# Copy model — run src/pneumonia_final.ipynb first to train and save it.
# The build intentionally fails here if the model file is missing.
COPY best_final_model.keras .

# Hugging Face Spaces uses port 7860; local use 8501
ENV MODEL_PATH=/app/best_final_model.keras
EXPOSE 7860 8501

# Streamlit config: disable browser auto-open, bind to all interfaces
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
