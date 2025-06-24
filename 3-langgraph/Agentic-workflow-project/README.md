# Agentic AI Workflow

A sophisticated AI workflow system that intelligently routes queries between RAG (document-based), Web search, and LLM responses with validation and retry mechanisms.

## 🎬 Demo Video

Check out this demo recording to see the application in action:

📹 **[Application Demo](data2/demo_video.mp4)**

*This recording demonstrates the key features and workflow of the Agentic AI system.*

## 🏗️ Project Structure

```
Agentic-workflow-project/
├── config.py              # Configuration and environment setup
├── models.py              # Pydantic models and type definitions
├── document_loader.py     # Document loading and vector store creation
├── nodes.py               # All workflow nodes and processing functions
├── workflow.py            # Workflow definition and compilation
├── utils.py               # Utility functions for formatting and metrics
├── app.py                 # Class-based application interface
├── main.py                # Command-line interface
├── streamlit_app.py       # Streamlit web interface
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── data2/                 # Document directory
    ├── mental_health.pdf
    └── usa.txt
```

## 🚀 Features

- **Intelligent Routing**: Automatically routes queries to the most appropriate source
- **Multi-Source Support**: 
  - 📚 RAG (Retrieval-Augmented Generation) for document-based queries
  - 🌐 Web search for real-time information
  - 🧠 LLM for general knowledge
- **Response Validation**: Comprehensive validation with scoring and retry mechanisms
- **Fallback Strategies**: RAG failure detection with web search fallback
- **Interactive Interfaces**: Both command-line and web-based interfaces
- **Conversation History**: Automatic saving and loading of query history

## 📋 Requirements

- Python 3.8+
- Google API key for Gemini (set in environment)
- Tavily API key for web search (set in environment)

## 🛠️ Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_google_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Prepare documents:**
   Place your documents (PDF, TXT, DOCX, PPT, CSV) in the `data2/` directory.

## 🎮 Usage

### Streamlit Web Interface (Recommended)

Launch the interactive web interface:
```bash
streamlit run streamlit_app.py
```

Features:
- 🎨 Beautiful, user-friendly interface
- 📊 Real-time validation metrics
- 💬 Conversation history sidebar
- 📈 Session statistics
- 💡 Example questions
- 🔄 Progress tracking during initialization

### Command Line Interface

**Single query:**
```bash
python main.py --query "What are symptoms of anxiety?"
```

**Interactive mode:**
```bash
python main.py --interactive
```

**Verbose output with validation details:**
```bash
python main.py --query "What's the GDP of USA?" --verbose
```

### Python API

```python
from app import AgenticWorkflowApp

# Initialize the application
app = AgenticWorkflowApp()
app.initialize()

# Ask a question
result = app.ask_question("What are effective treatments for depression?")

# Get conversation history
history = app.get_conversation_history(limit=5)
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Model Settings**: Change LLM model or embeddings
- **Data Directory**: Update document location
- **Validation Parameters**: Adjust scoring thresholds
- **Search Settings**: Modify retriever parameters

## 🧩 Module Overview

### Core Modules

- **`config.py`**: Environment setup, model configurations, and constants
- **`models.py`**: Pydantic models for type safety and state management
- **`document_loader.py`**: Handles document loading and vector store creation
- **`nodes.py`**: Contains all workflow nodes (Supervisor, RAG, Web, LLM, Validator)
- **`workflow.py`**: Defines and compiles the LangGraph workflow

### Interface Modules

- **`streamlit_app.py`**: Full-featured web interface with metrics and history
- **`main.py`**: Command-line interface with argument parsing
- **`app.py`**: Class-based Python API for programmatic usage

### Utility Modules

- **`utils.py`**: Helper functions for formatting, metrics, and data handling

## 🤖 How It Works

1. **Query Classification**: The Supervisor node classifies queries into categories
2. **Intelligent Routing**: Queries are routed to the most appropriate processor:
   - Mental health topics → RAG (document-based)
   - Real-time information → Web search
   - General knowledge → LLM
3. **Response Generation**: The selected node generates a response
4. **Validation**: Comprehensive validation with scoring (0-100)
5. **Retry Logic**: Failed responses trigger retries with adaptive strategies
6. **Fallback**: RAG failures automatically fallback to web search

## 📊 Validation Metrics

The system validates responses based on:
- Content quality and completeness
- Relevance to the original question
- Response structure and formatting
- Error detection and handling
- Source-specific validation rules

## 🎯 Example Queries

**Mental Health (RAG):**
- "What are effective treatments for depression?"
- "How can I manage stress and anxiety?"
- "What are the symptoms of PTSD?"

**Real-time Information (Web):**
- "What's the current GDP of the United States?"
- "Latest news in artificial intelligence"
- "Current Bitcoin price"

**General Knowledge (LLM):**
- "Explain the theory of relativity"
- "What is machine learning?"
- "How does photosynthesis work?"

## 🔍 Troubleshooting

**Common Issues:**

1. **API Key Errors**: Ensure your `.env` file contains valid API keys
2. **Document Loading Issues**: Check file formats and permissions in `data2/`
3. **Memory Issues**: Reduce `CHUNK_SIZE` in `config.py` for large documents
4. **Network Errors**: Verify internet connection for web search functionality

**Debug Mode:**
Run with verbose flag to see detailed validation information:
```bash
python main.py --query "your question" --verbose
```

## 🚀 Running the Application

Choose your preferred interface:

1. **Web Interface** (Best for exploration):
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Command Line** (Best for automation):
   ```bash
   python main.py --interactive
   ```

3. **Python API** (Best for integration):
   ```python
   from app import AgenticWorkflowApp
   app = AgenticWorkflowApp()
   app.initialize()
   result = app.ask_question("Your question here")
   ```

## 📈 Performance Tips

- Use SSD storage for faster document loading
- Increase `RETRIEVER_K` for more comprehensive RAG responses
- Adjust `MAX_RETRIES` based on quality requirements
- Monitor validation scores to optimize thresholds

---

🎉 **Ready to explore intelligent AI workflows!** Start with the Streamlit interface for the best experience.