@echo off
echo Starting GHOST FOUNDER Backend & Frontend...
echo.

:: 1. Start Python Flask API Backend
echo Launching Flask Backend on http://localhost:5000...
start "Ghost Founder - Backend API" cmd /k "call venv\Scripts\activate && python server.py"

:: 2. Start React Frontend
echo Launching React Frontend on http://localhost:5173...
start "Ghost Founder - React Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers have been launched in separate console windows!
echo - API Server: http://localhost:5000
echo - React Dashboard: http://localhost:5173
echo.
pause
