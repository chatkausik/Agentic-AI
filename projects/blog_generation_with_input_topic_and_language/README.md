# Multilingual Blog Generation with LangGraph

A sophisticated blog generation system that creates content based on input topics and can translate the generated content into multiple languages using LangGraph workflows and Groq LLM.

## 🚀 Features

- **Topic-based Blog Generation**: Generate comprehensive blog posts from any topic
- **Multilingual Support**: Translate content to Hindi and French
- **LangGraph Workflows**: Efficient workflow orchestration with conditional routing
- **FastAPI Integration**: RESTful API for easy integration
- **Groq LLM**: Fast and efficient language model for content generation
- **Structured Output**: Consistent blog format with title and content
- **LangSmith Integration**: Built-in tracing and observability

## 🏗️ Architecture

The system uses a graph-based architecture with LangGraph:

```
Topic Input → Title Creation → Content Generation → Language Routing → Translation → Output
```

### Workflow Types

1. **Topic-only Workflow**: Generates blog content in English
2. **Topic + Language Workflow**: Generates content and translates to specified language

## 📦 Installation

### Prerequisites
- Python 3.13+
- Groq API Key
- LangChain API Key (optional, for tracing)

### Setup

1. **Clone and navigate to the project**:
```bash
cd /Users/kausik/Desktop/Agentic-AI/projects/blog_generation_with_input_topic_and_language
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp _copy.env .env
```

Edit `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGSMITH_PROJECT_NAME=blog-generation-multilingual
LANGSMITH_TRACING=true
```

## 🎯 Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:8002`

### API Endpoints

#### Generate Blog (Topic Only)
```bash
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence in Healthcare"
  }'
```

#### Generate Blog with Translation
```bash
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence in Healthcare",
    "language": "hindi"
  }'
```

**Supported Languages:**
- `hindi`
- `french`

### Response Format

```json
{
  "data": {
    "topic": "Artificial Intelligence in Healthcare",
    "blog": {
      "title": "# AI Revolution in Healthcare: Transforming Patient Care",
      "content": "## Introduction\n\nArtificial Intelligence (AI) is revolutionizing..."
    },
    "current_language": "hindi"
  }
}
```

## 🔧 Project Structure

```
blog_generation_with_input_topic_and_language/
├── app.py                 # FastAPI application
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── pyproject.toml       # Project configuration
├── .env                 # Environment variables
├── src/
│   ├── __init__.py
│   ├── graphs/
│   │   └── graph_builder.py    # LangGraph workflow builder
│   ├── llms/
│   │   └── groqllm.py          # Groq LLM configuration
│   ├── nodes/
│   │   └── blog_node.py        # Workflow nodes
│   └── states/
│       └── blogstate.py        # State management
```

## 🧩 Components

### GraphBuilder
Orchestrates the workflow with two main patterns:
- **Topic Graph**: Simple linear workflow for English content
- **Language Graph**: Conditional workflow with translation routing

### BlogNode
Contains the core processing nodes:
- `title_creation`: Generates SEO-friendly blog titles
- `content_generation`: Creates detailed blog content
- `translation`: Translates content to target language
- `route`: Determines translation path

### BlogState
Manages workflow state with:
- `topic`: Input topic
- `blog`: Generated content (title + content)
- `current_language`: Target language for translation

## 🔍 API Reference

### POST /blogs

**Request Body:**
```json
{
  "topic": "string (required)",
  "language": "string (optional: 'hindi' | 'french')"
}
```

**Response:**
```json
{
  "data": {
    "topic": "string",
    "blog": {
      "title": "string",
      "content": "string"
    },
    "current_language": "string"
  }
}
```

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```

### Testing the API
```bash
# Test with topic only
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Machine Learning Basics"}'

# Test with translation
curl -X POST "http://localhost:8002/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Machine Learning Basics", "language": "french"}'
```

## 📊 Monitoring

The system includes LangSmith integration for:
- Workflow tracing
- Performance monitoring
- Error tracking
- Usage analytics

## 🔐 Security

- API keys are loaded from environment variables
- Input validation for topic and language parameters
- Secure LLM API communication

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t blog-generator-multilingual .

# Run container
docker run -p 8002:8002 --env-file .env blog-generator-multilingual
```

### Production Considerations
- Use production WSGI server (Gunicorn)
- Implement rate limiting
- Add authentication if needed
- Set up monitoring and logging

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Required for LLM access
- `LANGCHAIN_API_KEY`: Optional for tracing
- `LANGSMITH_PROJECT_NAME`: Project name for tracing
- `LANGSMITH_TRACING`: Enable/disable tracing

### LLM Configuration
- Model: `llama-3.1-8b-instant`
- Provider: Groq
- Structured output support for consistent formatting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the Agentic AI learning series.

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -i :8002
kill -9 <PID>
```

**API key issues:**
```bash
# Verify environment variables
python -c "import os; print(os.getenv('GROQ_API_KEY'))"
```

**Dependencies issues:**
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Groq API Documentation](https://console.groq.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)