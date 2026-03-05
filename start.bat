@echo off
echo Starting Expense Tracking System...
echo.

echo Starting FastAPI backend server...
start "FastAPI Backend" cmd /k "cd backend && uvicorn server:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Streamlit frontend...
start "Streamlit Frontend" cmd /k "streamlit run frontend/app.py"

echo.
echo Both servers are starting in separate windows.
echo Close those windows to stop the servers.
