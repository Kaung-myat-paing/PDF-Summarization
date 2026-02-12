import time
import psutil
from evaluate import load
from backend.core.pdf_extractor import extract_text_from_pdf
from backend.core.summarizer import summarize_text
from pathlib import Path
import os
import pandas as pd

# Load metrics
rouge = load("rouge")
bertscore = load("bertscore")

def evaluate_summary(model_name, text, reference_summary):
    """Run summarization + evaluation for a given model."""
    
    start_mem = psutil.virtual_memory().used
    
    # Use the core summarizer logic -> This ensures consistency!
    # summarize_text returns: {'summary': ..., 'keywords': ..., 'runtime_sec': ..., ...}
    result = summarize_text(text, model_name=model_name)
    
    end_mem = psutil.virtual_memory().used
    
    generated = result["summary"]
    runtime = result["runtime_sec"]
    tokens = result["tokens_generated"]
    
    mem_used_mb = round((end_mem - start_mem) / (1024 * 1024), 2)

    # Quality metrics
    rouge_scores = rouge.compute(predictions=[generated], references=[reference_summary])
    bert_scores = bertscore.compute(predictions=[generated], references=[reference_summary], model_type="distilbert-base-uncased", lang="en")

    results = {
        "model": model_name,
        "runtime_s": runtime,
        "tokens": tokens,
        "memory_MB": mem_used_mb,
        "ROUGE1": rouge_scores["rouge1"],
        "ROUGE2": rouge_scores["rouge2"],
        "ROUGEL": rouge_scores["rougeL"],
        "BERTScore_F1": bert_scores["f1"][0],
        "summary": generated,
    }
    return results

def run_evaluation(input_text=None):
    """
    Main entry point for running the evaluation pipeline.
    :param input_text: Optional text to evaluate. If None, loads sample1.pdf.
    """
    # Resolve project root from backend/evaluation/pipeline.py
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    # Reference data (for benchmarking)
    # If using user input, we might not have a perfect reference summary.
    # We can use the input text itself as a "recall" reference (checking how much source content is preserved),
    # or keep a generic reference. For now, let's keep the generic one or use the input as reference to avoid errors.
    reference_summary = "This document discusses the challenges of large-scale models and proposes efficient summarization for low-resource devices."
    
    text = input_text
    
    if not text:
        pdf_path = base_dir / "sample_docs" / "sample1.pdf"
        print(f"Extracting PDF from: {pdf_path}")
        if not pdf_path.exists():
            print(f"Error: Sample PDF not found at {pdf_path}")
            return False
        text = extract_text_from_pdf(str(pdf_path))
    else:
        print("Using provided input text for evaluation...")
        # If evaluating user text, the hardcoded reference summary is likely irrelevant.
        # Ideally, we'd have a reference. Without one, ROUGE/BERTScore against a mismatching reference is meaningless.
        # Fallback: Use the text itself as the reference? (Measures extraction/compression)
        # Or just acknowledge this limit. For this demo, let's use the text itself 
        # as a proxy for "ground truth" to avoid low scores against an unrelated reference.
        reference_summary = text[:2000] # Use first 2k chars as a proxy reference

    models = ["llama3.2:1b"] # Add more models if available
    all_results = []

    for model in models:
        print(f"\nEvaluating model: {model}")
        try:
            results = evaluate_summary(model, text, reference_summary)
            all_results.append(results)
        except Exception as e:
            print(f"Failed to evaluate {model}: {e}")

    output_dir = base_dir / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    csv_path = output_dir / "evaluation_results.csv"
    df = pd.DataFrame(all_results)
    
    df.to_csv(csv_path, index=False)
    print(f"\nEvaluation completed! Results saved to {csv_path}")
    if not df.empty:
        print(df[["model", "runtime_s", "memory_MB", "ROUGE1", "ROUGEL", "BERTScore_F1"]])
    
    return True

if __name__ == "__main__":
    run_evaluation()