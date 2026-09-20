@echo off
setlocal enabledelayedexpansion
echo ============================================================
echo   Starting Kalinga University AI Chatbot (Multi-Device PWA)
echo ============================================================
echo.

:: Detect local network IPv4 address for multi-device access
set "LOCAL_IP=localhost"
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "(Test-Connection -ComputerName (hostname) -Count 1).IPV4Address.IPAddressToString"`) do (
    set "LOCAL_IP=%%i"
)

echo [1/2] Starting FastAPI Backend on 0.0.0.0:8000...
start "Kalinga Chatbot - Backend (Port 8000)" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo.
echo [2/2] Starting React + Vite Frontend on 0.0.0.0:5173...
start "Kalinga Chatbot - Frontend (Port 5173)" cmd /k "cd /d %~dp0frontend && npm run dev -- --host 0.0.0.0"
echo.
echo ============================================================
echo   Both servers launched successfully!
echo ------------------------------------------------------------
echo   Local PC Access:          http://localhost:5173
echo   Phone / Other Devices:    http://%LOCAL_IP%:5173
echo   Backend API & Docs:       http://localhost:8000/docs
echo ------------------------------------------------------------
echo   PWA: Open in browser and click "Install App" or "QR"
echo   to use the app natively on any phone, tablet, or PC!
echo ============================================================
