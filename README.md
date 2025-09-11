# Welder Monitoring Dashboard

Sistem **Welder Monitoring Dashboard** adalah aplikasi berbasis web untuk memantau aktivitas, performa, dan profil welder (tukang las) secara real-time. Dashboard ini menampilkan data sensor, prediksi aktivitas, distribusi aktivitas, serta profil lengkap welder untuk mendukung pengawasan dan pengambilan keputusan di lingkungan kerja.

## Fitur Utama

- Dashboard real-time
- Profil welder
- Prediksi aktivitas
- API backend (Django REST Framework)
- Support Progressive Web App (PWA)
- Bisa dijalankan cukup klik 2x (run_dashboard.exe)

## Struktur Proyek

```
web_app/
├── venv310/                # Virtual environment (Python 3.10)
└── welder_monitoring/
    ├── welder_dashboard/
    │   ├── dashboard/
    │   │   ├── static/
    │   │   │   ├── manifest.json
    │   │   │   ├── service-worker.js
    │   │   │   └── icons/
    │   │   └── templates/
    │   │       └── dashboard/
    │   ├── manage.py
    │   └── ...
    ├── run_dashboard.py
    └── requirements.txt
```

## Cara Instalasi & Menjalankan Aplikasi

### 1. Clone Repository

```sh
git clone https://github.com/username/welder_monitoring.git
cd welder_monitoring
```

### 2. Buat Virtual Environment (Python 3.10)

```sh
cd .. # ke folder web_app
python -m venv venv310
```

### 3. Aktifkan Virtual Environment

- **Windows:**
  ```sh
  venv310\Scripts\activate
  ```
- **Linux/MacOS:**
  ```sh
  source venv310/bin/activate
  ```

### 4. Install Dependencies

```sh
cd welder_monitoring
pip install -r requirements.txt
```

### 5. Build File Otomatis (run_dashboard.exe) dengan PyInstaller

```sh
pip install pyinstaller
pyinstaller --onefile run_dashboard.py
```

- Hasilnya ada di folder `dist/run_dashboard.exe`

### 6. Jalankan Aplikasi

- Cukup klik 2x `dist/run_dashboard.exe` untuk menjalankan server Django.
- Server akan berjalan di `http://localhost:8000/`

### 7. Install PWA di Browser

- Buka `http://localhost:8000/` di Chrome/Edge.
- Klik tombol "Install App" di pojok kanan bawah atau ikon install di address bar.
- Setelah terinstall, aplikasi bisa dibuka dari desktop/start menu seperti aplikasi native.

### 8. Penggunaan Selanjutnya

- Untuk menjalankan aplikasi, cukup klik 2x `run_dashboard.exe` lalu buka aplikasi PWA dari desktop/start menu.
- Tidak perlu buka terminal lagi.

## Catatan Penting

- Pastikan folder `venv310` ada di `web_app` (bukan di dalam folder proyek).
- Jika ingin rebuild exe, hapus folder `build/` dan `dist/` lalu ulangi langkah PyInstaller.
- Jika ada error path, pastikan struktur folder sesuai contoh di atas.

---

**Selamat menggunakan Welder Monitoring Dashboard!**