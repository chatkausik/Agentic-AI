import time
import logging
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ..vector_db.base import VectorDatabase
from ..models.data_models import DocumentChunk

logger = logging.getLogger(__name__)

class RetrievalPipeline:
    """Complete retrieval pipeline with multiple vector databases and reranking"""
    
    def __init__(self):
        self.databases = {}
        self.bm25 = None
        self.corpus = []
        
    def add_database(self, name: str, db: VectorDatabase):
        """Add a vector database to the pipeline"""
        self.databases[name] = db
        
    def setup_bm25(self, chunks: List[DocumentChunk]):
        """Setup BM25 for reranking"""
        self.corpus = [chunk.text for chunk in chunks]
        tokenized_corpus = [doc.lower().split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
    def benchmark_retrieval(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """Benchmark retrieval across all databases"""
        results = {}
        
        for db_name, db in self.databases.items():
            start_time = time.time()
            search_results = db.search(query, top_k)
            end_time = time.time()
            
            results[db_name] = {
                "results": search_results,
                "retrieval_time": end_time - start_time,
                "num_results": len(search_results)
            }
            
        return results
    
    def rerank_bm25(self, query: str, candidates: List[DocumentChunk], top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """Rerank using BM25"""
        if not self.bm25:
            logger.warning("BM25 not initialized")
            return [(chunk, 0.0) for chunk in candidates[:top_k]]
            
        query_tokens = query.lower().split()
        candidate_texts = [chunk.text for chunk in candidates]
        
        # Get BM25 scores
        scores = []
        for text in candidate_texts:
            tokenized_text = text.lower().split()
            score = self.bm25.get_score(query_tokens, tokenized_text)
            scores.append(score)
        
        # Sort by BM25 score
        ranked_pairs = list(zip(candidates, scores))
        ranked_pairs.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_pairs[:top_k]
    
    def mmr_rerank(self, query: str, candidates: List[DocumentChunk], 
                   lambda_param: float = 0.7, top_k: int = 5) -> List[DocumentChunk]:
        """Maximal Marginal Relevance reranking"""
        if not candidates:
            return []
            
        # Get query embedding
        embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        query_embedding = embedding_model.encode([query])[0]
        
        # Get candidate embeddings
        candidate_embeddings = embedding_model.encode([chunk.text for chunk in candidates])
        
        selected = []
        remaining = list(range(len(candidates)))
        
        for _ in range(min(top_k, len(candidates))):
            mmr_scores = []
            
            for i in remaining:
                # Relevance score
                relevance = cosine_similarity([query_embedding], [candidate_embeddings[i]])[0][0]
                
                # Diversity score (max similarity to already selected)
                if selected:
                    selected_embeddings = [candidate_embeddings[j] for j in selected]
                    max_sim = max(cosine_similarity([candidate_embeddings[i]], selected_embeddings)[0])
                else:
                    max_sim = 0
                
                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim
                mmr_scores.append((i, mmr_score))
            
            # Select best MMR score
            best_idx = max(mmr_scores, key=lambda x: x[1])[0]
            selected.append(best_idx)
            remaining.remove(best_idx)
        
        return [candidates[i] for i in selected]