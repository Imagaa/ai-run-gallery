from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from core.config import CORS_ALLOWED_ORIGINS, FACE_MATCH_THRESHOLD
from core.database import get_db_connection
from core.face_engine import extract_faces

app_api = FastAPI(title="Adipati Face Search API", version="2.0 - Enterprise")

# Pengaturan CORS Dinamis dari .env
origins = [origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",")] if CORS_ALLOWED_ORIGINS else ["*"]

app_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False, # Mutlak False untuk public API
    allow_methods=["*"],
    allow_headers=["*"],
)

@app_api.post("/search-double-tap")
async def search_double_tap(bib: str = Form(""), file: UploadFile = File(...)):
    # 1. Baca File
    contents = await file.read()
    
    # 2. Ekstraksi Wajah Terpusat (Memanggil Core Module)
    faces = extract_faces(contents)
    if len(faces) == 0:
        return {"status": "failed", "message": "no_face_detected"}
    
    # Ambil wajah terbesar (Selfie)
    faces = sorted(faces, key=lambda x: (x.bbox[2]-x.bbox[0]) * (x.bbox[3]-x.bbox[1]), reverse=True)
    embedding = faces[0].embedding
    vector_str = "[" + ",".join(map(str, embedding)) + "]"

    # 3. KONEKSI & SMART HYBRID QUERY
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        if bib and bib.strip() != "":
            # SKENARIO 1: UPLOAD (BIB + WAJAH)
            query = """
                WITH matched_photos AS (
                    SELECT r.id, r.file_name, r.gdrive_id, r.bib_numbers,
                           MIN(f.face_vector <=> %s) as face_distance
                    FROM runner_photos r
                    LEFT JOIN photo_faces f ON r.id = f.photo_id
                    GROUP BY r.id, r.file_name, r.gdrive_id, r.bib_numbers
                )
                SELECT file_name, gdrive_id, bib_numbers, COALESCE(face_distance, 2.0) as final_distance
                FROM matched_photos
                WHERE face_distance < %s OR bib_numbers::text ILIKE %s
                ORDER BY final_distance ASC
                LIMIT 20;
            """
            cur.execute(query, (vector_str, FACE_MATCH_THRESHOLD, f"%{bib}%"))
        else:
            # SKENARIO 2: LIVE SELFIE (MURNI WAJAH)
            query = """
                WITH matched_photos AS (
                    SELECT r.id, r.file_name, r.gdrive_id, r.bib_numbers,
                           MIN(f.face_vector <=> %s) as face_distance
                    FROM runner_photos r
                    JOIN photo_faces f ON r.id = f.photo_id
                    GROUP BY r.id, r.file_name, r.gdrive_id, r.bib_numbers
                )
                SELECT file_name, gdrive_id, bib_numbers, face_distance as final_distance
                FROM matched_photos
                WHERE face_distance < %s
                ORDER BY final_distance ASC
                LIMIT 15;
            """
            # Toleransi live selfie diketatkan (-0.05) dari setting .env
            cur.execute(query, (vector_str, FACE_MATCH_THRESHOLD - 0.05))
            
        rows = cur.fetchall()
        
        if not rows:
            return {"status": "failed", "message": "no_match_found"}

        results = []
        for row in rows:
            dist = float(row[3])
            results.append({
                "file_name": row[0],
                "gdrive_id": row[1],
                "bib_numbers": row[2] if row[2] else "",
                "distance": dist if dist <= 1.0 else 0.99
            })

        return {"status": "success", "matches_found": len(results), "data": results}
    
    finally:
        cur.close()
        conn.close()