"""
visualize_results.py
--------------------
Plots efficiency vs. quality trade-offs from evaluation_results.csv
for thesis reporting and analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def generate_plots():
    """Generates evaluation plots from the results CSV."""
    
    # Resolve project root from backend/evaluation/visualize.py
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_dir = base_dir / "outputs"
    csv_path = output_dir / "evaluation_results.csv"

    if not csv_path.exists():
        print(f"Warning: Evaluation file not found at {csv_path}")
        return False

    # Read CSV with proper header handling
    try:
        df = pd.read_csv(csv_path, header=0)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False

    # Remove any duplicate header rows that got saved as data
    df = df[df['model'] != 'model']

    numeric_cols = ['runtime_s', 'memory_MB', 'tokens', 'ROUGE1', 'ROUGE2', 'ROUGEL', 'BERTScore_F1']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Reset index after filtering
    df = df.reset_index(drop=True)

    print("\n=== Summary of Evaluation Results ===")
    print(df[["model", "runtime_s", "memory_MB", "ROUGE1", "ROUGEL", "BERTScore_F1"]])

    # Ensure output directory exists (it should)
    output_dir.mkdir(exist_ok=True)

    # === Plot 1: Runtime vs. Quality ===
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=df,
        x="runtime_s",
        y="BERTScore_F1",
        hue="model",
        s=120,
        style="model"
    )
    plt.title("Runtime vs. Semantic Quality (BERTScore F1)")
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("BERTScore F1")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "runtime_vs_quality.png", dpi=300)
    plt.close() # Close figure to free memory

    # === Plot 2: ROUGE vs. Runtime ===
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=df,
        x="runtime_s",
        y="ROUGEL",
        hue="model",
        s=120
    )
    plt.title("Runtime vs. ROUGE-L Score")
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("ROUGE-L")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "runtime_vs_rouge.png", dpi=300)
    plt.close()

    # === Plot 3: Memory Usage Bar Chart ===
    plt.figure(figsize=(7, 5))
    sns.barplot(data=df, x="model", y="memory_MB", hue="model", palette="coolwarm", legend=False)
    plt.title("Memory Usage by Model")
    plt.ylabel("Memory (MB)")
    plt.xlabel("Model")
    plt.tight_layout()
    plt.savefig(output_dir / "memory_usage.png", dpi=300)
    plt.close()

    print(f"Plots saved to {output_dir}")
    return True

if __name__ == "__main__":
    generate_plots()