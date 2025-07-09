import os, sys, django
import sys
import numpy as np
from unittest.mock import patch, MagicMock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "welder_dashboard.settings")
django.setup()

# Test ketika data cukup dan model berhasil memprediksi
@patch('dashboard.prediction_pipeline.predict.get_latest_window_data')
@patch('dashboard.prediction_pipeline.predict.model')
@patch('dashboard.prediction_pipeline.predict.idx_to_label', {
    0: "Grinding",
    1: "Others",
    2: "Preparation",
    3: "Slag Cleaning",
    4: "Welding"
})
def test_predict_latest_activity_valid(mock_model, mock_get_data):
    # Dummy input shape (1, 25, 9)
    dummy_input = np.random.rand(1, 25, 9).astype(np.float32)
    mock_get_data.return_value = dummy_input
    mock_model.predict.return_value = np.array([[0.05, 0.1, 0.05, 0.2, 0.6]])  # 0.6 -> index 4 -> Welding

    from dashboard.prediction_pipeline.predict import predict_latest_activity
    label = predict_latest_activity()

    assert isinstance(label, str)
    assert label == "Welding"

# Test versi dengan return_proba=True
@patch('dashboard.prediction_pipeline.predict.get_latest_window_data')
@patch('dashboard.prediction_pipeline.predict.model')
@patch('dashboard.prediction_pipeline.predict.idx_to_label', {
    0: "Grinding",
    1: "Others",
    2: "Preparation",
    3: "Slag Cleaning",
    4: "Welding"
})
def test_predict_latest_activity_with_confidence(mock_model, mock_get_data):
    dummy_input = np.random.rand(1, 25, 9).astype(np.float32)
    mock_get_data.return_value = dummy_input
    mock_model.predict.return_value = np.array([[0.01, 0.01, 0.02, 0.05, 0.91]])

    from dashboard.prediction_pipeline.predict import predict_latest_activity
    label, confidence = predict_latest_activity(return_proba=True)

    assert label == "Welding"
    assert isinstance(confidence, float)
    assert 0.0 <= confidence <= 1.0

# Test ketika data tidak cukup
@patch('dashboard.prediction_pipeline.predict.get_latest_window_data')
def test_predict_latest_activity_insufficient_data(mock_get_data):
    mock_get_data.return_value = None

    from dashboard.prediction_pipeline.predict import predict_latest_activity
    result = predict_latest_activity()

    assert result is None
