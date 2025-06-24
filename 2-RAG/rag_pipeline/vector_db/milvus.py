import logging
from typing import List, Tuple
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

from .base import VectorDatabase
from ..models.data_models import DocumentChunk

logger = logging.getLogger(__name__)

class MilvusVectorDB(VectorDatabase):
    """Milvus vector database implementation"""
    
    def __init__(self, host: str = "localhost", port: str = "19530", collection_name: str = "documents"):
        super().__init__()
        connections.connect("default", host=host, port=port)
        self.collection_name = collection_name
        self.collection = None
        
    def create_index(self, index_type: str = "HNSW"):
        """Create different types of indices in Milvus"""
        if not self.collection:
            self._create_collection()
            
        index_params = {
            "FLAT": {"index_type": "FLAT", "metric_type": "L2"},
            "HNSW": {"index_type": "HNSW", "metric_type": "L2", "params": {"M": 8, "efConstruction": 64}},
            "IVF": {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 100}}
        }
        
        if index_type in index_params:
            self.collection.create_index("embedding", index_params[index_type])
            logger.info(f"Created {index_type} index in Milvus")
    
    def _create_collection(self):
        """Create Milvus collection"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=200),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
        ]
        
        schema = CollectionSchema(fields, "Document chunks collection")
        self.collection = Collection(self.collection_name, schema)
        
    def insert_documents(self, chunks: List[DocumentChunk]):
        """Insert documents into Milvus"""
        if not self.collection:
            self._create_collection()
            
        data = [
            [chunk.chunk_id for chunk in chunks],
            [chunk.text[:65535] for chunk in chunks],  # Truncate if too long
            [chunk.embedding.tolist() for chunk in chunks]
        ]
        
        self.collection.insert(data)
        self.collection.flush()
        logger.info(f"Inserted {len(chunks)} documents into Milvus")
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[DocumentChunk, float]]:
        """Search using Milvus"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        
        results = self.collection.search(
            [query_embedding.tolist()], 
            "embedding", 
            search_params, 
            limit=top_k,
            output_fields=["chunk_id", "text"]
        )
        
        search_results = []
        for hits in results:
            for hit in hits:
                chunk = DocumentChunk(
                    text=hit.entity.get("text"),
                    metadata={},
                    chunk_id=hit.entity.get("chunk_id")
                )
                search_results.append((chunk, hit.score))
        
        return search_results