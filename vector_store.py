"""
Vector Store Management
Handles embedding generation and vector database operations
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import hashlib


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
        
        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
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
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for similar chunks
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of dicts with 'text', 'metadata', and 'distance' keys
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
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
        return self.collection.count()


