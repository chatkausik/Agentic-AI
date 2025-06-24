import logging
from typing import List, Tuple
import pymongo
from pymongo import MongoClient

from .base import VectorDatabase
from ..models.data_models import DocumentChunk

logger = logging.getLogger(__name__)

class MongoVectorDB(VectorDatabase):
    """MongoDB Atlas Vector Search implementation"""
    
    def __init__(self, connection_string: str, database_name: str, collection_name: str):
        super().__init__()
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        
    def create_index(self, index_type: str = "vector"):
        """Create vector search index in MongoDB"""
        if index_type == "vector":
            index_definition = {
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": 384,  # for all-MiniLM-L6-v2
                        "similarity": "cosine"
                    }
                ]
            }
            # MongoDB Atlas Vector Search index creation would be done via Atlas UI
            logger.info("Vector index definition created for MongoDB")
    
    def insert_documents(self, chunks: List[DocumentChunk]):
        """Insert documents into MongoDB"""
        documents = []
        for chunk in chunks:
            doc = {
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "metadata": chunk.metadata,
                "embedding": chunk.embedding.tolist()
            }
            documents.append(doc)
        
        self.collection.insert_many(documents)
        logger.info(f"Inserted {len(documents)} documents into MongoDB")
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[DocumentChunk, float]]:
        """Search using MongoDB vector search"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_embedding.tolist(),
                    "path": "embedding",
                    "numCandidates": top_k * 2,
                    "limit": top_k,
                    "index": "vector_index"
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        search_results = []
        for result in results:
            chunk = DocumentChunk(
                text=result["text"],
                metadata=result["metadata"],
                chunk_id=result["chunk_id"]
            )
            score = result.get("score", 0.0)
            search_results.append((chunk, score))
        
        return search_results