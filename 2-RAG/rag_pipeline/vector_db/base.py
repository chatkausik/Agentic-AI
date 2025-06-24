from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

from ..models.data_models import DocumentChunk

class VectorDatabase(ABC):
    """Abstract base class for vector databases"""
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
        
    def create_embeddings(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Create embeddings for chunks"""
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
            
        return chunks
    
    @abstractmethod
    def create_index(self, index_type: str):
        """Create different types of indices"""
        pass
    
    @abstractmethod
    def insert_documents(self, chunks: List[DocumentChunk]):
        """Insert documents into vector database"""
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 10) -> List[Tuple[DocumentChunk, float]]:
        """Search for similar documents"""
        pass