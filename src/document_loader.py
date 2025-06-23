import pdfplumber
from typing import List
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text

def chunk_by_size(text: str, max_chars: int = 2000) -> List[str]:
    """Splits text into chunks of up to max_chars, trying to split at paragraph boundaries."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chars:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def chunk_by_clause(text: str) -> List[str]:
    """Splits text into chunks based on clause numbering (e.g., 1., 2., 3.)."""
    # Regex to match clause numbers at the start of a line
    clauses = re.split(r'(?m)^\s*\d+\.\s+', text)
    # Remove empty strings and strip whitespace
    clauses = [clause.strip() for clause in clauses if clause.strip()]
    return clauses

def chunk_text(text: str, mode: str = "size", max_chars: int = 2000) -> List[str]:
    """Chunks text by size or by clause numbering, depending on mode."""
    if mode == "clause":
        return chunk_by_clause(text)
    else:
        return chunk_by_size(text, max_chars=max_chars) 