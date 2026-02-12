# PDF Summarizer

A private, local document summarization tool powered by Ollama, now featuring a modern React frontend and FastAPI backend.

## ✨ Features
- **Local Privacy**: All processing runs locally on your machine using Ollama.
- **Modern UI**: Clean, responsive interface built with React, Tailwind CSS, and Shadcn/UI.
- **Efficient Backend**: Fast extraction and summarization using Python and FastAPI.
- **Drag & Drop**: Easy file upload support.

## 🚀 Prerequisites
- **Ollama**: Must be installed and running (`ollama serve`).
- **Python 3.11+**: For the backend.
- **Node.js 18+**: For the frontend.

## 🛠️ Quick Start

### 1. Start Ollama
Ensure you have the model pulled:
```bash
ollama pull llama3.2:1b
```

### 2. Run the Application
We provide a helper script to start both backend and frontend:
```bash
chmod +x start.sh
./start.sh
```
This will start:
- Backend at `http://localhost:8000`
- Frontend at `http://localhost:5173`

### Manual Setup

**Backend:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📂 Project Structure
- `backend/`: FastAPI application and core logic.
- `frontend/`: React application (Vite).
- `src/`: Legacy scripts (kept for reference).
- `outputs/`: Generated summaries and upload storage.

## 📝 License
MIT
