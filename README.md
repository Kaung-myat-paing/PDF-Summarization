# Project: Private and Resource-Efficient Document Summarization

## 📋 Prerequisites
- macOS 11+ (Apple Silicon M1/M2 preferred)
- ≥ 8 GB RAM and ≈ 25 GB free disk space
- Internet connection (for model downloads)
- Command-line familiarity

---

## ⚙️ 1. Environment Setup


### 1.1 Install Homebrew (if missing)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew --version
```

### 1.2 Install Python 3.11 and Git LFS
```bash
brew install python@3.11 git-lfs
git lfs install
```

### 1.3 Create and Activate a Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 1.4 Install Ollama (Local Model Runtime)
```bash
brew install ollama
brew services start ollama
ollama version
```

### 1.5 (Recommended) Install PDF/OCR Utilities
```bash
brew install poppler tesseract
```

## 2. Install Core Dependencies
Activate your environment first:
```bash
source .venv/bin/activate
pip install --upgrade pip
```

Then install all required packages:
```bash
pip install langchain langchain-community ollama
pip install transformers==4.43.4 datasets evaluate
pip install rouge-score bert-score
pip install pdfplumber PyMuPDF
pip install numpy pandas matplotlib tqdm
```

---

## 3. Download a Lightweight Model
```bash
ollama pull llama3.2:1b
# or, for a slightly larger model:
ollama pull mistral:7b
```

Verify available models:
```bash
ollama list
```

---


