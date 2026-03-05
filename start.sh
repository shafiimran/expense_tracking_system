#!/bin/bash

echo "Starting Expense Tracking System..."
echo ""

echo "Starting FastAPI backend server..."
cd backend
uvicorn server:app --reload &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Streamlit frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

echo ""
echo "Both servers are running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for Ctrl+C
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
