# Modular RAG Pipeline

A comprehensive, modular Retrieval-Augmented Generation (RAG) pipeline with support for multiple vector databases, advanced retrieval techniques, and semantic document processing.

## Features

- **Multi-format Document Processing**: PDF text, images (OCR), and table extraction
- **Semantic Chunking**: Advanced text chunking based on sentence similarity
- **Multiple Vector Databases**: Support for MongoDB Atlas Vector Search and Milvus
- **Advanced Retrieval**: BM25 and MMR reranking algorithms
- **Benchmarking**: Performance comparison across different vector databases
- **LLM Integration**: Flexible LLM pipeline with customizable prompts
- **Document Generation**: Automated DOCX report generation

## Project Structure

```
rag_pipeline/
├── __init__.py                 # Main package initialization
├── config.py                   # Configuration management
├── utils.py                    # Utility functions
├── core/
│   ├── __init__.py
│   └── pipeline.py            # Main pipeline orchestrator
├── models/
│   ├── __init__.py
│   └── data_models.py         # Data structures
├── processing/
│   ├── __init__.py
│   ├── chunking.py            # Semantic chunking
│   └── pdf_processor.py       # PDF processing
├── vector_db/
│   ├── __init__.py
│   ├── base.py                # Abstract base class
│   ├── mongodb.py             # MongoDB implementation
│   └── milvus.py              # Milvus implementation
├── retrieval/
│   ├── __init__.py
│   └── pipeline.py            # Retrieval and reranking
├── llm/
│   ├── __init__.py
│   └── pipeline.py            # LLM processing
└── output/
    ├── __init__.py
    └── document_generator.py   # DOCX generation
```

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export OPENAI_API_KEY="your-openai-api-key"
export MONGODB_CONNECTION_STRING="your-mongodb-connection"
export MILVUS_HOST="your-milvus-host"
export MILVUS_PORT="your-milvus-port"
```

## Quick Start

```python
from rag_pipeline import CompleteRAGPipeline

# Initialize the pipeline
rag_pipeline = CompleteRAGPipeline()

# Process PDFs and run complete pipeline
pdf_paths = ["document1.pdf", "document2.pdf"]
query = "What are the main findings from these documents?"

results = rag_pipeline.run_complete_pipeline(
    pdf_paths=pdf_paths,
    query=query,
    output_filename="analysis_report.docx"
)

print(f"Processed {results['chunks_processed']} chunks")
print(f"Generated report: {results['output_file']}")
```

## Detailed Usage

### 1. Document Processing

```python
from rag_pipeline.processing import PDFProcessor

processor = PDFProcessor()
chunks = processor.process_pdf("document.pdf")
```

### 2. Vector Database Setup

```python
from rag_pipeline.vector_db import MilvusVectorDB, MongoVectorDB

# Milvus
milvus_db = MilvusVectorDB(host="localhost", port="19530")
milvus_db.create_index("HNSW")

# MongoDB Atlas
mongo_db = MongoVectorDB(
    connection_string="mongodb+srv://...",
    database_name="rag_db",
    collection_name="documents"
)
```

### 3. Retrieval Pipeline

```python
from rag_pipeline.retrieval import RetrievalPipeline

retrieval = RetrievalPipeline()
retrieval.add_database("milvus", milvus_db)
retrieval.setup_bm25(chunks)

# Benchmark different databases
results = retrieval.benchmark_retrieval("your query")

# Rerank results
reranked = retrieval.rerank_bm25("your query", candidate_chunks)
```

### 4. LLM Integration

```python
from rag_pipeline.llm import LLMPipeline

llm = LLMPipeline(model_name="gpt-3.5-turbo")
response = llm.generate_response(context, question)
```

### 5. Document Generation

```python
from rag_pipeline.output import DocumentGenerator

generator = DocumentGenerator()
generator.create_docx(response, "output.docx")
```

## Configuration

The pipeline uses a comprehensive configuration system:

```python
from rag_pipeline.config import RAGConfig

config = RAGConfig()
config.embedding.model_name = "sentence-transformers/all-MiniLM-L6-v2"
config.chunking.max_chunk_size = 512
config.retrieval.top_k = 10
```

## Vector Database Support

### Milvus
- Multiple index types: FLAT, HNSW, IVF
- High-performance vector similarity search
- Horizontal scalability

### MongoDB Atlas Vector Search
- Native MongoDB integration
- Cloud-managed service
- Rich metadata querying

## Advanced Features

### Semantic Chunking
- Sentence similarity-based chunking
- Maintains semantic coherence
- Configurable similarity thresholds

### Reranking Algorithms
- **BM25**: Traditional relevance scoring
- **MMR**: Maximal Marginal Relevance for diversity

### Benchmarking
- Performance comparison across vector databases
- Retrieval time measurement
- Result quality metrics

## Dependencies

Key dependencies include:
- `sentence-transformers`: Embedding models
- `pymilvus`: Milvus vector database
- `pymongo`: MongoDB integration
- `transformers`: NLP models
- `langchain`: LLM orchestration
- `python-docx`: Document generation

See `requirements.txt` for complete list.

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for LLM integration
- `MONGODB_CONNECTION_STRING`: MongoDB Atlas connection string
- `MILVUS_HOST`: Milvus server host
- `MILVUS_PORT`: Milvus server port

## Logging

The pipeline includes comprehensive logging:
- Console output for real-time monitoring
- File logging (`rag_pipeline.log`) for debugging
- Configurable log levels

## Error Handling

- Robust error handling throughout the pipeline
- Graceful degradation when services are unavailable
- Detailed error messages and logging

## Contributing

1. Follow the modular architecture
2. Add comprehensive docstrings
3. Include error handling
4. Update tests and documentation

## License

This project is provided as-is for educational and research purposes.

## Troubleshooting

### Common Issues

1. **Tesseract not found**: Install tesseract-ocr system package
2. **Milvus connection error**: Ensure Milvus server is running
3. **Memory issues**: Reduce batch sizes in configuration
4. **Import errors**: Check all dependencies are installed

### Performance Tips

1. Use HNSW index for better query performance
2. Adjust chunk sizes based on your documents
3. Enable GPU acceleration for embeddings if available
4. Use appropriate similarity thresholds for chunking