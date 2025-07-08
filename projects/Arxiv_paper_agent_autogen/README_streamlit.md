# ArXiv Literature Review Assistant

A Streamlit web application that uses AI agents to automatically generate comprehensive literature reviews from ArXiv papers.

## Features

- 🔍 **Intelligent Search**: AI agent finds the most relevant papers for your topic
- 📊 **Comprehensive Analysis**: Papers are analyzed for key problems and contributions
- 📝 **Formatted Output**: Clean, readable literature reviews in Markdown format
- 💾 **Download Support**: Save reviews as Markdown files
- 📚 **Search History**: Keep track of previous searches
- ⚙️ **Customizable**: Choose number of papers to analyze (3-10)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Run the App**:
   ```bash
   streamlit run streamlit_arxiv_app.py
   ```

## Usage

1. Enter a research topic in the search box
2. Use the sidebar to configure the number of papers
3. Click "Generate Literature Review"
4. Wait for the AI agents to process (may take 2-3 minutes)
5. View, copy, or download the formatted review

## How It Works

The application uses two AI agents:

1. **ArXiv Researcher Agent**: Searches ArXiv for relevant papers using intelligent queries
2. **Summarizer Agent**: Creates a comprehensive literature review with:
   - Topic introduction
   - Individual paper summaries with key contributions
   - Overall conclusions and takeaways

## Output Format

Each literature review includes:
- Clear title and introduction
- Detailed paper analysis with:
  - Title (linked to PDF)
  - Authors and publication date
  - Problem statement
  - Key contributions
  - Brief summary
- Conclusion with key insights

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for ArXiv access

## Troubleshooting

- **API Key Error**: Make sure your OpenAI API key is correctly set
- **Import Error**: Ensure all dependencies are installed
- **Slow Response**: Literature reviews can take 2-3 minutes to generate
- **Connection Issues**: Check your internet connection for ArXiv access