@echo off

title DocuMind AI

echo ========================================
echo        DOCUMIND AI STARTING
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Flask Backend...
start "DocuMind Backend" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate && python app.py"

timeout /t 3 /nobreak >nul

echo Starting React Frontend...
start "DocuMind Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo ========================================
echo.
echo Both servers are starting...
echo Do not close the two terminal windows.
echo.

pause