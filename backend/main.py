from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import os
import uuid
from typing import Optional

# Import core logic (relative import if run from parent, or absolute from root)
from backend.core.pdf_extractor import extract_text_from_pdf
from backend.core.summarizer import summarize_text
from backend.evaluation.pipeline import run_evaluation
from backend.evaluation.visualize import generate_plots

app = FastAPI(
    title="PDF Summarizer API",
    description="API for extracting text and summarizing PDF documents using local LLMs.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",  # React Frontend (Vite default)
    "http://127.0.0.1:5173",
    "*", # Allow all for development convenience
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (graphs, etc.)
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="outputs"), name="static")

# Configuration
UPLOAD_DIR = os.path.join(os.getcwd(), "outputs", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SummarizeRequest(BaseModel):
    text: str
    model: str = "llama3.2:1b"
    max_length: int = 800

@app.get("/")
def read_root():
    return {"message": "PDF Summarizer API is running"}

@app.post("/api/extract-text")
async def extract_text_endpoint(
    file: UploadFile = File(...), 
    ocr_fallback: bool = False
):
    """
    Upload a PDF file and extract its text content.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Generate unique filename to prevent collisions
        file_id = str(uuid.uuid4())
        safe_filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract text
        text = extract_text_from_pdf(file_path, ocr_fallback=ocr_fallback)
        
        # Optional cleanup: remove file after extraction to save space
        # os.remove(file_path)
        
        return {
            "filename": file.filename,
            "text": text,
            "message": "Text extraction successful"
        }
        
    except Exception as e:
        # cleanup if error occurs
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/api/summarize")
async def summarize_endpoint(request: SummarizeRequest):
    """
    Summarize the provided text using the specified LLM model.
    """
    try:
        result = summarize_text(
            text=request.text, 
            model_name=request.model, 
            max_length=request.max_length
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.get("/api/evaluation-results")
def get_evaluation_results():
    """
    Retrieve evaluation metrics from the CSV file.
    """
    csv_path = os.path.join(os.getcwd(), "outputs", "evaluation_results.csv")
    if not os.path.exists(csv_path):
        # Return dummy data or empty list if file doesn't exist
        return []
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        # Handle NaN values
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading evaluation results: {str(e)}")

class EvaluateRequest(BaseModel):
    text: Optional[str] = None

@app.post("/api/evaluate")
async def run_evaluation_endpoint(request: EvaluateRequest = None):
    """
    Trigger the full evaluation pipeline:
    1. Run summarization benchmarks (pipeline.py)
    2. Generate visualization plots (visualize.py)
    """
    try:
        input_text = request.text if request else None
        
        # 1. Run Pipeline
        print("Starting evaluation pipeline...")
        success_pipeline = run_evaluation(input_text=input_text)
        if not success_pipeline:
             raise Exception("Pipeline execution failed.")

        # 2. Generate Plots
        print("Generating plots...")
        success_plots = generate_plots()
        if not success_plots:
            raise Exception("Plot generation failed.")
            
        return {"message": "Evaluation and visualization completed successfully."}
    except Exception as e:
        print(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
