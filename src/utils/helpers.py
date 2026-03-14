import os
import yaml
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def get_pdf_files(folder_path: str) -> list:
    folder = Path(folder_path)
    return [str(f) for f in folder.glob("*.pdf")]

def ensure_directories():
    dirs = ["data/raw_pdfs", "data/processed", "vectorstore", "logs"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.1f} MB"

def get_paper_name(file_path: str) -> str:
    return Path(file_path).stem
