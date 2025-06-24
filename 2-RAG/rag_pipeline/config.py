"""
Configuration settings for the RAG pipeline
"""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EmbeddingConfig:
    """Configuration for embedding models"""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    dimension: int = 384
    batch_size: int = 32

@dataclass
class ChunkingConfig:
    """Configuration for text chunking"""
    max_chunk_size: int = 512
    similarity_threshold: float = 0.7
    overlap_size: int = 50

@dataclass
class VectorDBConfig:
    """Configuration for vector databases"""
    # MongoDB settings
    mongodb_connection_string: str = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
    mongodb_database: str = "rag_db"
    mongodb_collection: str = "documents"
    
    # Milvus settings
    milvus_host: str = os.getenv("MILVUS_HOST", "localhost")
    milvus_port: str = os.getenv("MILVUS_PORT", "19530")
    milvus_collection: str = "documents"
    
    # Index settings
    default_index_type: str = "HNSW"

@dataclass
class LLMConfig:
    """Configuration for LLM settings"""
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

@dataclass
class RetrievalConfig:
    """Configuration for retrieval settings"""
    top_k: int = 10
    rerank_top_k: int = 5
    mmr_lambda: float = 0.7
    enable_bm25: bool = True
    enable_mmr: bool = True

@dataclass
class RAGConfig:
    """Main configuration class for RAG pipeline"""
    embedding: EmbeddingConfig = EmbeddingConfig()
    chunking: ChunkingConfig = ChunkingConfig()
    vector_db: VectorDBConfig = VectorDBConfig()
    llm: LLMConfig = LLMConfig()
    retrieval: RetrievalConfig = RetrievalConfig()
    
    # General settings
    log_level: str = "INFO"
    temp_dir: str = "./temp"
    output_dir: str = "./output"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "embedding": self.embedding.__dict__,
            "chunking": self.chunking.__dict__,
            "vector_db": self.vector_db.__dict__,
            "llm": self.llm.__dict__,
            "retrieval": self.retrieval.__dict__,
            "log_level": self.log_level,
            "temp_dir": self.temp_dir,
            "output_dir": self.output_dir
        }