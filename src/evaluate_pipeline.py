"""
evaluate_pipeline.py
--------------------
Evaluates summarization quality and efficiency for different LLMs.
Uses ROUGE, BERTScore (small, lightweight), and runtime/memory metrics.
"""

import time
import psutil
from ollama import Client
from evaluate import load
from pdf_extractor import extract_text_from_pdf
from pathlib import Path

# Load metrics
rouge = load("rouge")
bertscore = load("bertscore")

client = Client()

def evaluate_summary(model_name, text, reference_summary):
    """Run summarization + evaluation for a given model."""
    prompt = f"Summarize the following document in about 200 words:\n\n{text[:5000]}"

    start_mem = psutil.virtual_memory().used
    start_time = time.time()

    response = client.generate(model=model_name, prompt=prompt)

    end_time = time.time()
    end_mem = psutil.virtual_memory().used

    generated = response["response"].strip()

    # Efficiency metrics
    runtime = round(end_time - start_time, 2)
    mem_used_mb = round((end_mem - start_mem) / (1024 * 1024), 2)
    tokens = response.get("eval_count", None)

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


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    # Reference data (for benchmarking)
    pdf_path = str(base_dir / "sample_docs" / "sample1.pdf")
    reference_summary = "This document discusses the challenges of large-scale models and proposes efficient summarization for low-resource devices."

    print("Extracting PDF...")
    text = extract_text_from_pdf(pdf_path)

    models = ["llama3.2:1b", "gemma:2b"]
    all_results = []

    for model in models:
        print(f"\nEvaluating model: {model}")
        results = evaluate_summary(model, text, reference_summary)
        all_results.append(results)

    import pandas as pd
    csv_path = str(base_dir / "outputs" / "evaluation_results.csv")
    df = pd.DataFrame(all_results)
    df.to_csv(csv_path, index=False)
    print("\nEvaluation completed! Results saved to ../outputs/evaluation_results.csv")
    print(df[["model", "runtime_s", "memory_MB", "ROUGE1", "ROUGEL", "BERTScore_F1"]])