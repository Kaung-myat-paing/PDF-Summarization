"""
summarizer.py
-------------
Generates a summary from extracted PDF text using Ollama local LLMs.
Records performance benchmarks.
"""

import time
import pandas as pd
from ollama import Client
from tqdm import tqdm
from pathlib import Path

def summarize_text(text: str, model_name: str = "llama3.2:1b", max_length: int = 800) -> dict:
    """
    :param text: Input text string (e.g., extracted PDF content)
    :param model_name: Ollama model to use
    :param max_length: Maximum summary token length
    :return: dict with summary, runtime, token count, and length
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Input text is empty")

    prompt = f"""
    Summarize the following document into key points and a concise abstract (max {max_length} tokens). 
    Focus on domain-specific terminology and factual accuracy.

    Text:
    {text[:5000]}  # limit context for smaller models
    """

    client = Client()
    start_time = time.time()

    response = client.generate(model=model_name, prompt=prompt)

    end_time = time.time()
    runtime = end_time - start_time

    result = {
        "summary": response["response"].strip(),
        "runtime_sec": round(runtime, 2),
        "tokens_used": response.get("eval_count", None),
        "summary_length": len(response["response"].split())
    }

    return result


if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf

    # Path to sample PDF
    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = str(base_dir / "sample_docs" / "sample1.pdf")

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path, ocr_fallback=False)

    print("\nGenerating summary...")
    output = summarize_text(text, model_name="llama3.2:1b")

    # Save results to CSV
    csv_path = str(base_dir / "outputs" / "summary_results.csv")
    result_df = pd.DataFrame([output])
    result_df.to_csv(csv_path, mode="a", index=False, header=False)

    print("\n=== Summary Output ===\n")
    print(output["summary"])
    print("\n--- Benchmark Info ---")
    print(f"Runtime: {output['runtime_sec']}s | Tokens: {output['tokens_used']} | Length: {output['summary_length']} words")