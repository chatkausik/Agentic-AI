import streamlit as st
import asyncio
import os
from datetime import datetime
import sys
import pandas as pd

# Add the current directory to Python path to import the agent
sys.path.append('.')

try:
    from Arxiv_paper_Agent_Autogen import get_literature_review, arxiv_search
except ImportError:
    st.error("Could not import the Arxiv agent. Make sure Arxiv_paper_Agent_Autogen.py is in the same directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="ArXiv Literature Review Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #1e3a8a;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1e40af;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .literature-review {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'review_result' not in st.session_state:
    st.session_state.review_result = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Header
st.markdown('<h1 class="main-header">📚 ArXiv Literature Review Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Generate comprehensive literature reviews using AI agents")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        st.error("⚠️ OpenAI API key not found!")
        st.info("Please set your OPENAI_API_KEY environment variable")
        openai_key = st.text_input("Or enter your OpenAI API key:", type="password")
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key
            st.success("API key set!")
    else:
        st.success("✅ OpenAI API key found")
    
    st.divider()
    
    # Number of papers slider
    num_papers = st.slider(
        "Number of papers to analyze:",
        min_value=3,
        max_value=10,
        value=5,
        help="More papers provide broader coverage but take longer to process"
    )
    
    st.divider()
    
    # Search history
    st.header("📝 Search History")
    if st.session_state.search_history:
        for i, search in enumerate(reversed(st.session_state.search_history[-5:])):
            if st.button(f"🔄 {search['topic']}", key=f"history_{i}"):
                st.session_state.selected_topic = search['topic']
                st.session_state.selected_papers = search['papers']
                st.rerun()
    else:
        st.info("No searches yet")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Topic input
    topic = st.text_input(
        "🔍 Enter research topic:",
        placeholder="e.g., machine learning, quantum computing, computer vision...",
        value=st.session_state.get('selected_topic', '')
    )
    
    # Quick topic suggestions
    st.markdown("**Quick suggestions:**")
    suggestion_cols = st.columns(4)
    suggestions = ["Transformer Models", "Graph Neural Networks", "Reinforcement Learning", "Computer Vision"]
    
    for i, suggestion in enumerate(suggestions):
        with suggestion_cols[i]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                topic = suggestion
                st.rerun()

with col2:
    st.markdown("### 💡 How it works")
    st.info("""
    1. **Search**: AI agent finds relevant papers
    2. **Analyze**: Papers are analyzed for key insights
    3. **Summarize**: Comprehensive review is generated
    4. **Present**: Results shown in readable format
    """)

# Main action area
if st.button("🚀 Generate Literature Review", disabled=not topic):
    if not topic.strip():
        st.error("Please enter a research topic")
    else:
        with st.spinner(f"🔍 Searching for papers on '{topic}'... This may take a few minutes..."):
            try:
                # Create progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Searching ArXiv database...")
                progress_bar.progress(25)
                
                # Check if there's an existing event loop
                try:
                    loop = asyncio.get_running_loop()
                    # If we're in an existing loop, we need to use a different approach
                    import concurrent.futures
                    import threading
                    
                    def run_async_task():
                        # Create a new event loop in a separate thread
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        try:
                            return new_loop.run_until_complete(get_literature_review(topic, num_papers))
                        finally:
                            new_loop.close()
                    
                    status_text.text("🤖 AI agents analyzing papers...")
                    progress_bar.progress(50)
                    
                    # Run in a separate thread to avoid event loop conflicts
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_async_task)
                        result = future.result(timeout=300)  # 5 minute timeout
                        
                except RuntimeError:
                    # No event loop running, we can create our own
                    status_text.text("🤖 AI agents analyzing papers...")
                    progress_bar.progress(50)
                    
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        result = loop.run_until_complete(get_literature_review(topic, num_papers))
                    finally:
                        loop.close()
                
                # Check if result contains an error
                if result.startswith("Error generating literature review:"):
                    st.error(f"❌ {result}")
                    st.info("This might be due to:")
                    st.write("- Invalid or missing OpenAI API key")
                    st.write("- Network connectivity issues")
                    st.write("- AutoGen API changes")
                    st.write("- ArXiv service unavailable")
                else:
                    status_text.text("📝 Generating comprehensive review...")
                    progress_bar.progress(75)
                    
                    # Store result and update history
                    st.session_state.review_result = result
                    st.session_state.search_history.append({
                        'topic': topic,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'papers': num_papers
                    })
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Review generated successfully!")
                
            except concurrent.futures.TimeoutError:
                st.error("❌ Request timed out. The operation took too long.")
                st.info("Please try with fewer papers or check your internet connection.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.info("Please try the following:")
                st.write("- Check your OpenAI API key")
                st.write("- Verify internet connection")
                st.write("- Try a different topic")
                st.write("- Restart the application")
                
                # Show detailed error for debugging
                with st.expander("🔧 Technical Details"):
                    st.code(f"Error type: {type(e).__name__}\nError message: {str(e)}")

# Display results
if st.session_state.review_result:
    st.markdown("---")
    st.markdown("## 📋 Literature Review Results")
    
    # Action buttons for the result
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📋 Copy to Clipboard"):
            st.write("Review copied! (Use Ctrl+A, Ctrl+C to copy the text below)")
    
    with col2:
        # Download button
        st.download_button(
            label="💾 Download as Markdown",
            data=st.session_state.review_result,
            file_name=f"literature_review_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    
    # Display the review with custom styling
    st.markdown('<div class="literature-review">', unsafe_allow_html=True)
    st.markdown(st.session_state.review_result)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Option to search for more papers
    if st.button("🔄 Generate New Review"):
        st.session_state.review_result = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem;'>
    <p>🤖 Powered by AutoGen AI Agents & OpenAI GPT-4</p>
    <p>📚 Data sourced from ArXiv.org</p>
</div>
""", unsafe_allow_html=True)