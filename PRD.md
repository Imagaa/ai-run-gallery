# 📄 Product Requirements Document (PRD)
**Project:** AI Run Gallery - Enterprise Edition  
**Architecture:** Decoupled Microservices, Single-Tenant, Environment-Driven  
**Version:** 2.0 (Stable Enterprise)

## 1. Visi & Objektif
Membangun sistem *Facial Recognition* & *BIB Checker* skala korporat untuk acara olahraga massal (Maraton/Lari) yang 100% *recyclable* (bisa didaur ulang untuk ribuan *event* berbeda tanpa menyentuh *source code* inti). Sistem ini tahan banting terhadap lonjakan *traffic* garis finis dan mendukung pemrosesan AI adaptif.

## 2. Topologi Arsitektur (Decoupled Microservices)
Sistem ini menggunakan topologi Monorepo yang dipecah menjadi dua layanan independen yang hanya dihubungkan oleh URL Database.

### A. The Local Watcher (Mesin Indeks Lapangan)
* **Lokasi Eksekusi:** Laptop lokal kru/panitia di tenda acara.
* **Fungsi:** Memantau Google Drive fotografer secara *Real-Time* (Delta-Sync), mengunduh foto baru, mengekstrak matriks wajah menggunakan InsightFace, mengunggah ID & Vektor ke PostgreSQL, lalu menghapus foto dari RAM/Disk.
* **Keunggulan:** Laptop tidak perlu IP Publik. Zero Egress Cost dari Google Drive.

### B. The Sniper API (Peladen Pencarian Publik)
* **Lokasi Eksekusi:** *Cloud Server* (Railway / HuggingFace).
* **Fungsi:** Menerima unggahan foto *selfie* dari HP pelari (via Vercel Frontend), mengekstrak wajah pelari, lalu melakukan kueri pencarian vektor (`<=>`) ke database PostgreSQL.
* **Skalabilitas:** Sangat ringan. Hanya membutuhkan *Scale-Up* RAM/CPU murni pada saat "Hari H" perlombaan berlangsung.

## 3. Spesifikasi Infrastruktur (Single-Tenant)
Setiap 1 *Event* Lari akan dibuatkan 1 set infrastruktur terisolasi:
1.  **Storage:** Google Drive (Menyimpan foto asli fotografer).
2.  **Database:** PostgreSQL dengan ekstensi `pgvector` (menyimpan indeks L2 Distance).
3.  **Backend AI:** FastAPI berjalan di Python 3.10+ dengan model `buffalo_sc` (ArcFace 512D).
4.  **Frontend:** Next.js (Vercel) dengan pembatasan resolusi kanvas kamera maksimal 640px untuk mencegah HP *overheat*.

## 4. Fitur Cerdas Inti (Core Engine)
1.  **Zero-Touch Provisioning:** Sistem inisiasi `setup_and_run.bat` yang memindai spesifikasi *hardware* PC secara otomatis dan membangun *virtual environment* tanpa campur tangan manusia.
2.  **Adaptive Compute:** Jika GPU NVIDIA terdeteksi, AI Engine menggunakan `CUDAExecutionProvider`. Jika tidak, mundur otomatis ke `CPUExecutionProvider`.
3.  **Smart Hybrid Query:** Pencarian database memprioritaskan toleransi jarak Euclidean (*threshold* ~0.65) dan di- *fallback* menggunakan pencarian *Wildcard* nomor BIB.