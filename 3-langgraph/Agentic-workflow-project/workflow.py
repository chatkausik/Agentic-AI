from langgraph.graph import StateGraph, END
from models import AgentState
from nodes import (
    supervisor_node, 
    rag_node, 
    llm_node, 
    web_node, 
    validator_node, 
    final_node,
    router,
    retry_router,
    set_retriever
)
from document_loader import create_vector_store

def create_workflow():
    """Create and compile the agentic workflow"""
    
    # Initialize vector store and set retriever
    retriever = create_vector_store()
    set_retriever(retriever)
    
    # Define workflow
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("RAG", rag_node)
    workflow.add_node("LLM", llm_node)
    workflow.add_node("Web", web_node)
    workflow.add_node("Validate", validator_node)
    workflow.add_node("Final", final_node)

    # Set entry point
    workflow.set_entry_point("Supervisor")

    # Add conditional edges
    workflow.add_conditional_edges(
        "Supervisor", router, {"RAG": "RAG", "LLM": "LLM", "Web": "Web"}
    )

    workflow.add_edge("RAG", "Validate")
    workflow.add_edge("LLM", "Validate")
    workflow.add_edge("Web", "Validate")

    workflow.add_conditional_edges(
        "Validate", retry_router, {"Supervisor": "Supervisor", "Final": "Final", "Web": "Web"}
    )

    workflow.add_edge("Final", END)

    # Compile and return app
    app = workflow.compile()
    return app

def run_query(app, question):
    """Run a query through the workflow"""
    state = {"messages": [question]}
    print(f"Initial state: {state}")
    print("Starting the agentic workflow...")
    result = app.invoke(state)
    return result