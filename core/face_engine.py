import cv2
import numpy as np
from insightface.app import FaceAnalysis

print("[*] MEMUAT MESIN ARCFACE 512D (STANDBY)...")
# Mode murni CPU untuk efisiensi biaya server
face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

def extract_faces(image_bytes: bytes):
    """
    Menerima input byte gambar dari internet/lokal,
    Mengembalikan array wajah yang terdeteksi beserta titik koordinatnya.
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