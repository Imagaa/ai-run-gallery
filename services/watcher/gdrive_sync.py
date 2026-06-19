import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Hanya butuh akses BACA (Aman untuk data klien)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_gdrive_service():
    """Membangun koneksi autentikasi ke Google Drive"""
    creds = None
    # Token.json menyimpan akses sesi agar tidak perlu login web berkali-kali
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("[!] FATAL: File 'credentials.json' dari Google Cloud Console tidak ditemukan di folder utama!")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('drive', 'v3', credentials=creds)

def fetch_new_photos(service, folder_id: str, last_sync_time: str, batch_size: int = 20):
    """
    Mengambil daftar file terbaru (Delta-Sync) dari folder GDrive.
    last_sync_time format: ISO 8601 (contoh: '2023-10-01T15:00:00Z')
    """
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    if last_sync_time:
        query += f" and createdTime > '{last_sync_time}'"
        
    results = service.files().list(
        q=query,
        pageSize=batch_size,
        fields="nextPageToken, files(id, name, createdTime)",
        orderBy="createdTime asc" # Proses dari yang paling lama antre
    ).execute()
    
    return results.get('files', [])

def download_photo_to_ram(service, file_id: str) -> bytes:
    """Mengunduh gambar langsung ke RAM (Tanpa menyentuh Harddisk/SSD)"""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        
    return fh.getvalue()