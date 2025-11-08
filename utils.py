"""
Utility Functions
Helper functions for the Campus Compass application
"""

import os
from pathlib import Path
from typing import List


def ensure_documents_directory() -> Path:
    """Ensure documents directory exists"""
    docs_dir = Path("documents")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir


def get_document_files() -> List[str]:
    """Get list of all document files in documents directory"""
    docs_dir = ensure_documents_directory()
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
    
    files = []
    for ext in supported_extensions:
        files.extend(list(docs_dir.glob(f"*{ext}")))
        files.extend(list(docs_dir.glob(f"**/*{ext}")))
    
    return [str(f) for f in files if f.is_file()]


def format_sources(sources: List[str]) -> str:
    """Format source list for display"""
    if not sources:
        return "No sources"
    
    if len(sources) == 1:
        return f"Source: {sources[0]}"
    
    return f"Sources: {', '.join(sources)}"


