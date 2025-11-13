"""
Vector Store Management
Handles embedding generation and vector database operations
"""

# CRITICAL: Set environment variables BEFORE any torch-related imports
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Disable CUDA completely
os.environ['TORCH_USE_CUDA_DSA'] = '0'   # Disable CUDA DSA
os.environ['TORCH_DEVICE'] = 'cpu'       # Force CPU device

# Import torch FIRST and force CPU mode
import torch
# Force CPU mode - compatible with all torch versions
if hasattr(torch, 'cuda'):
    # Monkey patch to always return False for CUDA availability
    original_is_available = torch.cuda.is_available
    torch.cuda.is_available = lambda: False
    # Also disable CUDA device count
    if hasattr(torch.cuda, 'device_count'):
        original_device_count = torch.cuda.device_count
        torch.cuda.device_count = lambda: 0

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from pathlib import Path
import hashlib

# Import SentenceTransformer after torch is configured
from sentence_transformers import SentenceTransformer


class VectorStore:
    """Manages vector embeddings and semantic search"""
    
    def __init__(self, persist_directory: str = "./vector_db", model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            model_name: Sentence transformer model name
        """
        self.persist_directory = persist_directory
        self.model_name = model_name
        
        # Initialize embedding model with CPU-only mode
        print(f"Loading embedding model: {model_name}")
        
        # Multiple fallback strategies for device compatibility
        last_error = None
        
        # Strategy 1: Load with explicit CPU device
        try:
            self.embedding_model = SentenceTransformer(
                model_name,
                device='cpu'
            )
            print("Model loaded successfully with explicit CPU device")
        except (NotImplementedError, Exception) as e1:
            last_error = e1
            print(f"Strategy 1 failed: {e1}")
            
            # Strategy 2: Patch torch.nn.Module.to to prevent device conversion errors
            try:
                # Save original methods
                original_to = torch.nn.Module.to
                original_apply = torch.nn.Module._apply
                
                # Create a safe wrapper that prevents NotImplementedError
                def safe_to(self, device=None, *args, **kwargs):
                    """Safe wrapper that prevents device conversion errors"""
                    if device is None:
                        return self
                    # Always convert to CPU to avoid device errors
                    if str(device).startswith('cuda') or str(device).startswith('gpu'):
                        device = 'cpu'
                    try:
                        return original_to(self, device, *args, **kwargs)
                    except NotImplementedError:
                        # If conversion fails, just return self (already on CPU)
                        return self
                
                def safe_apply(self, fn):
                    """Safe _apply that handles device conversion gracefully"""
                    try:
                        return original_apply(self, fn)
                    except NotImplementedError:
                        # If device conversion fails, the model is likely already on CPU
                        # Just return self to continue initialization
                        return self
                
                # Apply patches
                torch.nn.Module.to = safe_to
                torch.nn.Module._apply = safe_apply
                
                # Now try loading the model
                self.embedding_model = SentenceTransformer(model_name)
                
                # Restore original methods
                torch.nn.Module.to = original_to
                torch.nn.Module._apply = original_apply
                
                print("Model loaded successfully with patched device handling")
            except (NotImplementedError, Exception) as e2:
                last_error = e2
                print(f"Strategy 2 failed: {e2}")
                
                # Strategy 3: Load with minimal device interaction using model_kwargs
                try:
                    # Use model_kwargs to avoid device issues
                    self.embedding_model = SentenceTransformer(
                        model_name,
                        model_kwargs={'torch_dtype': torch.float32}
                    )
                    # Don't try to move to device - just use as-is
                    print("Model loaded successfully with model_kwargs")
                except (NotImplementedError, Exception) as e3:
                    last_error = e3
                    print(f"Strategy 3 failed: {e3}")
                    raise RuntimeError(
                        f"Failed to load embedding model after all strategies. "
                        f"Last error: {last_error}. "
                        f"This may be due to PyTorch/device compatibility issues. "
                        f"Please ensure torch>=2.0.0 is installed and compatible with your system."
                    ) from e3
        
        # Initialize ChromaDB client
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="campus_compass",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _generate_id(self, text: str, metadata: Dict) -> str:
        """Generate unique ID for a chunk"""
        content = f"{text}_{metadata.get('source', '')}_{metadata.get('chunk_index', 0)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_documents(self, chunks: List[Dict]):
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of dicts with 'text' and 'metadata' keys
        """
        if not chunks:
            return
        
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        ids = [self._generate_id(chunk['text'], chunk['metadata']) for chunk in chunks]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(texts)} chunks to vector store")
    
    def search(self, query: str, n_results: int = 5, prioritize_source: Optional[str] = None) -> List[Dict]:
        """
        Search for similar chunks
        
        Args:
            query: Search query
            n_results: Number of results to return
            prioritize_source: If provided, prioritize chunks from this source (filename)
            
        Returns:
            List of dicts with 'text', 'metadata', and 'distance' keys
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search in ChromaDB - retrieve more results if we need to prioritize
        search_n = n_results * 2 if prioritize_source else n_results
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=search_n
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        # If prioritizing a source, reorder to put that source first
        if prioritize_source and formatted_results:
            prioritized = []
            others = []
            source_name = Path(prioritize_source).name if prioritize_source else None
            
            for chunk in formatted_results:
                chunk_source = chunk['metadata'].get('source', '')
                if source_name and chunk_source == source_name:
                    prioritized.append(chunk)
                else:
                    others.append(chunk)
            
            # Combine: prioritized chunks first, then others, limit to n_results
            formatted_results = (prioritized + others)[:n_results]
        
        return formatted_results
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.client.delete_collection(name="campus_compass")
            self.collection = self.client.get_or_create_collection(
                name="campus_compass",
                metadata={"hnsw:space": "cosine"}
            )
            print("Vector store cleared")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        try:
            # Check if collection exists
            if self.collection is None:
                return 0
            return self.collection.count()
        except Exception as e:
            # If collection doesn't exist or any error occurs, return 0
            print(f"Error getting collection count: {e}")
            # Try to recreate collection if it was deleted
            try:
                self.collection = self.client.get_or_create_collection(
                    name="campus_compass",
                    metadata={"hnsw:space": "cosine"}
                )
                return self.collection.count()
            except:
                return 0


