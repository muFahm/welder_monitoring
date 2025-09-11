import os
import sys
import subprocess

# Deteksi lokasi file ini (baik .py maupun .exe hasil PyInstaller)
if getattr(sys, 'frozen', False):
    # Jika dibundle, ambil folder dist, lalu naik satu ke welder_monitoring
    BASE_DIR = os.path.dirname(sys.executable)
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
else:
    # Jika dijalankan dari source
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# venv310 ada di web_app
VENV_PYTHON = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'venv310', 'Scripts', 'python.exe'))
MANAGE_PY = os.path.abspath(os.path.join(PROJECT_ROOT, 'welder_dashboard', 'manage.py'))

if not os.path.exists(VENV_PYTHON):
    print(f'Virtual environment tidak ditemukan di: {VENV_PYTHON}')
    print('Silakan pastikan venv310 sudah dibuat di lokasi yang benar.')
    input('Tekan Enter untuk keluar...')
    sys.exit(1)

if not os.path.exists(MANAGE_PY):
    print(f'manage.py tidak ditemukan di: {MANAGE_PY}')
    print('Silakan pastikan struktur folder sudah benar.')
    input('Tekan Enter untuk keluar...')
    sys.exit(1)

try:
    subprocess.run([VENV_PYTHON, MANAGE_PY, 'runserver'], check=True)
except KeyboardInterrupt:
    print('Server dihentikan.')
except Exception as e:
    print(f'Gagal menjalankan server: {e}')
    input('Tekan Enter untuk keluar...')
