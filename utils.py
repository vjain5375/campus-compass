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
    """Get list of all document files in documents directory (root only, no subdirectories)"""
    docs_dir = ensure_documents_directory()
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
    
    # Only look in root directory, not subdirectories (since we only allow single file uploads)
    files = []
    seen_paths = set()  # Track seen files to avoid duplicates
    
    # Get all files in root directory only
    for file_path in docs_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            # Use absolute resolved path for deduplication
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


