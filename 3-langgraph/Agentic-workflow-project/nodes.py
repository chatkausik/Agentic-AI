from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.tavily_search import TavilySearchResults
from models import AgentState, TopicSelection
from config import LLM_MODEL, MAX_RETRIES, TAVILY_API_KEY
from document_loader import format_docs

# Initialize retriever (will be set by workflow)
retriever = None

def set_retriever(ret):
    """Set the retriever for RAG node"""
    global retriever
    retriever = ret

# ========== Output Parser ==========
parser = PydanticOutputParser(pydantic_object=TopicSelection)

# ========== Supervisor Node ==========
def supervisor_node(state: AgentState):
    question = state["messages"][-1]

    prompt = PromptTemplate(
        template="""
        Classify the user query into one of these: [Mental Health, Real Time Info, Not Related].
        
        Classification Rules:
        - Mental Health: Questions about mental health, stress management, anxiety, depression, coping strategies, emotional wellbeing, therapy, psychological support, mental disorders, or any mental health-related topics
        - Real Time Info: Questions asking for current, recent, latest, or real-time information like news, stock prices, weather, sports scores, or current events
        - Not Related: General knowledge questions that don't fit the above categories
        
        Examples:
        - "How to manage stress and anxiety?" → Mental Health
        - "What are coping strategies for depression?" → Mental Health  
        - "Current Bitcoin price" → Real Time Info
        - "Latest news about elections" → Real Time Info
        - "What is the capital of France?" → Not Related

        Query: {question}
        {format_instructions}
        """,
        input_variables=["question"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | LLM_MODEL | parser
    response = chain.invoke({"question": question})
    print(f"Supervisor classification: {response}")
    return {"messages": [response.Topic]}

# ========== Router Function ==========
def router(state: AgentState):
    last = state["messages"][-1].lower()
    print(f"Routing decision for: {last}")
    
    # Enhanced keyword sets for better classification
    web_keywords = {
        # Time-based indicators
        "real time", "live", "latest", "current", "recent", "today", "now",
        "breaking", "news", "updates", "happening", "trending", "just",
        # Date indicators
        "2024", "2023", "this year", "this month", "this week", "yesterday",
        # Web-specific content
        "stock price", "weather", "sports score", "election results",
        "cryptocurrency", "bitcoin", "market", "exchange rate"
    }
    
    mental_health_keywords = {
        # Core mental health terms
        "mental health", "mental illness", "depression", "anxiety", "stress",
        "therapy", "counseling", "psychiatry", "psychology", "psychiatric",
        "bipolar", "schizophrenia", "ptsd", "trauma", "panic", "phobia",
        "suicide", "self-harm", "addiction", "substance abuse",
        # Related concepts
        "wellbeing", "wellness", "mindfulness", "meditation", "self-care",
        "emotional", "mood", "feelings", "cognitive", "behavioral",
        "mind", "brain health", "neurological", "psychological"
    }
    
    # Check for web-related content
    if any(keyword in last for keyword in web_keywords):
        print(f"→ Routing to WEB (found web keywords)")
        return "Web"
    
    # Check for mental health content
    if any(keyword in last for keyword in mental_health_keywords):
        print(f"→ Routing to RAG (found mental health keywords)")
        return "RAG"
    
    # Additional pattern matching for better detection
    
    # Check for question patterns that might indicate real-time info
    time_patterns = [
        "what's happening", "what is happening", "latest on", "update on",
        "current status", "right now", "at the moment", "as of today"
    ]
    
    if any(pattern in last for pattern in time_patterns):
        print(f"→ Routing to WEB (found time-related patterns)")
        return "Web"
    
    # Check for mental health question patterns
    health_patterns = [
        "how to cope", "dealing with", "managing stress", "feeling anxious",
        "mental state", "emotional support", "psychological help",
        "mental disorder", "brain function", "cognitive issue"
    ]
    
    if any(pattern in last for pattern in health_patterns):
        print(f"→ Routing to RAG (found mental health patterns)")
        return "RAG"
    
    # Check if it's asking about document-specific content
    doc_indicators = [
        "according to", "document says", "research shows", "study indicates",
        "pdf", "report", "who says", "health organization"
    ]
    
    if any(indicator in last for indicator in doc_indicators):
        print(f"→ Routing to RAG (document-related query)")
        return "RAG"
    
    # Default to LLM for general knowledge questions
    print(f"→ Routing to LLM (general knowledge/default)")
    return "LLM"

# ========== RAG Node ==========
def rag_node(state: AgentState):
    question = state["messages"][0]

    prompt = PromptTemplate(
        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 

If the provided context does not contain relevant information to answer the question, respond with: "The provided text does not offer information about [topic]. This question requires information not available in the current documents."

If you have relevant context, provide a concise answer using the information.

Question: {question}
Context: {context}
Answer:""",
        input_variables=["context", "question"],
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | LLM_MODEL
        | StrOutputParser()
    )
    result = chain.invoke(question)
    print(f"result from rag: {result}")
    return {"messages": [result], "last_source": "RAG"}

# ========== LLM Node ==========
def llm_node(state: AgentState):
    question = state["messages"][0]
    prompt = (
        f"Answer the following question using your own knowledge: {question}"
    )
    response = LLM_MODEL.invoke(prompt)
    print(f"response from llm: {response}")
    return {"messages": [response.content]}

# ========== Enhanced Web Crawler Node ==========
def web_node(state: AgentState):
    """
    Enhanced web search with better result processing and formatting
    """
    query = state["messages"][0]
    print(f"🔍 Web search for: {query}")
    
    try:
        # Initialize Tavily search tool with API key
        if TAVILY_API_KEY:
            tool = TavilySearchResults(max_results=3, tavily_api_key=TAVILY_API_KEY)
        else:
            # Fallback without API key (uses default configuration)
            tool = TavilySearchResults(max_results=3)
        
        # Perform search
        search_results = tool.invoke({"query": query})
        print(f"📊 Found {len(search_results)} search results")
        
        if not search_results:
            return {"messages": ["I couldn't find any relevant information through web search. Please try rephrasing your question."], "last_source": "Web"}
        
        # Process and format results
        formatted_content = []
        
        for i, result in enumerate(search_results, 1):
            content = result.get("content", "")
            url = result.get("url", "")
            title = result.get("title", f"Result {i}")
            
            if content:
                # Clean and truncate content if too long
                clean_content = content.strip()
                if len(clean_content) > 800:
                    clean_content = clean_content[:800] + "..."
                
                formatted_result = f"**Source {i}: {title}**\n{clean_content}"
                if url:
                    formatted_result += f"\n*Source: {url}*"
                
                formatted_content.append(formatted_result)
        
        if not formatted_content:
            return {"messages": ["I found search results but couldn't extract useful content. Please try a different query."], "last_source": "Web"}
        
        # Combine all results into a comprehensive answer
        if len(formatted_content) == 1:
            final_answer = formatted_content[0]
        else:
            final_answer = "Here's what I found from multiple sources:\n\n" + "\n\n".join(formatted_content)
        
        # Add a helpful conclusion for stress/anxiety queries
        query_lower = query.lower()
        if any(term in query_lower for term in ["stress", "anxiety", "mental health", "cope", "manage"]):
            final_answer += "\n\n💡 **Remember**: If you're experiencing persistent stress or anxiety, consider consulting with a mental health professional for personalized guidance."
        
        print(f"✅ Web search completed successfully")
        return {"messages": [final_answer], "last_source": "Web"}
        
    except Exception as e:
        print(f"❌ Web search error: {str(e)}")
        error_message = f"I encountered an error while searching the web: {str(e)}. Please try rephrasing your question or check your internet connection."
        return {"messages": [error_message], "last_source": "Web"}

# ========== Enhanced Validator Node ==========
def validator_node(state: AgentState):
    """
    Comprehensive validation with RAG failure detection and web fallback
    """
    print(f"🔍 Validating response...")
    answer = state["messages"][-1]
    original_question = state["messages"][0]
    last_source = state.get("last_source", "")
    
    # Initialize validation score
    validation_score = 0
    validation_issues = []
    rag_failed = False
    
    # Special check for RAG failure responses
    rag_failure_phrases = {
        "the provided text does not offer information",
        "provided text does not contain",
        "text does not provide",
        "document does not contain",
        "no relevant information found",
        "cannot find information in the provided context",
        "the context does not include",
        "based on the provided context, there is no information",
        "the given context doesn't contain"
    }
    
    answer_lower = answer.lower()
    
    # Check if this is a RAG response that failed to find information
    if any(phrase in answer_lower for phrase in rag_failure_phrases):
        print("🔍 Detected RAG failure: No relevant information found in documents")
        rag_failed = True
        validation_issues.append("RAG failed to find relevant information")
        # Lower score but don't immediately fail - allow for web fallback
        validation_score = 30
    
    # 1. Basic content checks
    if not answer or answer.strip() == "":
        validation_issues.append("Empty response")
    elif len(answer.strip()) < 15:
        validation_issues.append("Response too short (< 15 characters)")
    else:
        validation_score += 20
    
    # 2. Check for unhelpful responses
    unhelpful_phrases = {
        "i don't know", "i'm not sure", "i cannot", "i can't help",
        "no information", "not available", "unclear", "insufficient data",
        "unable to provide", "sorry, i don't have", "not found",
        "cannot determine", "no data available", "information not available"
    }
    
    if any(phrase in answer_lower for phrase in unhelpful_phrases):
        validation_issues.append("Contains unhelpful phrases indicating lack of knowledge")
    else:
        validation_score += 20
    
    # 3. Check for relevance to the question
    question_words = set(original_question.lower().split())
    answer_words = set(answer_lower.split())
    
    # Remove common stop words for better relevance checking
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "what", "how", "why", "when", "where"}
    question_keywords = question_words - stop_words
    answer_keywords = answer_words - stop_words
    
    if question_keywords:
        relevance_overlap = len(question_keywords & answer_keywords) / len(question_keywords)
        if relevance_overlap > 0.1:  # At least 10% keyword overlap
            validation_score += 20
        else:
            validation_issues.append("Low relevance to original question")
    
    # 4. Check for appropriate structure and completeness
    if len(answer.split('.')) >= 2:  # Has multiple sentences
        validation_score += 15
    
    if any(char in answer for char in '.,!?'):  # Has proper punctuation
        validation_score += 10
    
    # 5. Check for error messages or technical failures
    error_indicators = [
        "error", "exception", "failed", "timeout", "connection",
        "server error", "not found", "access denied", "forbidden"
    ]
    
    if any(indicator in answer_lower for indicator in error_indicators):
        validation_issues.append("Contains error indicators")
    else:
        validation_score += 15
    
    # 6. Determine current retry count and max retries
    current_retry_count = state.get("retry_count", 0)
    max_retries = MAX_RETRIES
    
    # Create validation report
    validation_report = {
        "score": validation_score,
        "max_score": 100,
        "issues": validation_issues,
        "retry_count": current_retry_count,
        "answer_length": len(answer),
        "rag_failed": rag_failed,
        "timestamp": "current"
    }
    
    # Add to validation history
    validation_scores = state.get("validation_scores", [])
    validation_scores.append(validation_report)
    
    print(f"📊 Validation Score: {validation_score}/100")
    if validation_issues:
        print(f"⚠️  Issues found: {', '.join(validation_issues)}")
    
    # Enhanced decision logic with RAG fallback
    if rag_failed:
        print("🔄 RAG failed - triggering web search fallback")
        return {
            "messages": ["__RAG_FALLBACK__"],
            "rag_failed": True,
            "retry_count": current_retry_count,
            "validation_scores": validation_scores
        }
    elif validation_score >= 70:
        print("✅ Validation Passed - High Quality Response")
        return {
            "messages": [answer],
            "validation_scores": validation_scores
        }
    elif validation_score >= 40 and current_retry_count >= max_retries:
        print(f"⚠️  Validation Passed with Warnings - Max retries ({max_retries}) reached")
        return {
            "messages": [answer],
            "validation_scores": validation_scores
        }
    else:
        print(f"❌ Validation Failed - Score: {validation_score}/100, Retry: {current_retry_count + 1}/{max_retries + 1}")
        return {
            "messages": ["__RETRY__"],
            "retry_count": current_retry_count + 1,
            "validation_scores": validation_scores
        }

# ========== Enhanced Retry Router ==========
def retry_router(state: AgentState):
    """
    Intelligent retry routing with adaptive strategies and RAG fallback
    """
    print(f"🔄 Retry Router Decision...")
    
    last_message = state["messages"][-1]
    retry_count = state.get("retry_count", 0)
    validation_scores = state.get("validation_scores", [])
    
    if last_message == "__RETRY__":
        print(f"📈 Retry Analysis:")
        print(f"   • Current retry count: {retry_count}")
        print(f"   • Validation history: {len(validation_scores)} attempts")
        
        # Analyze validation history for patterns
        if len(validation_scores) >= 2:
            recent_scores = [v["score"] for v in validation_scores[-2:]]
            if recent_scores[-1] <= recent_scores[-2]:
                print(f"   • Score trend: Declining ({recent_scores[-2]} → {recent_scores[-1]})")
            else:
                print(f"   • Score trend: Improving ({recent_scores[-2]} → {recent_scores[-1]})")
        
        # Strategic retry decision
        if retry_count <= 2:
            print(f"🔄 Routing back to Supervisor for retry #{retry_count}")
            return "Supervisor"
        else:
            print(f"🛑 Max retries exceeded. Proceeding to Final with best available answer.")
            # Find the best scoring response from history
            if validation_scores:
                best_attempt = max(validation_scores, key=lambda x: x["score"])
                print(f"   • Using best attempt with score: {best_attempt['score']}/100")
            return "Final"
    elif last_message == "__RAG_FALLBACK__":
        print("🔄 RAG failed to find information - routing to Web search for fallback")
        return "Web"
    else:
        print("✅ Proceeding to Final output")
        return "Final"

# ========== Final Output Node ==========
def final_node(state: AgentState):
    return {"messages": [f"✅ Final Answer: {state['messages'][-1]}"]}