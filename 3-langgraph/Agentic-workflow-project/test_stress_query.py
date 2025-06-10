#!/usr/bin/env python3
"""
Test script for stress and anxiety management queries
"""

from workflow import create_workflow, run_query
import os

def test_stress_queries():
    """Test various stress and anxiety related queries"""
    
    # Create the workflow
    print("🚀 Initializing Agentic Workflow...")
    app = create_workflow()
    
    # Test queries
    test_questions = [
        "How to manage stress and anxiety?",
        "What are effective coping strategies for dealing with stress?",
        "Can you give me advice on reducing anxiety?",
        "How can I handle work-related stress better?"
    ]
    
    print("=" * 60)
    print("TESTING STRESS AND ANXIETY QUERIES")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🧪 TEST {i}: {question}")
        print("-" * 50)
        
        try:
            result = run_query(app, question)
            final_answer = result["messages"][-1]
            
            print(f"✅ RESULT:")
            print(final_answer)
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print("-" * 50)
    
    print("\n" + "=" * 60)
    print("Testing completed!")
    print("=" * 60)

if __name__ == "__main__":
    # Check if Tavily API key is available
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        print("⚠️  WARNING: TAVILY_API_KEY not found in environment variables.")
        print("   The web search might not work optimally.")
        print("   To get better results, sign up at https://tavily.com and add your API key to .env file")
        print("   Example: TAVILY_API_KEY=your_api_key_here")
        print()
    
    test_stress_queries()