#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping services..."
    kill $(jobs -p)
    exit
}

trap cleanup SIGINT SIGTERM

echo "Starting PDF Summarizer..."

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

# Apply backend requirements if not installed
# pip install fastapi uvicorn python-multipart pdfplumber pymupdf pytesseract pillow ollama pandas

# Start Backend
echo "Starting Backend on port 8000..."
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
