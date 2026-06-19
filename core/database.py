import psycopg2
from core.config import DATABASE_URL

def get_db_connection():
    """Membuka koneksi baru ke PostgreSQL"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL belum disetting!")
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Inisialisasi Tabel & Ekstensi Vektor (Otomatis Daur Ulang untuk Klien Baru)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Aktifkan ekstensi AI Vector (Wajib di Railway Postgres)
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Tabel Data Foto
        cur.execute("""
            CREATE TABLE IF NOT EXISTS runner_photos (
                id SERIAL PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                gdrive_id VARCHAR(255) UNIQUE NOT NULL,
                bib_numbers TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Tabel Matriks Wajah (1 foto bisa punya >1 wajah)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS photo_faces (
                id SERIAL PRIMARY KEY,
                photo_id INTEGER REFERENCES runner_photos(id) ON DELETE CASCADE,
                face_vector vector(512) NOT NULL
            );
        """)
        
        # Index untuk pencarian super cepat (Euclidean distance L2)
        # Akan sangat terasa performanya jika data > 10.000 wajah
        cur.execute("""
            CREATE INDEX IF NOT EXISTS face_vector_idx 
            ON photo_faces USING ivfflat (face_vector vector_l2_ops) WITH (lists = 100);
        """)
        
        conn.commit()
        print("[*] DATABASE SIAP: Tabel dan Ekstensi Vector berhasil diinisialisasi.")
    except Exception as e:
        print(f"[!] GAGAL INISIALISASI DB: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()