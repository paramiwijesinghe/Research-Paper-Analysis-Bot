# backend/app/utils/pdf_loader.py
from langchain.document_loaders import PyPDFLoader
from pathlib import Path

def load_pdf(pdf_path: str or Path):
    """Load and split PDF document."""
    loader = PyPDFLoader(str(pdf_path))
    return loader.load_and_split()
