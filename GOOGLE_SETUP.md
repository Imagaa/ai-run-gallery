# ☁️ PANDUAN SETUP GOOGLE CLOUD CONSOLE (OAUTH)

Dokumen ini menjelaskan cara mendapatkan file `credentials.json` yang WAJIB ada agar program "Local Watcher" bisa mengunduh foto dari Google Drive panitia/klien.

## TAHAP 1: Membuat Project & Mengaktifkan API
1. Buka browser dan login ke [Google Cloud Console](https://console.cloud.google.com/).
2. Klik dropdown di kiri atas (sebelah logo Google Cloud), lalu klik **New Project**.
3. Beri nama project (misal: `AI-Run-Gallery-Event`), lalu klik **Create**.
4. Pastikan project tersebut terpilih di dropdown atas.
5. Di menu pencarian atas, ketik **Google Drive API**, lalu klik hasilnya.
6. Klik tombol biru **Enable** (Aktifkan).

## TAHAP 2: Mengonfigurasi Layar Persetujuan (OAuth Consent Screen)
*(Langkah ini agar Google tahu siapa yang berhak memakai aplikasi ini)*
1. Di menu sebelah kiri, cari **APIs & Services** > **OAuth consent screen**.
2. Pilih tipe **External** (Eksternal), lalu klik **Create**.
3. Isi formulir wajib:
   - **App Name:** `AI Run Watcher`
   - **User support email:** (Pilih email Anda)
   - **Developer contact information:** (Isi email Anda)
4. Scroll ke bawah, klik **Save and Continue** hingga selesai (abaikan bagian Scopes).
5. **SANGAT PENTING:** Di layar "Test users", klik **Add Users** dan masukkan alamat email Google yang memiliki folder foto acara tersebut. Jika email tidak ditambahkan ke sini, program akan ditolak masuk oleh Google!

## TAHAP 3: Membuat Kunci Rahasia (Credentials.json)
1. Di menu sebelah kiri, klik **Credentials**.
2. Di atas, klik **+ CREATE CREDENTIALS** > pilih **OAuth client ID**.
3. Di bagian Application type, wajib pilih **Desktop App** (Aplikasi Desktop).
4. Beri nama (misal: `Watcher Desktop`), lalu klik **Create**.
5. Akan muncul *pop-up* sukses. Klik tombol **DOWNLOAD JSON**.
6. Pindahkan file JSON yang ter-download ke dalam folder utama `AI-Run-Gallery` di komputer Anda.
7. **Ubah nama file tersebut menjadi tepat `credentials.json`** (huruf kecil semua).

## TAHAP 4: Uji Coba (Login Pertama)
1. Buka terminal, jalankan `python run.py start-watcher`.
2. Browser akan otomatis terbuka meminta Anda login ke akun Google.
3. Google mungkin memberi peringatan "Google hasn't verified this app" (Google belum memverifikasi aplikasi ini). Abaikan saja, klik **Continue / Lanjutkan** atau **Advanced -> Go to AI Run Watcher (unsafe)**.
4. Izinkan akses baca Google Drive.
5. Selesai! Program akan membuat file `token.json` agar Anda tidak perlu login ulang di hari H.

---
🚨 **CATATAN ERROR HANDLING GOOGLE:**
- Jika error `file credentials.json not found`: Anda lupa mengubah nama file JSON yang didownload atau salah menaruh foldernya.
- Jika error `Access Denied` saat login browser: Email yang Anda pakai untuk login belum dimasukkan ke daftar "Test Users" di Tahap 2 Langkah 5.