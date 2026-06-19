import os
from dotenv import load_dotenv

# Muat variabel dari .env (jika ada)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID", "")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 30))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 20))
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "")
FACE_MATCH_THRESHOLD = float(os.getenv("FACE_MATCH_THRESHOLD", 0.65))

if not DATABASE_URL:
    print("[WARNING] DATABASE_URL kosong! Pastikan .env sudah diisi jika berjalan di lokal.")