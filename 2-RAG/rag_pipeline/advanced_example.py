"""
Advanced example demonstrating individual module usage
"""

import logging
from rag_pipeline.config import RAGConfig
from rag_pipeline.utils import setup_logging, validate_pdf_files
from rag_pipeline.processing import PDFProcessor, SemanticChunker
from rag_pipeline.vector_db import MilvusVectorDB
from rag_pipeline.retrieval import RetrievalPipeline
from rag_pipeline.llm import LLMPipeline
from rag_pipeline.output import DocumentGenerator

def advanced_example():
    """Demonstrate advanced usage of individual modules"""
    
    # Setup configuration and logging
    config = RAGConfig()
    logger = setup_logging(config.log_level)
    
    logger.info("Starting advanced RAG pipeline example")
    
    # 1. Document Processing Example
    logger.info("=== Document Processing ===")
    pdf_processor = PDFProcessor()
    
    # Process individual PDFs
    pdf_paths = validate_pdf_files(["2-RAG/llama2-bf0a30209b224e26e31087559688ce81.pdf"])
    all_chunks = []
    
    for pdf_path in pdf_paths:
        chunks = pdf_processor.process_pdf(pdf_path)
        all_chunks.extend(chunks)
        logger.info(f"Processed {pdf_path}: {len(chunks)} chunks")
    
    # 2. Custom Chunking Example
    logger.info("=== Custom Chunking ===")
    chunker = SemanticChunker(model_name=config.embedding.model_name)
    
    sample_text = "This is a sample document. It contains multiple sentences. Each sentence has different semantic meaning."
    custom_chunks = chunker.chunk_text(
        sample_text, 
        max_chunk_size=config.chunking.max_chunk_size,
        similarity_threshold=config.chunking.similarity_threshold
    )
    logger.info(f"Created {len(custom_chunks)} custom chunks")
    
    # 3. Vector Database Comparison
    logger.info("=== Vector Database Setup ===")
    
    # Setup Milvus with different index types
    milvus_dbs = {}
    for index_type in ["FLAT", "HNSW", "IVF"]:
        db = MilvusVectorDB(
            host=config.vector_db.milvus_host,
            port=config.vector_db.milvus_port,
            collection_name=f"docs_{index_type.lower()}"
        )
        db.create_embeddings(all_chunks[:10])  # Use subset for demo
        db.create_index(index_type)
        db.insert_documents(all_chunks[:10])
        milvus_dbs[index_type] = db
        logger.info(f"Setup Milvus with {index_type} index")
    
    # 4. Advanced Retrieval Pipeline
    logger.info("=== Advanced Retrieval ===")
    retrieval = RetrievalPipeline()
    
    # Add multiple databases
    for index_type, db in milvus_dbs.items():
        retrieval.add_database(f"milvus_{index_type.lower()}", db)
    
    # Setup BM25
    retrieval.setup_bm25(all_chunks)
    
    # Benchmark query
    query = "What are the key features of LLaMA2?"
    benchmark_results = retrieval.benchmark_retrieval(query, top_k=5)
    
    logger.info("Benchmark results:")
    for db_name, results in benchmark_results.items():
        logger.info(f"{db_name}: {results['retrieval_time']:.4f}s, {results['num_results']} results")
    
    # Get best performing database
    fastest_db = min(benchmark_results.keys(), key=lambda x: benchmark_results[x]['retrieval_time'])
    best_results = benchmark_results[fastest_db]['results']
    
    # Extract candidate chunks
    candidate_chunks = [result[0] for result in best_results]
    
    # Apply different reranking strategies
    bm25_reranked = retrieval.rerank_bm25(query, candidate_chunks, top_k=3)
    mmr_reranked = retrieval.mmr_rerank(query, candidate_chunks, lambda_param=0.7, top_k=3)
    
    logger.info(f"BM25 reranking: {len(bm25_reranked)} results")
    logger.info(f"MMR reranking: {len(mmr_reranked)} results")
    
    # 5. LLM Processing with Custom Prompt
    logger.info("=== LLM Processing ===")
    llm = LLMPipeline(model_name=config.llm.model_name)
    
    # Create context from reranked results
    context_texts = [chunk.text for chunk, _ in bm25_reranked]
    context = "\n\n".join(context_texts)
    
    response = llm.generate_response(context, query)
    logger.info("Generated LLM response")
    
    # 6. Document Generation with Metadata
    logger.info("=== Document Generation ===")
    doc_generator = DocumentGenerator()
    
    # Enhanced content with metadata
    enhanced_content = f"""
# RAG Pipeline Analysis Report

## Query
{query}

## Processing Summary
- Total chunks processed: {len(all_chunks)}
- Fastest database: {fastest_db}
- Reranking methods applied: BM25, MMR

## Results
{response}

## Technical Details
- Embedding model: {config.embedding.model_name}
- Chunk size: {config.chunking.max_chunk_size}
- Similarity threshold: {config.chunking.similarity_threshold}
"""
    
    output_file = doc_generator.create_docx(enhanced_content, "advanced_analysis.docx")
    logger.info(f"Generated enhanced report: {output_file}")
    
    return {
        "chunks_processed": len(all_chunks),
        "databases_tested": list(milvus_dbs.keys()),
        "benchmark_results": benchmark_results,
        "fastest_db": fastest_db,
        "output_file": output_file
    }

if __name__ == "__main__":
    results = advanced_example()
    print("\n=== Advanced Example Results ===")
    print(f"Chunks processed: {results['chunks_processed']}")
    print(f"Databases tested: {results['databases_tested']}")
    print(f"Fastest database: {results['fastest_db']}")
    print(f"Output file: {results['output_file']}")