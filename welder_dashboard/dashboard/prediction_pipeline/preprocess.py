import numpy as np
from dashboard.models import SensorRecord  # sesuaikan dengan modelmu
from django.utils.timezone import now

WINDOW_SIZE = 25  # Sesuai model CNN-mu

def get_latest_window_data():
    # Ambil 25 data terakhir dari DB (urut dari paling baru ke lama, lalu dibalik)
    records = SensorRecord.objects.order_by('-timestamp')[:WINDOW_SIZE][::-1]

    if len(records) < WINDOW_SIZE:
        return None  # Belum cukup data untuk diprediksi

    # Susun data menjadi array [window_size, 9]
    data = np.array([[r.ax, r.ay, r.az, r.gx, r.gy, r.gz, r.mx, r.my, r.mz] for r in records], dtype=np.float32)

    # Bentuk ke (1, window_size, 9) karena CNN expects batch
    return data.reshape(1, WINDOW_SIZE, 9)
