"""
summarizer.py
-------------
Generates a summary from extracted PDF text using Ollama local LLMs.
"""

import time
from ollama import Client

def summarize_text(text: str, model_name: str = "llama3.2:1b", max_length: int = 2000) -> dict:
    """
    :param text: Input text string (e.g., extracted PDF content)
    :param model_name: Ollama model to use
    :param max_length: Maximum summary token length
    :return: dict with summary, runtime, token count, and length
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Input text is empty")

    prompt = f"""
    You are an expert technical writer. 
    1. Provide a comprehensive summary of the following document.
    2. Structure your summary with the following sections:
       - **Introduction**: Brief overview of the document's purpose.
       - **Key Points**: Bulleted list of the most important findings or arguments (at least 5 points).
       - **Conclusion**: A final wrapping thought or implication.
    3. The summary should be approximately 500 words in length to cover all details.
    4. Extract exactly 2 key topics or keywords, separated by commas.
    
    Format your response exactly like this:
    SUMMARY: <structured summary text>
    KEYWORDS: <keyword1, keyword2>

    Text:
    {text[:10000]}
    """

    client = Client()
    start_time = time.time()

    response = client.generate(model=model_name, prompt=prompt)

    end_time = time.time()
    runtime = end_time - start_time
    
    full_response = response["response"].strip()
    
    # Parse the structured response
    summary_text = full_response
    keywords = []
    
    if "SUMMARY:" in full_response and "KEYWORDS:" in full_response:
        parts = full_response.split("KEYWORDS:")
        summary_part = parts[0].replace("SUMMARY:", "").strip()
        keywords_part = parts[1].strip()
        
        summary_text = summary_part
        keywords = [k.strip() for k in keywords_part.split(",") if k.strip()]
    
    # Calculate speed (tokens/sec) based on eval_count and eval_duration if available, 
    # otherwise fallback to runtime
    eval_count = response.get("eval_count", 0)
    eval_duration = response.get("eval_duration", 0) # in nanoseconds
    
    speed = 0
    if eval_duration > 0:
        speed = eval_count / (eval_duration / 1e9)
    elif runtime > 0:
        speed = eval_count / runtime

    result = {
        "summary": summary_text,
        "keywords": keywords,
        "runtime_sec": round(runtime, 2),
        "tokens_generated": eval_count,
        "speed_tokens_per_sec": round(speed, 2),
    }

    return result