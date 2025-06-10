"""
Modular Agentic AI Workflow Application
This module provides a simplified interface to the workflow system.
"""

from workflow import create_workflow, run_query
from utils import print_workflow_results, save_conversation_history, load_conversation_history
import time

class AgenticWorkflowApp:
    """Main application class for the Agentic AI Workflow"""
    
    def __init__(self):
        self.app = None
        self.conversation_history = []
        self.initialized = False
    
    def initialize(self):
        """Initialize the workflow application"""
        print("🚀 Initializing Agentic AI Workflow...")
        try:
            self.app = create_workflow()
            self.conversation_history = load_conversation_history()
            self.initialized = True
            print("✅ Application initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize application: {str(e)}")
            return False
    
    def ask_question(self, question: str, save_to_history: bool = True) -> dict:
        """Process a question through the workflow"""
        if not self.initialized:
            raise RuntimeError("Application not initialized. Call initialize() first.")
        
        print(f"\n🤔 Processing: {question}")
        start_time = time.time()
        
        try:
            result = run_query(self.app, question)
            processing_time = time.time() - start_time
            
            if save_to_history:
                conversation_entry = {
                    'question': question,
                    'answer': result['messages'][-1],
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'processing_time': round(processing_time, 2),
                    'validation_scores': result.get('validation_scores', [])
                }
                self.conversation_history.append(conversation_entry)
                save_conversation_history(self.conversation_history)
            
            return result
            
        except Exception as e:
            print(f"❌ Error processing question: {str(e)}")
            raise
    
    def get_conversation_history(self, limit: int = None) -> list:
        """Get conversation history, optionally limited to recent entries"""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        save_conversation_history(self.conversation_history)
        print("🗑️ Conversation history cleared!")

def demo():
    """Run a demonstration of the workflow"""
    app = AgenticWorkflowApp()
    
    if not app.initialize():
        return
    
    # Demo questions
    demo_questions = [
        "What are effective treatments for depression?",
        "What's the current GDP of the United States?",
        "How can I manage stress and anxiety?"
    ]
    
    print("\n🎭 Running Demo Queries...")
    print("=" * 50)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n📝 Demo Query {i}/{len(demo_questions)}")
        try:
            result = app.ask_question(question)
            print_workflow_results(result, show_details=True)
        except Exception as e:
            print(f"❌ Demo query failed: {str(e)}")
        
        if i < len(demo_questions):
            print("\n" + "-" * 30)
    
    print(f"\n📊 Demo completed! Processed {len(demo_questions)} queries.")
    print(f"💾 Conversation history saved with {len(app.get_conversation_history())} total entries.")

if __name__ == "__main__":
    demo()