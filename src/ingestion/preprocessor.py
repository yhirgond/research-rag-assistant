import re


def clean_text(text: str) -> str:
    """Clean and normalize extracted PDF text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove null bytes
    text = text.replace('\x00', '')
    return text.strip()


def preprocess_pages(pages: list) -> list:
    """Apply cleaning to all extracted pages."""
    cleaned = []
    for page in pages:
        cleaned_text = clean_text(page["text"])
        if len(cleaned_text) > 10:  # only filter very empty pages
            page["text"] = cleaned_text
            cleaned.append(page)
    return cleaned