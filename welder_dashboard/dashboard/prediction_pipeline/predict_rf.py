import numpy as np
import json
from pathlib import Path
from .preprocess import get_latest_window_data
from django.utils.timezone import now
from dashboard.models import PredictionResult
import logging
import joblib

logger = logging.getLogger(__name__)

# Load model saat modul ini pertama kali diimpor (efisien)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'prediction_pipeline' / 'dny_1G.pkl'
LABEL_PATH = BASE_DIR / 'prediction_pipeline' / 'label_mapping.json'

logger.info(f"Loading Random Forest model from: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)
logger.info("Model loaded successfully.")

# Load label mapping
with open(LABEL_PATH) as f:
    label_mapping = json.load(f)
logger.info(f"Label mapping loaded: {label_mapping}")

# Mapping indeks ke label nama
idx_to_label = {int(k): v for k, v in label_mapping.items()}
logger.info(f"Index to label mapping: {idx_to_label}")


def predict_latest_activity(welder_id=None):
    logger.info("Running predict_latest_activity()...")

    try:
        data, records = get_latest_window_data()
        logger.info(f"Data shape: {None if data is None else data.shape}")
        logger.info(f"Records count: {0 if records is None else len(records)}")

        if data is None:
            logger.warning("Not enough data for prediction.")
            return None

        # RandomForest expects 2D input [n_samples, n_features]
        # -> data sekarang (1, window_size, 9), jadi flatten ke (1, n_features)
        features = data.reshape(1, -1)

        # Gunakan predict_proba supaya dapat confidence
        pred_proba = model.predict_proba(features)
        logger.info(f"Prediction probabilities: {pred_proba}")

        pred_label_idx = int(np.argmax(pred_proba, axis=1)[0])
        pred_label_name = idx_to_label[pred_label_idx]
        confidence = float(pred_proba[0][pred_label_idx])

        logger.info(f"Predicted: {pred_label_name} with confidence {confidence}")

        # Ambil rentang waktu window dari data sensor
        window_start = records[0].timestamp
        window_end = records[-1].timestamp

        # Simpan hasil prediksi ke DB
        result = PredictionResult.objects.create(
            predicted_class=pred_label_name,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end
        )

        logger.info(f"Saved PredictionResult with id {result.id}")

        return pred_label_name

    except Exception as e:
        logger.exception(f"Error in predict_latest_activity: {e}")
        raise
