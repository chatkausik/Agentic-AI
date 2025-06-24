import logging
from typing import List, Dict, Any

from ..processing.pdf_processor import PDFProcessor
from ..retrieval.pipeline import RetrievalPipeline
from ..llm.pipeline import LLMPipeline
from ..output.document_generator import DocumentGenerator
from ..vector_db.milvus import MilvusVectorDB
from ..vector_db.mongodb import MongoVectorDB
from ..models.data_models import DocumentChunk

logger = logging.getLogger(__name__)

class CompleteRAGPipeline:
    """Complete RAG pipeline orchestrator"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.retrieval_pipeline = RetrievalPipeline()
        self.llm_pipeline = LLMPipeline()
        self.doc_generator = DocumentGenerator()
        self.chunks = []
        
    def process_pdfs(self, pdf_paths: List[str]) -> List[DocumentChunk]:
        """Process multiple PDFs"""
        all_chunks = []
        
        for pdf_path in pdf_paths:
            chunks = self.pdf_processor.process_pdf(pdf_path)
            all_chunks.extend(chunks)
            
        self.chunks = all_chunks
        logger.info(f"Processed {len(pdf_paths)} PDFs, created {len(all_chunks)} chunks")
        
        return all_chunks
    
    def setup_vector_databases(self):
        """Setup multiple vector databases"""
        # MongoDB setup (requires connection string)
        # mongo_db = MongoVectorDB("mongodb://localhost:27017", "rag_db", "documents")
        
        # Milvus setup
        milvus_db = MilvusVectorDB()
        
        # Create embeddings
        self.chunks = milvus_db.create_embeddings(self.chunks)
        
        # Setup databases
        # self.retrieval_pipeline.add_database("mongodb", mongo_db)
        self.retrieval_pipeline.add_database("milvus", milvus_db)
        
        # Create different indices
        for index_type in ["FLAT", "HNSW", "IVF"]:
            milvus_db.create_index(index_type)
            
        # Insert documents
        milvus_db.insert_documents(self.chunks)
        
        # Setup BM25
        self.retrieval_pipeline.setup_bm25(self.chunks)
        
    def run_complete_pipeline(self, pdf_paths: List[str], query: str, output_filename: str = "rag_output.docx"):
        """Run the complete RAG pipeline"""
        logger.info("Starting complete RAG pipeline")
        
        # Step 1: Process PDFs
        chunks = self.process_pdfs(pdf_paths)
        
        # Step 2: Setup vector databases
        self.setup_vector_databases()
        
        # Step 3: Benchmark retrieval
        logger.info("Benchmarking retrieval systems")
        benchmark_results = self.retrieval_pipeline.benchmark_retrieval(query)
        
        for db_name, results in benchmark_results.items():
            logger.info(f"{db_name}: {results['retrieval_time']:.4f}s, {results['num_results']} results")
        
        # Step 4: Get best results and rerank
        best_db = min(benchmark_results.keys(), key=lambda x: benchmark_results[x]['retrieval_time'])
        best_results = benchmark_results[best_db]['results']
        
        # Extract chunks for reranking
        candidate_chunks = [result[0] for result in best_results]
        
        # BM25 reranking
        bm25_reranked = self.retrieval_pipeline.rerank_bm25(query, candidate_chunks)
        
        # MMR reranking
        mmr_reranked = self.retrieval_pipeline.mmr_rerank(query, candidate_chunks)
        
        # Step 5: Generate context
        context_texts = [chunk.text for chunk, _ in bm25_reranked[:5]]
        context = "\n\n".join(context_texts)
        
        # Step 6: Generate LLM response
        response = self.llm_pipeline.generate_response(context, query)
        
        # Step 7: Create DOCX output
        self.doc_generator.create_docx(response, output_filename)
        
        # Return comprehensive results
        return {
            "chunks_processed": len(chunks),
            "benchmark_results": benchmark_results,
            "fastest_db": best_db,
            "reranked_results": {
                "bm25": bm25_reranked,
                "mmr": mmr_reranked
            },
            "llm_response": response,
            "output_file": output_filename
        }