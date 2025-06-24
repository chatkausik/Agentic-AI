"""
Example usage and testing script for the RAG pipeline
"""

import logging
from rag_pipeline import CompleteRAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate the pipeline"""
    
    # Initialize pipeline
    rag_pipeline = CompleteRAGPipeline()
    
    # Example PDF paths (you would provide actual paths)
    pdf_paths = [
        "document1.pdf",
        "document2.pdf", 
        "document3.pdf"
    ]
    
    # Example query
    query = "What are the main findings and recommendations from the analyzed documents?"
    
    try:
        # Run complete pipeline
        results = rag_pipeline.run_complete_pipeline(pdf_paths, query, "comprehensive_analysis.docx")
        
        print("=== RAG Pipeline Results ===")
        print(f"Processed chunks: {results['chunks_processed']}")
        print(f"Fastest database: {results['fastest_db']}")
        print(f"Output file: {results['output_file']}")
        
        print("\n=== Benchmark Results ===")
        for db_name, metrics in results['benchmark_results'].items():
            print(f"{db_name}: {metrics['retrieval_time']:.4f}s")
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()