import os
from langchain_community.document_loaders import (
    DirectoryLoader, 
    PyPDFLoader, 
    TextLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from config import DATA_DIRECTORY, SUPPORTED_EXTENSIONS, EMBEDDINGS, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_K

def get_loader_for_extension(file_path):
    """Return appropriate loader based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return PyPDFLoader(file_path)
    elif ext == '.txt':
        return TextLoader(file_path, encoding='utf-8')
    elif ext in ['.docx', '.doc']:
        return Docx2txtLoader(file_path)
    elif ext in ['.ppt', '.pptx']:
        return UnstructuredPowerPointLoader(file_path)
    elif ext == '.csv':
        return CSVLoader(file_path)
    else:
        # Fallback to TextLoader for other text-based files
        try:
            return TextLoader(file_path, encoding='utf-8')
        except:
            print(f"Warning: Could not load {file_path} - unsupported format")
            return None

def load_documents():
    """Load and process documents from the data directory"""
    docs = []
    for ext in SUPPORTED_EXTENSIONS:
        try:
            if ext == '.pdf':
                loader = DirectoryLoader(DATA_DIRECTORY, glob=f"*{ext}", loader_cls=PyPDFLoader)
            elif ext == '.txt':
                loader = DirectoryLoader(DATA_DIRECTORY, glob=f"*{ext}", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
            elif ext in ['.docx', '.doc']:
                loader = DirectoryLoader(DATA_DIRECTORY, glob=f"*{ext}", loader_cls=Docx2txtLoader)
            elif ext in ['.ppt', '.pptx']:
                loader = DirectoryLoader(DATA_DIRECTORY, glob=f"*{ext}", loader_cls=UnstructuredPowerPointLoader)
            elif ext == '.csv':
                loader = DirectoryLoader(DATA_DIRECTORY, glob=f"*{ext}", loader_cls=CSVLoader)
            
            ext_docs = loader.load()
            docs.extend(ext_docs)
            print(f"Loaded {len(ext_docs)} documents with extension {ext}")
        except Exception as e:
            print(f"Warning: Failed to load {ext} files - {str(e)}")

    print(f"Total documents loaded: {len(docs)}")
    if not docs:
        print("No documents found! Please check the data directory and file formats.")
    
    return docs

def create_vector_store():
    """Create and return vector store with retriever"""
    docs = load_documents()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    new_docs = text_splitter.split_documents(docs)
    print(f"Documents split into {len(new_docs)} chunks")

    db = Chroma.from_documents(new_docs, EMBEDDINGS)
    retriever = db.as_retriever(search_kwargs={"k": RETRIEVER_K})
    
    return retriever

def format_docs(docs):
    """Helper function to format documents for RAG"""
    return "\n\n".join(doc.page_content for doc in docs)