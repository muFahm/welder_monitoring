import numpy as np
import tensorflow as tf
import json
from pathlib import Path
from .preprocess import get_latest_window_data

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

def predict_latest_activity():
    data = get_latest_window_data()
    if data is None:
        return None  # Data belum cukup

    # Lakukan prediksi
    pred_proba = model.predict(data)
    pred_label_idx = np.argmax(pred_proba, axis=1)[0]
    pred_label_name = idx_to_label[pred_label_idx]

    return pred_label_name
