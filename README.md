# 🚀 AI Run Gallery - Panduan Operasional Lapangan (0 to Running)

Buku panduan ini merangkum seluruh siklus hidup program AI Run Gallery Enterprise Edition. Dari komputer perawan (nol) hingga program berjalan dan mengindeks wajah pelari.

---

## 🛑 PRASYARAT WAJIB (Sebelum Memulai)
1. Komputer/Laptop memiliki sistem operasi Windows.
2. Terinstal **Python 3.10 atau lebih baru** (Pastikan opsi *"Add Python to PATH"* dicentang saat menginstal Python).
3. Akun Google Cloud (untuk akses Google Drive API).
4. Akun Railway (untuk PostgreSQL Database & Deployment API).

---

## 🗺️ PANDUAN LANGKAH DEMI LANGKAH (0 -> 100%)

### TAHAP 1: Menyiapkan Amunisi Cloud (Database & Google)
Sebelum menyentuh program, siapkan dua "Kunci" eksternal ini:
1. **Buat Database:** Buka Railway, buat project baru -> Provision PostgreSQL. Salin **Connection URL**-nya (Dimulai dengan `postgresql://...`).
2. **Siapkan Google Auth:** Jika Anda bertugas sebagai Watcher (penyedot foto), Anda wajib membuat file OAuth. Baca file `GOOGLE_SETUP.md` secara terpisah untuk panduan klik-demi-klik di Google Cloud Console. 
   * **Output Mutlak:** Anda harus meletakkan file bernama `credentials.json` di dalam folder utama proyek ini.

### TAHAP 2: Mengonfigurasi Remote Control (`.env`)
Sistem ini kebal dan bisa berganti-ganti acara lari hanya dengan mengubah 1 file.
1. Salin file `.env.example` dan ubah namanya menjadi `.env` (hilangkan `.example`).
2. Buka `.env` menggunakan **Notepad**.
3. Isi variabel sesuai dengan *event* hari ini:
   - `DATABASE_URL="postgresql://..."` *(Paste dari Railway)*
   - `GDRIVE_FOLDER_ID="id_folder_di_url_drive"` *(Folder tempat fotografer upload)*
4. **Aturan Mutlak .env:** Jangan ada spasi sebelum/sesudah tanda `=`, dan jika ingin menulis catatan, gunakan awalan tanda pagar `#`.

### TAHAP 3: Inisiasi Zero-Touch (Instalasi Laptop)
Anda meminjam PC baru? Tidak masalah.
1. Buka folder proyek ini.
2. Klik ganda (*double-click*) file **`setup_and_run.bat`**.
3. Skrip akan memindai apakah PC tersebut punya GPU NVIDIA, membuat Virtual Environment (`venv`), dan menginstal semua library AI yang tepat (versi CUDA GPU / CPU).
4. Setelah selesai, terminal akan memunculkan menu `run.py`.

### TAHAP 4: Diagnostik & Perakitan Infrastruktur
Di terminal yang terbuka (atau ketik manual di terminal VSCode/CMD), lakukan urutan ini:
1. **Cek Kesehatan:** Ketik `python run.py doctor`
   - *Sistem Dokter akan memindai apakah `.env` Anda benar, apakah `credentials.json` sudah ada, dan apakah koneksi Railway Anda aktif. JANGAN LANJUT JIKA ADA ERROR MERAH.*
2. **Rakit Database:** Ketik `python run.py init-db`
   - *Ini wajib dilakukan 1x untuk setiap event baru agar PostgreSQL di Railway Anda dibuatkan tabel dan diaktifkan ekstensi AI `pgvector`-nya.*

### TAHAP 5: Eksekusi Operasional (Go Live!)
Pilih mesin mana yang ingin Anda nyalakan berdasarkan posisi Anda saat ini:

* **POSISI A: Anda di Tenda Lapangan (Menyedot Foto)**
  Ketik: `python run.py start-watcher`
  - *Browser akan terbuka meminta izin akses Google Drive (Login email klien/Anda). Setelah diizinkan, biarkan terminal ini menyala selama acara. Ia akan mendownload foto ke RAM, mengekstrak wajah, dan mengirimnya ke Database.*

* **POSISI B: Anda di Cloud / Server Production (Melayani Pelari)**
  Ketik: `python run.py start-api`
  - *Ini adalah perintah yang dimasukkan di pengaturan Railway saat Anda mendeploy proyek ini ke cloud. Perintah ini menyalakan server pencarian agar web Next.js/Vercel Anda bisa menampilkan hasil foto ke ponsel pelari.*

---

## 🛠️ TROUBLESHOOTING & ERROR HANDLING

Setiap kali Anda menghadapi masalah, langkah pertama yang **wajib** dilakukan adalah mengetik:
`python run.py doctor`

**Masalah Umum & Solusinya:**
1. **Error: `DATABASE_URL belum disetting!`**
   - *Penyebab:* File `.env` belum dibuat, atau namanya masih `.env.example`, atau format isiannya salah (terdapat spasi).
2. **Error Google: `file credentials.json not found`**
   - *Penyebab:* Anda lupa mendownload kunci dari Google Cloud Console, atau namanya bukan huruf kecil semua, atau ditaruh di dalam sub-folder (harus sejajar dengan file `run.py`).
3. **Error Google: `Access Denied` saat login browser**
   - *Penyebab:* Email yang Anda pakai untuk login belum didaftarkan sebagai "Test Users" di menu OAuth Consent Screen pada Google Cloud Console Anda.
4. **Terminal `setup_and_run.bat` langsung tertutup (crash)**
   - *Penyebab:* Python belum dimasukkan ke "PATH" Windows. Coba buka CMD biasa, ketik `python --version`. Jika error, install ulang Python dan centang "Add Python to PATH" di halaman instalasi awal.
5. **HP Pelari Lambat Menerima Hasil (Overheat)**
   - *Penyebab:* Server API Anda (Railway) kehabisan RAM. Tingkatkan spesifikasi Server Railway ke 4GB/8GB selama jam sibuk acara.

---
*Visi: Satu Kode untuk Ribuan Event. Single-Tenant. Enterprise Microservices.*