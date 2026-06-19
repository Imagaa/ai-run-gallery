import time
from core.config import POLLING_INTERVAL, GDRIVE_FOLDER_ID
# from services.watcher.gdrive_sync import fetch_new_photos, download_photo

def start_watching():
    """Mesin Daemon Pengawas Google Drive (Real-Time)"""
    if not GDRIVE_FOLDER_ID:
        print("[!] FATAL: GDRIVE_FOLDER_ID di .env belum diisi!")
        return

    print(f"[*] LOCAL WATCHER AKTIF | Memantau Folder GDrive: {GDRIVE_FOLDER_ID}")
    print(f"[*] Interval Detak Jantung: {POLLING_INTERVAL} detik.")
    print("[*] Tekan CTRL+C untuk mematikan mesin pengawas.")
    print("="*60)
    
    try:
        while True:
            print(f"\n[*] [SYNC] Memindai foto baru dari fotografer...")
            
            # TODO: Integrasi logika Delta-Sync Google Drive
            # 1. new_files = fetch_new_photos(GDRIVE_FOLDER_ID, last_sync_time)
            # 2. if new_files:
            # 3.     for file in new_files:
            # 4.         bytes_data = download_photo(file['id'])
            # 5.         faces = extract_faces(bytes_data)
            # 6.         insert_to_db(file, faces)
            
            print(f"[*] [SYNC] Pindai selesai. Tertidur selama {POLLING_INTERVAL} detik...")
            time.sleep(POLLING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n[*] Menerima sinyal interupsi. Mematikan Watcher secara aman. Sampai jumpa!")