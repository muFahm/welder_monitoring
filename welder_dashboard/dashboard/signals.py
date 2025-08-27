from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.models import SensorRecord
from dashboard.prediction_pipeline.predict import predict_latest_activity

@receiver(post_save, sender=SensorRecord)
def run_prediction_on_new_record(sender, instance, created, **kwargs):
    if not created:
        return  # Hanya proses kalau record baru dibuat

    # Cek apakah sudah ada 25 record terbaru → kalau ya, lakukan prediksi
    result = predict_latest_activity()
    if result:
        print(f"[Prediction] New prediction saved: {result}")
