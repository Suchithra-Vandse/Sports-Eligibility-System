@echo off
title Sports Eligibility Management System
cd /d "%~dp0"

echo ============================================================
echo   Starting Sports Eligibility Management System...
echo ============================================================
echo.
echo Server starting at: http://127.0.0.1:5000/
echo Your web browser will open automatically in a moment...
echo (Keep this window open while using the application)
echo.

REM Automatically open the browser after a 2-second delay
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000/"

REM Run app with Python
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" app.py
    goto end
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    python app.py
    goto end
)

py app.py

:end
echo.
echo Server stopped.
pause
