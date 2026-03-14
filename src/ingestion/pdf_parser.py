import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> list:
    """Extract text page-by-page with metadata."""
    doc = fitz.open(pdf_path)
    pages = []
    paper_title = Path(pdf_path).stem

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            pages.append({
                "text": text,
                "page": page_num,
                "source": paper_title,
                "file_path": str(pdf_path)
            })

    doc.close()
    return pages