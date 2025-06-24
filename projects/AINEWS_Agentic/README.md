# 🤖 AINEWS Agentic - Multi-Modal LangGraph AI Application

An end-to-end agentic AI application built with LangGraph that provides multiple AI-powered functionalities including AI news aggregation, web-enabled chatbots, and basic conversational AI through an intuitive Streamlit interface.

## 📋 Overview

AINEWS_Agentic is a comprehensive AI application that demonstrates the power of LangGraph for building multi-agent workflows. The application offers three distinct use cases:

1. **Basic Chatbot** - Simple conversational AI
2. **Chatbot with Web Search** - Enhanced chatbot with real-time web search capabilities
3. **AI News Aggregator** - Automated AI news fetching, summarization, and archiving

## ✨ Features

### 🎯 Core Features
- **Multi-Use Case Support**: Switch between different AI functionalities seamlessly
- **LangGraph Integration**: Leverages state-of-the-art graph-based AI workflows
- **Streamlit UI**: User-friendly web interface with sidebar controls
- **Multiple LLM Support**: Currently supports Groq models with extensible architecture
- **Real-time Processing**: Live updates and streaming responses

### 🔧 Use Cases

#### 1. Basic Chatbot
- Simple conversational AI powered by Groq LLM
- Clean, straightforward chat interface
- Perfect for general Q&A and conversation

#### 2. Chatbot with Web Search
- Enhanced chatbot with Tavily web search integration
- Real-time information retrieval
- Tool-enabled responses with up-to-date data
- Conditional graph execution based on user queries

#### 3. AI News Aggregator
- **Automated News Fetching**: Retrieves latest AI news from multiple sources
- **Time-based Filtering**: Daily, Weekly, or Monthly news aggregation
- **Intelligent Summarization**: AI-powered news summarization with structured output
- **Markdown Export**: Saves summaries in organized markdown format
- **Date Sorting**: News sorted by latest first with IST timezone
- **Source Attribution**: Direct links to original articles

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- API Keys for:
  - Groq API (for LLM functionality)
  - Tavily API (for web search and news aggregation)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd AINEWS_Agentic
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

## 🚀 Usage

### Getting Started
1. Launch the application using `streamlit run app.py`
2. Open your browser to `http://localhost:8501`
3. Configure your settings in the sidebar:
   - Select LLM provider (Groq)
   - Choose model (various Groq models available)
   - Enter API keys
   - Select use case

### Use Case Specific Instructions

#### Basic Chatbot
1. Select "Basic Chatbot" from the sidebar
2. Enter your Groq API key
3. Start chatting in the main interface

#### Chatbot with Web Search
1. Select "Chatbot With Web" from the sidebar
2. Enter both Groq and Tavily API keys
3. Ask questions that require real-time information
4. The system will automatically search the web when needed

#### AI News Aggregator
1. Select "AI News" from the sidebar
2. Enter both Groq and Tavily API keys
3. Choose time frame (Daily/Weekly/Monthly)
4. Click "🔍 Fetch Latest AI News"
5. View summarized news in the interface
6. Check the `AINews/` folder for saved markdown files

## 📁 Project Structure

```
AINEWS_Agentic/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── AINews/                         # Generated news summaries
└── src/
    └── langgraphagenticai/
        ├── main.py                 # Core application logic
        ├── LLMS/
        │   └── groqllm.py         # Groq LLM configuration
        ├── graph/
        │   └── graph_builder.py   # LangGraph workflow builder
        ├── nodes/
        │   ├── basic_chatbot_node.py      # Basic chat functionality
        │   ├── chatbot_with_Tool_node.py  # Web-enabled chat
        │   └── ai_news_node.py            # News aggregation logic
        ├── state/
        │   └── state.py           # Graph state management
        ├── tools/
        │   └── search_tool.py     # Web search tools
        └── ui/
            └── streamlitui/       # Streamlit interface components
```

## 🏗️ Architecture

### LangGraph Workflows

The application uses LangGraph to create three distinct workflow patterns:

1. **Linear Flow** (Basic Chatbot): `START → chatbot → END`
2. **Conditional Flow** (Web Chatbot): `START → chatbot → [tools] → chatbot → END`
3. **Sequential Flow** (AI News): `fetch_news → summarize_news → save_result → END`

### Key Components

- **GraphBuilder**: Orchestrates different workflow patterns
- **State Management**: Maintains conversation and processing state
- **Node Architecture**: Modular processing units for different functionalities
- **UI Layer**: Streamlit-based interface with dynamic controls

## 🔑 API Requirements

### Groq API
- **Purpose**: Powers the LLM functionality across all use cases
- **Get API Key**: [Groq Console](https://console.groq.com/keys)
- **Models Supported**: Various Groq models available in the dropdown

### Tavily API
- **Purpose**: Enables web search and news aggregation
- **Get API Key**: [Tavily App](https://app.tavily.com/home)
- **Required For**: "Chatbot With Web" and "AI News" use cases

## 📊 Dependencies

```
langchain                 # LangChain framework
langgraph                 # Graph-based AI workflows
langchain_community       # Community extensions
langchain_core           # Core LangChain functionality
langchain_groq           # Groq integration
langchain_openai         # OpenAI compatibility
faiss-cpu                # Vector similarity search
streamlit                # Web UI framework
tavily-python            # Web search API
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of the Agentic AI learning series and is intended for educational purposes.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are valid and have sufficient credits
2. **Import Errors**: Verify all dependencies are installed via `pip install -r requirements.txt`
3. **Port Issues**: If port 8501 is busy, Streamlit will automatically use the next available port
4. **News Fetching Issues**: Check your Tavily API key and internet connection

### Support

For issues and questions, please check the project documentation or create an issue in the repository.

---

Built with ❤️ using LangGraph, Streamlit, and modern AI technologies.