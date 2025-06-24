# Blog Generation with Input Topic

An intelligent blog generation system built with LangGraph and FastAPI that creates SEO-friendly blog posts from user-provided topics using AI agents.

## 🚀 Features

- **AI-Powered Content Generation**: Uses Groq's Llama 3.1 model for high-quality content creation
- **Agentic Workflow**: LangGraph-based state machine with specialized nodes for title creation and content generation
- **RESTful API**: FastAPI-based web service for easy integration
- **LangSmith Integration**: Built-in observability and debugging support
- **Markdown Output**: Generated content formatted in Markdown for easy publishing

## 🏗️ Architecture

The system uses a multi-agent architecture built on LangGraph:

1. **Title Creation Node**: Generates creative, SEO-friendly titles
2. **Content Generation Node**: Creates detailed blog content with proper formatting
3. **State Management**: Maintains blog state throughout the generation process

```
Topic Input → Title Creation → Content Generation → Complete Blog Post
```

## 📁 Project Structure

```
blog_generation_with_input_topic/
├── app.py                      # FastAPI application
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── langgraph.json             # LangGraph configuration
├── pyproject.toml             # Project metadata
├── request.json               # Sample API request
└── src/
    ├── graphs/
    │   └── graph_builder.py   # LangGraph workflow builder
    ├── llms/
    │   └── groqllm.py        # Groq LLM integration
    ├── nodes/
    │   └── blog_node.py      # Blog generation nodes
    └── states/
        └── blogstate.py      # State management
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   cd /Users/kausik/Desktop/Agentic-AI/projects/blog_generation_with_input_topic
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGCHAIN_API_KEY=your_langchain_api_key_here
   ```

## 🚀 Usage

### Running the FastAPI Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:8001`

### API Endpoints

#### Generate Blog Post

**POST** `/blogs`

**Request Body**:
```json
{
    "topic": "Artificial Intelligence in Healthcare"
}
```

**Response**:
```json
{
    "data": {
        "topic": "Artificial Intelligence in Healthcare",
        "blog": {
            "title": "# Revolutionizing Healthcare: The AI Transformation",
            "content": "## Introduction\n\nArtificial Intelligence is transforming healthcare...\n\n## Key Applications\n\n..."
        }
    }
}
```

### Using with LangGraph Studio

The project is configured for LangGraph Studio debugging:

```bash
langgraph dev
```

This will launch the interactive debugging interface for the blog generation workflow.

## 🔧 Configuration

### LangGraph Configuration (`langgraph.json`)

```json
{
    "dependencies": ["."],
    "graphs": {
        "blog_generator_agent": "./src/graphs/graph_builder.py:graph"
    },
    "env": "./.env"
}
```

## 📊 State Management

The system uses a typed state structure:

```python
class BlogState(TypedDict):
    topic: str              # Input topic
    blog: Blog             # Generated blog object
    current_language: str   # Language setting
```

## 🧠 AI Components

### LLM Integration
- **Model**: Llama 3.1 8B Instant via Groq
- **Provider**: Groq for fast inference
- **Prompting**: Specialized prompts for title and content generation

### Node Functions

1. **Title Creation**: 
   - Generates SEO-friendly titles
   - Uses creative prompting strategies

2. **Content Generation**:
   - Creates detailed, structured content
   - Maintains context from title
   - Outputs markdown-formatted text

## 🔍 Monitoring & Debugging

### LangSmith Integration
- Automatic tracing of workflow execution
- Performance monitoring
- Debug information for troubleshooting

### Local Development
```bash
# Run with auto-reload
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

## 📝 Example Usage

```python
import requests

# Make API request
response = requests.post(
    "http://localhost:8001/blogs",
    json={"topic": "Sustainable Energy Solutions"}
)

blog_data = response.json()
print(blog_data["data"]["blog"]["title"])
print(blog_data["data"]["blog"]["content"])
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Agentic AI learning series.

## 🔗 Related Projects

- [Blog Generation with Language Support](../blog_generation_with_input_topic_and_language/)
- [Agentic Workflow Project](../../3-langgraph/Agentic-workflow-project/)

## 🚨 Requirements

- Python 3.8+
- Groq API key
- LangChain API key (for LangSmith)

## 📞 Support

For questions or issues, please refer to the main Agentic AI project documentation.