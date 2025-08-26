import numpy as np
import tensorflow as tf
import json
from pathlib import Path
from .preprocess import get_latest_window_data
from django.utils.timezone import now
from dashboard.models import PredictionResult

# Load model saat modul ini pertama kali diimpor (efisien)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'prediction_pipeline' / 'cnn1d_welder_model.h5'
LABEL_PATH = BASE_DIR / 'prediction_pipeline' / 'label_mapping.json'

model = tf.keras.models.load_model(MODEL_PATH)

# Load label mapping
with open(LABEL_PATH) as f:
    label_mapping = json.load(f)

# Mapping indeks ke label nama
idx_to_label = {int(k): v for k, v in label_mapping.items()}


def predict_latest_activity(welder_id=None):
    data = get_latest_window_data()
    if data is None:
        return None  # Data belum cukup

    pred_proba = model.predict(data)
    pred_label_idx = np.argmax(pred_proba, axis=1)[0]
    pred_label_name = idx_to_label[pred_label_idx]
    confidence = float(pred_proba[0][pred_label_idx])

    # Simpan ke DB jika ada sesi aktif
    from dashboard.views import active_sessions
    if welder_id and welder_id in active_sessions:
        session = active_sessions[welder_id]
        now_time = now()
        PredictionResult.objects.create(
            session=session,
            predicted_class=pred_label_name,
            confidence=confidence,
            window_start=now_time,
            window_end=now_time  # bisa kamu sesuaikan jika tahu durasi window
        )

    return pred_label_name
