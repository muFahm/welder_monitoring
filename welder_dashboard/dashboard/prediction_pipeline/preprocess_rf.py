import numpy as np
from dashboard.models import SensorRecord 
from django.utils.timezone import now

WINDOW_SIZE = 14  

def get_latest_window_data():
    # Ambil 14 data terakhir dari DB (urut dari paling baru ke lama, lalu dibalik)
    records = SensorRecord.objects.order_by('-timestamp')[:WINDOW_SIZE][::-1]

    if len(records) < WINDOW_SIZE:
        return None, None  # Belum cukup data untuk diprediksi

    # Susun data menjadi array [window_size, 9]
    data = np.array([[r.ax, r.ay, r.az, r.gx, r.gy, r.gz, r.mx, r.my, r.mz] for r in records], dtype=np.float32)

    # Bentuk ke (1, window_size, 9) karena CNN expects batch
    return data.reshape(1, -1), records
