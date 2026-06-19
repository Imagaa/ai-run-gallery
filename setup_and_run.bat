@echo off
setlocal enabledelayedexpansion
title AI Run Gallery - Enterprise Setup
color 0A

echo =======================================================
echo     AI RUN GALLERY - ZERO-TOUCH INITIATOR ENGINE
echo =======================================================
echo.

:: 1. CEK INSTALASI PYTHON
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] FATAL: Python tidak terdeteksi di sistem ini.
    echo Silakan install Python 3.10+ dan pastikan Add to PATH dicentang saat instalasi.
    pause
    exit /b
)

:: 2. DETEKSI HARDWARE (NVIDIA SCANNER)
echo [*] Memindai spesifikasi perangkat keras...
set HAS_NVIDIA=0
for /f "skip=1 delims=" %%i in ('wmic path win32_VideoController get name 2^>nul') do (
    echo %%i | findstr /i "NVIDIA" >nul
    if !errorlevel! equ 0 set HAS_NVIDIA=1
)

if !HAS_NVIDIA! equ 1 (
    echo [*] STATUS HARDWARE: NVIDIA GPU Terdeteksi
    echo [*] STRATEGI: Mode High-End CUDA disiapkan.
) else (
    echo [*] STATUS HARDWARE: GPU NVIDIA tidak ditemukan.
    echo [*] STRATEGI: Mode Low-End CPU Murni disiapkan.
)
echo.

:: 3. SETUP VIRTUAL ENVIRONMENT (BRANKAS ISOLASI)
if not exist "venv" (
    echo [*] Membangun brankas isolasi Virtual Environment...
    python -m venv venv
)

:: 4. AKTIVASI & INSTALASI AMUNISI
echo [*] Mengaktifkan lingkungan virtual...
call venv\Scripts\activate

echo [*] Memasang pustaka dasar...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt

echo [*] Menyuntikkan Mesin AI Adaptif...
if !HAS_NVIDIA! equ 1 (
    pip install onnxruntime-gpu
) else (
    pip install onnxruntime
)

echo.
echo =======================================================
echo  INISIASI SELESAI. SISTEM SIAP DIGUNAKAN.
echo =======================================================
echo.

:: 5. HANDOVER KE PUSAT KOMANDO (run.py)
python run.py

echo.
pause