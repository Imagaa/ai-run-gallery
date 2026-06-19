import time
from datetime import datetime, timezone
import psycopg2
from core.config import POLLING_INTERVAL, GDRIVE_FOLDER_ID, BATCH_SIZE
from core.database import get_db_connection
from core.face_engine import extract_faces
from services.watcher.gdrive_sync import get_gdrive_service, fetch_new_photos, download_photo_to_ram

def start_watching():
    """Mesin Daemon Pengawas Google Drive (Real-Time)"""
    if not GDRIVE_FOLDER_ID:
        print("[!] FATAL: GDRIVE_FOLDER_ID di .env belum diisi!")
        return

    print(f"[*] LOCAL WATCHER AKTIF | Memantau Folder GDrive: {GDRIVE_FOLDER_ID}")
    print(f"[*] Interval Detak Jantung: {POLLING_INTERVAL} detik. Batch: {BATCH_SIZE} file/putaran.")
    print("="*60)
    
    try:
        service = get_gdrive_service()
        print("[*] Autentikasi Google Drive: BERHASIL.")
    except Exception as e:
        print(f"[!] GAGAL AUTENTIKASI: {e}")
        return

    # Waktu mulai awal (Akan terus diperbarui setelah tiap file selesai diproses)
    # Jika ingin memproses folder dari nol, set ke None
    last_sync_time = None 

    try:
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [SYNC] Memindai foto baru...")
            
            try:
                new_files = fetch_new_photos(service, GDRIVE_FOLDER_ID, last_sync_time, BATCH_SIZE)
                
                if not new_files:
                    print(f"[*] Tidak ada foto baru. Tertidur selama {POLLING_INTERVAL} detik...")
                    time.sleep(POLLING_INTERVAL)
                    continue

                print(f"[*] Menemukan {len(new_files)} foto baru! Memulai pemrosesan...")
                
                conn = get_db_connection()
                cur = conn.cursor()

                for file in new_files:
                    file_id = file['id']
                    file_name = file['name']
                    file_time = file['createdTime']
                    
                    print(f"    -> Mengunduh ke RAM & Mengekstrak wajah: {file_name}...", end=" ")
                    
                    # 1. Download ke RAM
                    image_bytes = download_photo_to_ram(service, file_id)
                    
                    # 2. Ekstrak Wajah
                    faces = extract_faces(image_bytes)
                    
                    # 3. Simpan ke Database
                    try:
                        # Masukkan data foto
                        cur.execute(
                            "INSERT INTO runner_photos (file_name, gdrive_id) VALUES (%s, %s) RETURNING id",
                            (file_name, file_id)
                        )
                        photo_id = cur.fetchone()[0]
                        
                        # Masukkan semua vektor wajah yang terdeteksi di foto tersebut
                        for face in faces:
                            vector_str = "[" + ",".join(map(str, face.embedding)) + "]"
                            cur.execute(
                                "INSERT INTO photo_faces (photo_id, face_vector) VALUES (%s, %s)",
                                (photo_id, vector_str)
                            )
                        
                        conn.commit()
                        print(f"OK ({len(faces)} Wajah)")
                        
                        # Update checkpoint waktu agar tidak didownload ulang di putaran berikutnya
                        last_sync_time = file_time 
                        
                    except psycopg2.IntegrityError:
                        conn.rollback()
                        print("SKIP (Sudah ada di DB)")
                    except Exception as e:
                        conn.rollback()
                        print(f"ERROR DB: {e}")

                cur.close()
                conn.close()

            except Exception as e:
                print(f"[!] Terjadi kesalahan pada siklus sinkronisasi: {e}")
                
            print(f"[*] Siklus selesai. Tertidur selama {POLLING_INTERVAL} detik...")
            time.sleep(POLLING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n[*] Menerima sinyal interupsi. Mematikan Watcher secara aman. Sampai jumpa!")