"""
Utility functions for the RAG pipeline
"""

import os
import logging
import hashlib
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('rag_pipeline.log')
        ]
    )
    return logging.getLogger(__name__)

def create_directories(directories: List[str]) -> None:
    """Create directories if they don't exist"""
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def validate_pdf_files(pdf_paths: List[str]) -> List[str]:
    """Validate that PDF files exist and are readable"""
    valid_paths = []
    for path in pdf_paths:
        if os.path.exists(path) and path.lower().endswith('.pdf'):
            valid_paths.append(path)
        else:
            logging.warning(f"Invalid or missing PDF file: {path}")
    return valid_paths

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    return text.strip()

def save_metadata(metadata: Dict[str, Any], filename: str) -> None:
    """Save metadata to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

def load_metadata(filename: str) -> Optional[Dict[str, Any]]:
    """Load metadata from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Could not load metadata from {filename}: {e}")
        return None

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive file information"""
    stat = os.stat(file_path)
    return {
        "path": file_path,
        "name": os.path.basename(file_path),
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "modified": stat.st_mtime,
        "hash": calculate_file_hash(file_path)
    }