# backend/app/config.py
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "papers"

# API configurations
API_CONFIG = {
    "title": "LLM Research Chatbot API",
    "description": "API for chatting about LLM research papers",
    "version": "1.0.0"
}

# Model configurations
MODEL_CONFIG = {
    "llm_model": "gemini-2.0-flash-exp",
    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
    "temperature": 0
}
