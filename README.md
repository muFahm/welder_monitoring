# Welder Monitoring Dashboard

Sistem **Welder Monitoring Dashboard** adalah aplikasi berbasis web yang digunakan untuk memantau aktivitas, performa, dan profil welder (tukang las) secara real-time. Dashboard ini menampilkan data sensor, prediksi aktivitas, distribusi aktivitas, serta profil lengkap welder untuk mendukung pengawasan dan pengambilan keputusan di lingkungan kerja.

## Fitur Utama

- **Dashboard Real-Time:** Menampilkan waktu, aktivitas terakhir, distribusi aktivitas, timeline, dan data sensor.
- **Profil Welder:** Informasi detail welder seperti nama, email, nomor telepon, keahlian, pengalaman, dan sertifikasi.
- **Prediksi Aktivitas:** Menggunakan pipeline prediksi untuk menampilkan aktivitas terbaru welder.
- **API:** Backend menggunakan Django REST Framework untuk menyediakan data ke frontend.

## Struktur Proyek

```
welder_monitoring/
├── welder_dashboard/
│   ├── dashboard/
│   │   ├── static/
│   │   │   └── js/
│   │   │       └── dashboard.js
│   │   ├── templates/
│   │   │   └── dashboard/
│   │   │       └── index.html
│   │   ├── views.py
│   │   ├── models.py
│   │   └── serializers.py
│   └── ...
├── requirements.txt
└── README.md
```

## Teknologi yang Digunakan

- **Python 3.x** (backend dan integrasi model)  
- **TensorFlow / scikit-learn** (klasifikasi aktivitas)  
- **Django/Flask** (backend web)  
- **WebSocket** untuk komunikasi real-time  
- **HTML, CSS, JavaScript** untuk dashboard frontend 

## Prasyarat

Sebelum menjalankan proyek, pastikan sudah menginstal:

- Python ≥ 3.8  
- `pip` (package manager Python)  
- Virtual Environment (`venv`)  
- Browser modern (Chrome/Firefox/Edge)  
- Hardware sensor (IMU GY-85, ESP32)

## Instalasi & Setup Lokal

### 1. Clone Repository

```sh
git clone https://github.com/username/welder_monitoring.git
cd welder_monitoring
```

### 2. Buat Virtual Environment

Disarankan menggunakan virtual environment agar dependensi terisolasi.

```sh
python -m venv venv
```

Aktifkan virtual environment:

- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Linux/MacOS:**
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Migrasi Database

```sh
python manage.py migrate
```

### 5. Jalankan Server

```sh
python manage.py runserver
```

Akses dashboard di [http://localhost:8000/](http://localhost:8000/).

## Kontribusi

Silakan fork repo ini dan buat pull request untuk kontribusi. Untuk bug atau saran, silakan buat issue di GitHub.

---