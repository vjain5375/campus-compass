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
    
    # Use rglob to recursively find all files, then filter by extension
    # This avoids duplicates that would occur with both *{ext} and **/*{ext}
    all_files = list(docs_dir.rglob('*'))
    files = []
    seen_paths = set()  # Track seen files to avoid duplicates
    
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            # Normalize path to avoid duplicates (e.g., Windows path issues)
            normalized_path = str(file_path.resolve())
            if normalized_path not in seen_paths:
                seen_paths.add(normalized_path)
                files.append(str(file_path))
    
    return files


def format_sources(sources: List[str]) -> str:
    """Format source list for display"""
    if not sources:
        return "No sources"
    
    if len(sources) == 1:
        return f"Source: {sources[0]}"
    
    return f"Sources: {', '.join(sources)}"


