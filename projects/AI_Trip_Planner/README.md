# 🌍 AI Trip Planner

An intelligent travel planning application powered by AI agents that helps users create comprehensive travel itineraries with real-time data integration.

## 📋 Overview

The AI Trip Planner is an agentic AI application built using LangGraph that acts as a personal travel agent. It leverages multiple specialized tools to gather real-time information and create detailed, personalized travel plans for any destination worldwide.

## ✨ Features

- **Comprehensive Trip Planning**: Day-by-day itineraries with detailed recommendations
- **Real-time Weather Integration**: Current and forecasted weather conditions
- **Place Discovery**: Tourist attractions and off-beat locations
- **Budget Planning**: Detailed cost breakdowns and expense calculations
- **Currency Conversion**: Multi-currency support for international travel
- **Dual Interface**: Both web UI (Streamlit) and REST API (FastAPI)
- **Flexible LLM Support**: Works with OpenAI, Groq, and other providers

## 🏗️ Architecture

The application follows a modular architecture with the following components:

### Core Components

1. **Agent Workflow** (`agent/agentic_workflow.py`)
   - LangGraph-based workflow orchestration
   - Tool binding and execution management
   - State management for conversation flow

2. **Specialized Tools** (`tools/`)
   - Weather Information Tool
   - Place Search Tool
   - Expense Calculator Tool
   - Currency Conversion Tool

3. **Model Management** (`utils/model_loader.py`)
   - Configurable LLM provider support
   - Model loading and initialization

4. **Interfaces**
   - **Streamlit App** (`streamlit_app.py`): User-friendly web interface
   - **FastAPI Backend** (`main.py`): REST API for programmatic access

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- UV package manager (recommended) or pip

### Setup Instructions

1. **Clone and navigate to the project directory:**
   ```bash
   cd AI_Trip_Planner
   ```

2. **Set up virtual environment using UV:**
   ```bash
   uv venv env --python cpython-3.10.18
   ```

3. **Activate the virtual environment:**
   - **macOS/Linux:**
     ```bash
     source env/bin/activate
     ```
   - **Windows:**
     ```bash
     env\Scripts\activate.bat
     ```

4. **Install dependencies:**
   ```bash
   uv add -r requirements.txt
   ```
   
   Or with pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   ```bash
   cp .env.name .env
   # Edit .env file with your API keys
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# LLM Provider API Keys
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key

# Tool-specific API Keys
GOOGLE_PLACES_API_KEY=your_google_places_key
WEATHER_API_KEY=your_weather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Model Configuration

Edit `config/config.yaml` to configure LLM providers:

```yaml
llm:
  openai:
    provider: "openai"
    model_name: "gpt-4"
  groq:
    provider: "groq"
    model_name: "deepseek-r1-distill-llama-70b"
```

## 🚀 Usage

### Running the Streamlit Web App

```bash
streamlit run streamlit_app.py
```

Access the application at `http://localhost:8501`

### Running the FastAPI Backend

```bash
uvicorn main:app --reload --port 8000
```

API documentation available at `http://localhost:8000/docs`

### Using the API

**Endpoint:** `POST /query`

**Request Body:**
```json
{
  "question": "Plan a trip to Goa for 5 days"
}
```

**Response:**
```json
{
  "answer": "# 🌍 AI Travel Plan\n\n## Day-by-Day Itinerary...\n\n..."
}
```

## 🎯 Example Queries

- "Plan a 7-day trip to Japan in cherry blossom season"
- "Create a budget-friendly 3-day itinerary for Bangkok"
- "Suggest off-beat places to visit in Iceland for adventure travel"
- "Plan a family vacation to Orlando with kids under 10"

## 📊 Output Format

The AI Travel Agent provides comprehensive plans including:

- **Day-by-Day Itinerary**: Detailed schedule with timing and activities
- **Accommodation**: Hotel recommendations with pricing
- **Attractions**: Tourist spots and hidden gems
- **Dining**: Restaurant recommendations with price ranges
- **Transportation**: Local transport options and costs
- **Weather Information**: Current and forecasted conditions
- **Budget Breakdown**: Detailed cost analysis per category
- **Daily Expenses**: Per-day budget estimates

## 🔧 Tools Overview

### Weather Information Tool
- Real-time weather data
- Forecast information
- Seasonal recommendations

### Place Search Tool
- Tourist attractions discovery
- Off-beat location suggestions
- Reviews and ratings integration

### Expense Calculator Tool
- Cost calculations
- Budget planning
- Price comparisons

### Currency Conversion Tool
- Real-time exchange rates
- Multi-currency support
- Cost calculations in local currency

## 🛡️ Error Handling

The application includes robust error handling for:
- API failures and timeouts
- Invalid input validation
- Tool execution errors
- Model provider issues

## 📁 Project Structure

```
AI_Trip_Planner/
├── agent/                 # Core agent workflow
├── config/               # Configuration files
├── tools/                # Specialized AI tools
├── utils/                # Utility functions
├── prompt_library/       # System prompts
├── exception/            # Custom exceptions
├── logger/               # Logging configuration
├── main.py              # FastAPI backend
├── streamlit_app.py     # Streamlit frontend
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with LangGraph and LangChain
- Powered by various LLM providers (OpenAI, Groq)
- Integrates multiple external APIs for real-time data