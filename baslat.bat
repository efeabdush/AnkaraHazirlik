@echo off
title Hazirlik Prep
cd /d "%~dp0"

echo.
echo  Hazirlik Prep
echo  Site:  http://localhost:3000
echo  Admin: http://localhost:3000/admin
echo.
echo  Bu tek pencereyi kapatma. Durdurmak icin Ctrl+C bas.
echo.

if not exist "backend\.venv\Scripts\uvicorn.exe" (
  echo [!] Once backend kur:
  echo     cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
  pause
  exit /b 1
)

if not exist "frontend\node_modules\" (
  echo [!] Once frontend kur:
  echo     cd frontend ^&^& npm install
  pause
  exit /b 1
)

where powershell >nul 2>&1
if errorlevel 1 (
  echo [!] PowerShell bulunamadi.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0baslat.ps1"
echo.
pause
