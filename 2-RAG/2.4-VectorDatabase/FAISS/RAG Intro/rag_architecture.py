"""
RAG (Retrieval-Augmented Generation) Architecture
A comprehensive implementation with document loading, vector storage, and question-answering capabilities
"""

import os
import faiss
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class DocumentProcessor:
    """Handles document loading and text splitting"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load PDF documents"""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    def load_text(self, file_path: str) -> List[Document]:
        """Load text documents"""
        loader = TextLoader(file_path)
        return loader.load()
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)
    
    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """Process multiple documents"""
        all_documents = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: File not found - {file_path}")
                continue
                
            if file_path.endswith('.pdf'):
                docs = self.load_pdf(file_path)
            elif file_path.endswith('.txt'):
                docs = self.load_text(file_path)
            else:
                print(f"Warning: Unsupported file type - {file_path}")
                continue
            
            all_documents.extend(docs)
        
        # Split documents
        split_docs = self.split_documents(all_documents)
        print(f"Processed {len(all_documents)} documents into {len(split_docs)} chunks")
        
        return split_docs


class VectorStore:
    """Handles vector storage and retrieval operations"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", index_type: str = "IP"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.embedding_dimension = 384  # Default for all-MiniLM-L6-v2
        self.index_type = index_type
        self.vector_store = None
        
    def create_index(self) -> faiss.Index:
        """Create FAISS index based on type"""
        if self.index_type == "IP":
            return faiss.IndexFlatIP(self.embedding_dimension)
        elif self.index_type == "L2":
            return faiss.IndexFlatL2(self.embedding_dimension)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
    
    def build_vector_store(self, documents: List[Document]) -> None:
        """Build vector store from documents"""
        index = self.create_index()
        
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        
        # Add documents to vector store
        self.vector_store.add_documents(documents=documents)
        print(f"Added {len(documents)} documents to vector store")
    
    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Document]:
        """Perform similarity search"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call build_vector_store first.")
        
        if filter:
            return self.vector_store.similarity_search(query, k=k, filter=filter)
        else:
            return self.vector_store.similarity_search(query, k=k)
    
    def get_retriever(self, k: int = 5):
        """Get retriever for RAG chain"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call build_vector_store first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
    
    def save_local(self, folder_path: str) -> None:
        """Save vector store locally"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")
        
        self.vector_store.save_local(folder_path)
        print(f"Vector store saved to {folder_path}")
    
    def load_local(self, folder_path: str) -> None:
        """Load vector store from local storage"""
        self.vector_store = FAISS.load_local(
            folder_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        print(f"Vector store loaded from {folder_path}")


class RAGChain:
    """Handles the RAG question-answering chain"""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = ChatGoogleGenerativeAI(model=model_name)
        self.prompt = hub.pull("rlm/rag-prompt")
        self.chain = None
    
    def format_docs(self, docs: List[Document]) -> str:
        """Format documents for the prompt"""
        return "\n\n".join(doc.page_content for doc in docs)
    
    def build_chain(self, retriever) -> None:
        """Build the RAG chain"""
        self.chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.model
            | StrOutputParser()
        )
        print("RAG chain built successfully")
    
    def ask(self, question: str) -> str:
        """Ask a question using the RAG chain"""
        if not self.chain:
            raise ValueError("Chain not built. Call build_chain first.")
        
        return self.chain.invoke(question)


class RAGSystem:
    """Main RAG system that orchestrates all components"""
    
    def __init__(self, 
                 embedding_model: str = "all-MiniLM-L6-v2",
                 llm_model: str = "gemini-1.5-flash",
                 chunk_size: int = 500,
                 chunk_overlap: int = 50,
                 index_type: str = "IP"):
        
        self.document_processor = DocumentProcessor(chunk_size, chunk_overlap)
        self.vector_store = VectorStore(embedding_model, index_type)
        self.rag_chain = RAGChain(llm_model)
        self.retriever = None
        
    def setup(self, file_paths: List[str], retriever_k: int = 10) -> None:
        """Setup the complete RAG system"""
        print("Setting up RAG system...")
        
        # Process documents
        documents = self.document_processor.process_documents(file_paths)
        
        # Build vector store
        self.vector_store.build_vector_store(documents)
        
        # Get retriever
        self.retriever = self.vector_store.get_retriever(k=retriever_k)
        
        # Build RAG chain
        self.rag_chain.build_chain(self.retriever)
        
        print("RAG system setup complete!")
    
    def query(self, question: str) -> str:
        """Query the RAG system"""
        if not self.retriever:
            raise ValueError("System not setup. Call setup() first.")
        
        return self.rag_chain.ask(question)
    
    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """Search documents without LLM generation"""
        return self.vector_store.similarity_search(query, k=k)
    
    def save_system(self, folder_path: str) -> None:
        """Save the vector store"""
        self.vector_store.save_local(folder_path)
    
    def load_system(self, folder_path: str, retriever_k: int = 10) -> None:
        """Load a saved system"""
        self.vector_store.load_local(folder_path)
        self.retriever = self.vector_store.get_retriever(k=retriever_k)
        self.rag_chain.build_chain(self.retriever)
        print("RAG system loaded successfully!")


def main():
    """Main function demonstrating RAG usage"""
    # Load environment variables
    load_dotenv()
    
    # Ensure required environment variables are set
    if not os.getenv("HF_TOKEN"):
        print("Warning: HF_TOKEN not found in environment variables")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables")
        return
    
    # Initialize RAG System
    rag_system = RAGSystem(
        embedding_model="all-MiniLM-L6-v2",
        llm_model="gemini-1.5-flash",
        chunk_size=500,
        chunk_overlap=50,
        index_type="IP"
    )
    
    # Define file paths (update these paths as needed)
    file_paths = [
        "/Users/kausik/Desktop/Agentic-AI/2-RAG/llama2-bf0a30209b224e26e31087559688ce81.pdf",
        "/Users/kausik/Desktop/Agentic-AI/3-langgraph/data2/mental_health.pdf",
        "/Users/kausik/Desktop/Agentic-AI/3-langgraph/data2/usa.txt"
    ]
    
    try:
        # Setup the system
        rag_system.setup(file_paths, retriever_k=10)
        
        # Example queries
        questions = [
            "What is the Llama model?",
            "Tell me about mental health",
            "What information do you have about the USA?"
        ]
        
        print("\n" + "="*50)
        print("RAG SYSTEM DEMONSTRATION")
        print("="*50)
        
        for question in questions:
            print(f"\nQ: {question}")
            print("-" * 40)
            try:
                answer = rag_system.query(question)
                print(f"A: {answer}")
            except Exception as e:
                print(f"Error answering question: {e}")
        
        # Demonstrate document search
        print(f"\n{'='*50}")
        print("DOCUMENT SEARCH DEMONSTRATION")
        print("="*50)
        
        search_query = "artificial intelligence"
        docs = rag_system.search_documents(search_query, k=3)
        print(f"\nTop 3 documents for '{search_query}':")
        for i, doc in enumerate(docs, 1):
            print(f"\n{i}. {doc.page_content[:200]}...")
        
        # Save the system
        save_path = "rag_index"
        rag_system.save_system(save_path)
        print(f"\nSystem saved to {save_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your file paths and environment variables.")


if __name__ == "__main__":
    main()