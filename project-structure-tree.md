C:\AI-Run-Gallery\
│
├── .env.example              <-- Template variabel mutlak untuk tiap acara
├── .gitignore                <-- Mencegah file rahasia/model AI ter-upload ke GitHub
├── requirements.txt          <-- Daftar pustaka Python
├── run.py                    <-- Terminal Commander (Pusat Kontrol)
│
├── core/                     <-- Jantung Sistem (Bisa dipakai oleh Watcher maupun API)
│   ├── __init__.py
│   ├── config.py             <-- Pemuat variabel .env yang aman
│   ├── database.py           <-- Koneksi ke PostgreSQL
│   └── face_engine.py        <-- Mesin InsightFace & OpenCV
│
└── services/                 <-- Layanan Mikro Independen
    ├── __init__.py
    ├── watcher/              <-- PROGRAM 1: Dijalankan di Laptop Lokal (Tenda Acara)
    │   ├── __init__.py
    │   ├── gdrive_sync.py    <-- Logika Delta-Sync GDrive (Antrean download)
    │   └── indexer_job.py    <-- Loop utama penyedot foto ke Database
    │
    └── search_api/           <-- PROGRAM 2: Di-deploy ke Railway
        ├── __init__.py
        └── main.py           <-- FastAPI Server (Endpoint pencarian)