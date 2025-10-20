import time
from ollama import Client

client = Client()

prompt = """
Summarize the following paragraph in 3 sentences:
Large language models have transformed text summarization but are computationally expensive and often inaccessible for small organizations. 
Developing efficient summarization models that can run locally is essential for data privacy and energy efficiency.
"""

start = time.time()
response = client.generate(model="llama3.2:1b", prompt=prompt)
end = time.time()

print("\n=== Summary ===\n", response["response"])
print("\n--- Runtime Info ---")
print(f"Elapsed time: {end - start:.2f} seconds")
print(f"Tokens generated: {response['eval_count']}")