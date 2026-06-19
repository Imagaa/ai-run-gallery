# 🚀 AI Run Gallery - Operational Manual

Ini adalah pusat komando untuk inisiasi, peluncuran, dan manajemen *event* lari. Jangan ubah *source code* jika Anda hanya ingin membuat *event* baru. Cukup gunakan `.env`!

## ⚙️ 1. Persiapan Event Baru (Konfigurasi Mutlak)
Setiap kali ada *event* lari baru, buat salinan `.env` dari template ini dan isi nilainya:
```env

# URL Database PostgreSQL dari Railway (Event Spesifik)
DATABASE_URL="postgresql://postgres:password@host.railway.app:port/railway"

# ID Folder GDrive utama yang berisi sub-folder foto acara
GDRIVE_FOLDER_ID="1A2B3C4D5E..."

# Batas akurasi pengenalan wajah (0.60 sangat ketat, 0.65 standar, 0.70 longgar)
FACE_MATCH_THRESHOLD=0.65


🛠️ 2. Zero-Touch Setup (Instalasi Laptop Lokal / Tenda)
Untuk menyalakan Local Watcher di laptop panitia tanpa pusing soal versi Python:

Pastikan Python 3.10+ terinstal di PC.

Klik ganda pada file setup_and_run.bat.

Skrip akan mendeteksi apakah PC Anda memiliki NVIDIA GPU, menginstal CUDA otomatis, dan merakit Virtual Environment.

Menu Komando akan muncul secara otomatis.

🕹️ 3. Pusat Komando CLI
Jika Anda sudah melewati Setup, jalankan aplikasi menggunakan perintah ini di Terminal VSCode / CMD:

Merakit Database Pertama Kali:

Bash
python run.py init-db
(Wajib dilakukan 1x untuk setiap database event baru agar ekstensi Vector tercipta).

Menyalakan Local Watcher (Tenda Panitia):

Bash
python run.py start-watcher
(Biarkan terminal ini terbuka selama acara berlangsung agar foto terus terindeks ke database).

Menyalakan API Publik (Cloud/Railway):

Bash
python run.py start-api
(Hanya digunakan untuk uji coba lokal atau saat start di dalam Docker Railway).

☁️ 4. Panduan Deploy ke Railway (Sniper API)
Program ini sudah siap di- deploy sebagai Layanan Mikro.

Buat Project Baru di Railway.

Tambahkan PostgreSQL (sebagai database).

Hubungkan ke repositori GitHub ini.

Di bagian Variables Railway, masukkan isi .env Anda.

Di bagian Settings > Build, pastikan menggunakan Nixpacks atau Dockerfile (jika ada).

Di bagian Settings > Start Command, isi dengan perintah mutlak ini:
uvicorn services.search_api.main:app_api --host 0.0.0.0 --port $PORT

🚦 5. Siklus Hidup Event (Flow End-to-End)
H-7: Deploy API ke Railway & buat Frontend Vercel. Set .env. Jalankan init-db.

Hari H (Pagi): Panitia lapangan menyalakan setup_and_run.bat dan menjalankan start-watcher.

Hari H (Siang - Puncak Traffic): Lakukan Scale-Up RAM Railway menjadi 4GB/8GB untuk menahan ribuan unggahan selfie pelari.

H+3: Turunkan spesifikasi (Scale-Down) RAM Railway ke batas minimal untuk menghemat biaya.