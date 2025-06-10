import streamlit as st
import time
from workflow import create_workflow, run_query
from models import AgentState
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Agentic AI Workflow",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .response-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
    }
    .validation-score {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff3333;
        color: white;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'workflow_app' not in st.session_state:
        st.session_state.workflow_app = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'workflow_initialized' not in st.session_state:
        st.session_state.workflow_initialized = False
    if 'clear_input' not in st.session_state:
        st.session_state.clear_input = False

def initialize_workflow():
    """Initialize the workflow with progress tracking"""
    if not st.session_state.workflow_initialized:
        with st.spinner("🔄 Initializing AI Workflow..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Load documents
            status_text.text("📚 Loading documents...")
            progress_bar.progress(25)
            time.sleep(1)
            
            # Step 2: Create vector store
            status_text.text("🔍 Creating vector store...")
            progress_bar.progress(50)
            time.sleep(1)
            
            # Step 3: Initialize models
            status_text.text("🤖 Initializing AI models...")
            progress_bar.progress(75)
            time.sleep(1)
            
            # Step 4: Compile workflow
            status_text.text("⚙️ Compiling workflow...")
            progress_bar.progress(90)
            
            try:
                st.session_state.workflow_app = create_workflow()
                st.session_state.workflow_initialized = True
                progress_bar.progress(100)
                status_text.text("✅ Workflow initialized successfully!")
                time.sleep(1)
                status_text.empty()
                progress_bar.empty()
                st.success("🎉 AI Workflow is ready!")
            except Exception as e:
                st.error(f"❌ Failed to initialize workflow: {str(e)}")
                return False
    return True

def display_conversation_history():
    """Display conversation history in the sidebar"""
    st.sidebar.markdown("## 💬 Conversation History")
    
    if st.session_state.conversation_history:
        for i, entry in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
            query_num = len(st.session_state.conversation_history) - i
            with st.sidebar.expander(f"Query {query_num}", expanded=(i == 0)):
                st.markdown(f"**Q:** {entry['question']}")
                if 'score' in entry:
                    st.markdown(f"**Score:** {entry['score']}/100")
                st.markdown(f"**A:** {entry['answer'][:200]}{'...' if len(entry['answer']) > 200 else ''}")
    else:
        st.sidebar.info("No conversations yet. Ask a question to get started!")

def display_workflow_info():
    """Display workflow information in the sidebar"""
    st.sidebar.markdown("## 🔧 Workflow Information")
    
    st.sidebar.markdown("**Available Sources:**")
    st.sidebar.markdown("- 📚 **RAG**: Mental health documents")
    st.sidebar.markdown("- 🌐 **Web**: Real-time information") 
    st.sidebar.markdown("- 🧠 **LLM**: General knowledge")
    
    st.sidebar.markdown("**Features:**")
    st.sidebar.markdown("- ✅ Intelligent routing")
    st.sidebar.markdown("- 🔄 Retry mechanism")
    st.sidebar.markdown("- 📊 Response validation")
    st.sidebar.markdown("- 🔍 Fallback strategies")

def extract_validation_info(result):
    """Extract validation information from result"""
    validation_scores = result.get('validation_scores', [])
    if validation_scores:
        latest_score = validation_scores[-1]
        return {
            'score': latest_score.get('score', 0),
            'issues': latest_score.get('issues', []),
            'retry_count': latest_score.get('retry_count', 0),
            'answer_length': latest_score.get('answer_length', 0)
        }
    return None

def process_query(question):
    """Process a user query through the workflow"""
    if not st.session_state.workflow_app:
        st.error("Workflow not initialized. Please refresh the page.")
        return None
    
    with st.spinner("🤔 Processing your question..."):
        try:
            result = run_query(st.session_state.workflow_app, question)
            return result
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
            return None

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("<h1 class='main-header'>🤖 Agentic AI Workflow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Ask questions about mental health, get real-time information, or explore general knowledge!</p>", unsafe_allow_html=True)
    
    # Sidebar
    display_workflow_info()
    display_conversation_history()
    
    # Initialize workflow
    if not initialize_workflow():
        st.stop()
    
    # Main interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💭 Ask Your Question")
        
        # Example questions
        st.markdown("**💡 Example Questions:**")
        example_questions = [
            "What's the current GDP of the United States?",
            "What are effective treatments for depression?", 
            "How can I manage stress and anxiety?",
            "What's the latest news in technology?",
            "Explain the importance of mental health awareness"
        ]
        
        selected_example = st.selectbox("Choose an example question:", [""] + example_questions, key="example_selector")
        
        # Query input
        default_value = selected_example if selected_example else ""
        if st.session_state.clear_input:
            default_value = ""
            st.session_state.clear_input = False
        
        question = st.text_area(
            "Enter your question here:",
            value=default_value,
            placeholder="e.g., 'What are the symptoms of anxiety?' or 'What's the latest news about AI?'",
            height=100,
            key="user_question"
        )
    
    with col2:
        st.markdown("### 🚀 Actions")
        
        # Ask Question button (red styled)
        if st.button("🔍 Ask Question", key="ask_btn"):
            current_question = question.strip()
            if current_question:
                # Process the query
                result = process_query(current_question)
                
                if result:
                    # Extract answer
                    answer = result['messages'][-1]
                    if answer.startswith("✅ Final Answer: "):
                        answer = answer[17:]  # Remove prefix
                    
                    # Extract validation info
                    validation_info = extract_validation_info(result)
                    
                    # Store in conversation history
                    conversation_entry = {
                        'question': current_question,
                        'answer': answer,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if validation_info:
                        conversation_entry.update(validation_info)
                    
                    st.session_state.conversation_history.append(conversation_entry)
                    
                    # Clear input and trigger rerun
                    st.session_state.clear_input = True
                    st.rerun()
            else:
                st.warning("⚠️ Please enter a question or select an example.")
        
        # Clear History button
        if st.button("🗑️ Clear History", key="clear_btn"):
            st.session_state.conversation_history = []
            st.success("Conversation history cleared!")
            st.rerun()
    
    # Display recent query result if any
    if st.session_state.conversation_history:
        latest_entry = st.session_state.conversation_history[-1]
        
        st.markdown("---")
        st.markdown("### 📋 Latest Response")
        
        # Create response container
        with st.container():
            st.markdown(f"**🤔 Question:** {latest_entry['question']}")
            st.markdown("---")
            st.markdown(f"**🤖 Answer:** {latest_entry['answer']}")
            
            # Add validation metrics if available
            if 'score' in latest_entry:
                st.markdown("---")
                st.markdown("**📊 Quality Metrics:**")
                
                # Create columns for metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    score_color = "🟢" if latest_entry['score'] >= 70 else "🟡" if latest_entry['score'] >= 40 else "🔴"
                    st.markdown(f"{score_color} **Score:** {latest_entry['score']}/100")
                
                with col2:
                    st.markdown(f"🔄 **Retries:** {latest_entry.get('retry_count', 0)}")
                
                with col3:
                    st.markdown(f"📝 **Length:** {latest_entry.get('answer_length', len(latest_entry['answer']))} chars")
                
                with col4:
                    st.markdown(f"⚠️ **Issues:** {len(latest_entry.get('issues', []))}")
    
    # Session Statistics section
    if st.session_state.conversation_history:
        st.markdown("---")
        st.markdown("### 📊 Session Statistics")
        
        total_queries = len(st.session_state.conversation_history)
        avg_score = sum(entry.get('score', 0) for entry in st.session_state.conversation_history) / total_queries if total_queries > 0 else 0
        total_retries = sum(entry.get('retry_count', 0) for entry in st.session_state.conversation_history)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Queries", f"{total_queries}")
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}/100")
        with col3:
            st.metric("Total Retries", f"{total_retries}")

if __name__ == "__main__":
    main()