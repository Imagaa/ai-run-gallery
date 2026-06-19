import sys
import uvicorn
from core.database import init_db

def print_help():
    print("="*50)
    print("🚀 AI RUN GALLERY - ENTERPRISE COMMANDER")
    print("="*50)
    print("Penggunaan: python run.py [perintah]")
    print("\nPerintah tersedia:")
    print("  init-db       : Merakit tabel & ekstensi Vector di PostgreSQL")
    print("  start-api     : Menghidupkan FastAPI Server (Untuk Railway/Prod)")
    print("  start-watcher : Menghidupkan Local Watcher Engine (Untuk Tenda Event)")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "init-db":
        print("[*] Mengirim sinyal perakitan infrastruktur ke Database...")
        init_db()
        
    elif command == "start-api":
        print("[*] Memanaskan reaktor API Server...")
        # Arahkan uvicorn ke path modul yang benar
        uvicorn.run("services.search_api.main:app_api", host="0.0.0.0", port=8000, reload=True)
        
    elif command == "start-watcher":
        from services.watcher.indexer_job import start_watching
        start_watching()
        
    else:
        print(f"[!] Perintah '{command}' tidak valid.")
        print_help()