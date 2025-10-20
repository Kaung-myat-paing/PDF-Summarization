"""
pdf_extractor.py
----------------
Extracts text from PDF documents using pdfplumber and PyMuPDF.
Includes optional OCR fallback for scanned pages.
"""

import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from tqdm import tqdm
import os
from pathlib import Path


def extract_text_from_pdf(file_path: str, ocr_fallback: bool = False) -> str:
    """
    Extracts and returns the combined text from all pages of a PDF.
    
    :param file_path: Path to the PDF file.
    :param ocr_fallback: Whether to apply OCR if page text extraction fails.
    :return: Combined text string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text_output = []
    pdf = fitz.open(file_path)

    for page_index in tqdm(range(len(pdf)), desc="Extracting pages"):
        page = pdf.load_page(page_index)
        text = page.get_text("text")

        # OCR fallback for image-based PDFs
        if ocr_fallback and not text.strip():
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)

        text_output.append(text.strip())

    pdf.close()
    combined_text = "\n".join(text_output)
    return combined_text


if __name__ == "__main__":
     # Resolve path relative to project root
    base_dir = Path(__file__).resolve().parent.parent
    sample_pdf = str(base_dir / "sample_docs" / "sample1.pdf")
    result = extract_text_from_pdf(sample_pdf, ocr_fallback=False)
    print("\n--- Extracted Text Preview ---\n")
    print(result[:1500])  # print first 1500 chars