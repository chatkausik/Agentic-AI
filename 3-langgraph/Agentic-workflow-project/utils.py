import time
import json
from typing import Dict, Any, List

def format_response_for_display(response: str) -> str:
    """Format response text for better display"""
    if response.startswith("✅ Final Answer: "):
        return response[17:]  # Remove prefix
    return response

def calculate_response_metrics(text: str) -> Dict[str, Any]:
    """Calculate basic metrics for a response"""
    return {
        "character_count": len(text),
        "word_count": len(text.split()),
        "sentence_count": len([s for s in text.split('.') if s.strip()]),
        "has_punctuation": any(char in text for char in '.,!?'),
        "avg_words_per_sentence": len(text.split()) / max(1, len([s for s in text.split('.') if s.strip()]))
    }

def get_validation_summary(validation_scores: List[Dict]) -> Dict[str, Any]:
    """Get summary statistics from validation scores"""
    if not validation_scores:
        return {}
    
    scores = [v.get('score', 0) for v in validation_scores]
    all_issues = []
    for v in validation_scores:
        all_issues.extend(v.get('issues', []))
    
    return {
        "attempts": len(validation_scores),
        "max_score": max(scores) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "total_retries": sum(v.get('retry_count', 0) for v in validation_scores),
        "unique_issues": list(set(all_issues)),
        "final_score": scores[-1] if scores else 0
    }

def timestamp_to_readable(timestamp: str) -> str:
    """Convert timestamp to readable format"""
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
    except:
        return timestamp

def save_conversation_history(history: List[Dict], filename: str = "conversation_history.json"):
    """Save conversation history to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving conversation history: {e}")
        return False

def load_conversation_history(filename: str = "conversation_history.json") -> List[Dict]:
    """Load conversation history from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading conversation history: {e}")
        return []

def print_workflow_results(result: Dict[str, Any], show_details: bool = True):
    """Print workflow results in a formatted way"""
    print("\n" + "="*60)
    print("🤖 AGENTIC WORKFLOW RESULTS")
    print("="*60)
    
    # Extract final answer
    final_answer = result['messages'][-1]
    if final_answer.startswith("✅ Final Answer: "):
        final_answer = final_answer[17:]
    
    print(f"\n📝 RESPONSE:")
    print(f"{final_answer}")
    
    if show_details and 'validation_scores' in result:
        validation_summary = get_validation_summary(result['validation_scores'])
        if validation_summary:
            print(f"\n📊 VALIDATION SUMMARY:")
            print(f"   • Final Score: {validation_summary['final_score']}/100")
            print(f"   • Attempts: {validation_summary['attempts']}")
            print(f"   • Total Retries: {validation_summary['total_retries']}")
            if validation_summary['unique_issues']:
                print(f"   • Issues Found: {', '.join(validation_summary['unique_issues'])}")
    
    print("\n" + "="*60)

def get_source_emoji(source: str) -> str:
    """Get emoji for different sources"""
    source_emojis = {
        "RAG": "📚",
        "Web": "🌐", 
        "LLM": "🧠",
        "Supervisor": "👨‍💼"
    }
    return source_emojis.get(source, "🤖")