import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment
load_dotenv()

# Model configurations
LLM_MODEL = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
EMBEDDINGS = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Data directory path
DATA_DIRECTORY = "/Users/kausik/Desktop/Agentic-AI/3-langgraph/data2"

# Supported file extensions
SUPPORTED_EXTENSIONS = ['.pdf', '.txt', '.docx', '.doc', '.ppt', '.pptx', '.csv']

# Text splitter configuration
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Validation configuration
MAX_RETRIES = 2
MIN_VALIDATION_SCORE = 70
FALLBACK_VALIDATION_SCORE = 40

# Search configuration
RETRIEVER_K = 3