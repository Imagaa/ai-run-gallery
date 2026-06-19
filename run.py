import sys
import os
import uvicorn
from core.database import init_db, get_db_connection

def run_doctor():
    """Mesin Pemindai Error Terpusat (System Doctor)"""
    print("\n" + "="*60)
    print(" 🩺 AI RUN GALLERY - SYSTEM DOCTOR (DIAGNOSTIK)")
    print("="*60)
    
    issues_found = 0

    # 1. CEK ENVIRONMENT VARIABLES (.env)
    print("\n[1] Memeriksa Environment Variables (.env)...")
    from core.config import DATABASE_URL, GDRIVE_FOLDER_ID
    if not DATABASE_URL:
        print("  ❌ ERROR: DATABASE_URL kosong!")
        print("     Solusi: Buka file .env dan isi URL PostgreSQL dari Railway.")
        issues_found += 1
    else:
        print("  ✅ DATABASE_URL terdeteksi.")

    if not GDRIVE_FOLDER_ID:
        print("  ⚠️ PERINGATAN: GDRIVE_FOLDER_ID kosong!")
        print("     Info: Wajib diisi JIKA Anda ingin menjalankan Local Watcher.")
    else:
        print("  ✅ GDRIVE_FOLDER_ID terdeteksi.")

    # 2. CEK KONEKSI DATABASE & VEKTOR
    print("\n[2] Memeriksa Infrastruktur Database...")
    if DATABASE_URL:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
            ext = cur.fetchone()
            if ext:
                print("  ✅ Koneksi Database SUKSES dan Ekstensi 'pgvector' AKTIF.")
            else:
                print("  ❌ ERROR: Ekstensi 'pgvector' belum diinstal di Database!")
                print("     Solusi: Jalankan perintah 'python run.py init-db'.")
                issues_found += 1
            cur.close()
            conn.close()
        except Exception as e:
            print(f"  ❌ ERROR KONEKSI DB: {e}")
            print("     Solusi: Cek apakah DATABASE_URL valid, atau apakah database Railway sedang mati/kehabisan kredit.")
            issues_found += 1

    # 3. CEK KREDENSIAL GOOGLE DRIVE
    print("\n[3] Memeriksa Autentikasi Google Drive...")
    if not os.path.exists('credentials.json'):
        print("  ❌ ERROR: File 'credentials.json' TIDAK DITEMUKAN!")
        print("     Solusi: Download file OAuth dari Google Cloud Console dan taruh di folder utama (AI-Run-Gallery).")
        issues_found += 1
    else:
        print("  ✅ File 'credentials.json' tersedia.")
        if os.path.exists('token.json'):
            print("  ✅ File 'token.json' (Sesi Login) tersedia.")
        else:
            print("  ⚠️ PERINGATAN: 'token.json' belum ada.")
            print("     Info: Saat Watcher dijalankan pertama kali, browser akan terbuka untuk login Google.")

    # 4. CEK DEPENDENSI AI & HARDWARE
    print("\n[4] Memeriksa Mesin AI & Library...")
    try:
        import cv2
        import insightface
        import onnxruntime as ort
        print("  ✅ Library Inti (OpenCV, InsightFace, ONNX) terinstal dengan baik.")
        
        providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in providers:
            print("  🚀 Hardware: Mode GPU (NVIDIA CUDA) Tersedia dan Siap.")
        else:
            print("  🐢 Hardware: Mode CPU Murni (Tanpa GPU).")
    except ImportError as e:
        print(f"  ❌ ERROR LIBRARY: {e}")
        print("     Solusi: Virtual Environment belum aktif atau instalasi gagal. Jalankan ulang 'setup_and_run.bat'.")
        issues_found += 1

    print("\n" + "="*60)
    if issues_found == 0:
        print(" 🎉 KESIMPULAN: SISTEM 100% SEHAT DAN SIAP TEMPUR!")
    else:
        print(f" 🚨 KESIMPULAN: Ditemukan {issues_found} masalah fatal. Harap perbaiki sesuai solusi di atas sebelum memulai.")
    print("="*60 + "\n")

def print_help():
    print("="*50)
    print("🚀 AI RUN GALLERY - ENTERPRISE COMMANDER")
    print("="*50)
    print("Penggunaan: python run.py [perintah]")
    print("\nPerintah tersedia:")
    print("  doctor        : 🩺 Mendiagnosis error (Cek DB, Env, Google, AI)")
    print("  init-db       : 🏗️ Merakit tabel & ekstensi Vector di PostgreSQL")
    print("  start-api     : 🌐 Menghidupkan FastAPI Server (Untuk Railway/Prod)")
    print("  start-watcher : 👁️ Menghidupkan Local Watcher Engine (Untuk Tenda Event)")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "doctor":
        run_doctor()
    elif command == "init-db":
        init_db()
    elif command == "start-api":
        uvicorn.run("services.search_api.main:app_api", host="0.0.0.0", port=8000, reload=True)
    elif command == "start-watcher":
        from services.watcher.indexer_job import start_watching
        start_watching()
    else:
        print(f"[!] Perintah '{command}' tidak valid.")
        print_help()