from pathlib import Path
import fitz 
from docx import Document

def extract_text(path: Path) -> str:
    """
    Extracts text from a PDF or Word document.
    """
    path_str = str(path).lower()
    if path_str.endswith(".pdf"):
        return extract_pdf(path)
    elif path_str.endswith(".docx"):
        return extract_word(path)
    else:
        raise ValueError(f"Unsupported file format: {path.name}")

def extract_pdf(path: Path) -> str:
    with fitz.open(str(path)) as doc:
        return "".join(page.get_text() for page in doc)

def extract_word(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(para.text for para in doc.paragraphs)
