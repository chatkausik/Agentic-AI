#!/usr/bin/env python3
"""
Modular Agentic AI Workflow - Main Entry Point
A sophisticated AI workflow system that intelligently routes queries between
RAG (document-based), Web search, and LLM responses with validation and retry mechanisms.
"""

from workflow import create_workflow, run_query
from utils import print_workflow_results
import argparse
import sys

def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(
        description="Agentic AI Workflow - Intelligent Query Processing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --query "What are symptoms of anxiety?"
  python main.py --query "What's the current GDP of USA?" --verbose
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        "--query", "-q", 
        type=str, 
        help="Query to process through the workflow"
    )
    
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Show detailed validation information"
    )
    
    args = parser.parse_args()
    
    print("🤖 Agentic AI Workflow System")
    print("=" * 50)
    print("Initializing workflow components...")
    
    try:
        # Initialize the workflow
        app = create_workflow()
        print("✅ Workflow initialized successfully!")
        
        if args.interactive:
            run_interactive_mode(app, args.verbose)
        elif args.query:
            run_single_query(app, args.query, args.verbose)
        else:
            # Default example
            example_query = "What's the GDP of USA?"
            print(f"\n🔍 Running example query: '{example_query}'")
            run_single_query(app, example_query, args.verbose)
            
    except Exception as e:
        print(f"❌ Error initializing workflow: {str(e)}")
        sys.exit(1)

def run_single_query(app, query, verbose=False):
    """Run a single query through the workflow"""
    print(f"\n🔍 Processing query: '{query}'")
    print("-" * 50)
    
    try:
        result = run_query(app, query)
        print_workflow_results(result, show_details=verbose)
        
    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")

def run_interactive_mode(app, verbose=False):
    """Run the workflow in interactive mode"""
    print("\n🎯 Interactive Mode - Type 'quit' or 'exit' to stop")
    print("💡 Example queries:")
    print("   • What are effective treatments for depression?")
    print("   • What's the latest news in AI?")
    print("   • How can I manage stress?")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n❓ Enter your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not query:
                print("⚠️  Please enter a question.")
                continue
                
            print(f"\n🔍 Processing: '{query}'")
            print("-" * 50)
            
            result = run_query(app, query)
            print_workflow_results(result, show_details=verbose)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()