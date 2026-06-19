import cv2
import numpy as np
import onnxruntime as ort
from insightface.app import FaceAnalysis

print("\n[*] MEMULAI HARDWARE PROFILER...")

# 1. Deteksi Cerdas Ketersediaan Komputasi
available_providers = ort.get_available_providers()

# 2. Dynamic Execution Strategy
if 'CUDAExecutionProvider' in available_providers:
    print("[*] TIER 1 TERDETEKSI: Mengaktifkan Akselerasi GPU (CUDA). Kecepatan Maksimal!")
    active_providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
else:
    print("[*] TIER 2 TERDETEKSI: Menggunakan Komputasi CPU Murni. Mode Stabil.")
    active_providers = ['CPUExecutionProvider']

print("[*] MEMUAT MESIN ARCFACE 512D...")

# 3. Injeksi Provider secara Dinamis
try:
    face_app = FaceAnalysis(name='buffalo_sc', providers=active_providers)
    face_app.prepare(ctx_id=0, det_size=(640, 640))
    print("[*] MESIN AI SIAP TEMPUR.\n")
except Exception as e:
    print(f"[!] GAGAL MEMUAT MODEL AI: {e}")
    print("[!] Pastikan koneksi internet aktif untuk unduhan model pertama kali.")

def extract_faces(image_bytes: bytes):
    """
    Menerima input byte gambar dari internet/lokal.
    Mengembalikan array wajah yang terdeteksi.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return []
            
        faces = face_app.get(img)
        return faces
    except Exception as e:
        print(f"[!] Error ekstraksi wajah: {e}")
        return []