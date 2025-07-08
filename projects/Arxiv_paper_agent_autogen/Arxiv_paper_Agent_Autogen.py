from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
import arxiv
from typing import List,Dict,AsyncGenerator

# Initialize OpenAI client with error handling
def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    return OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """Return a compact list of arXiv papers matching *query*.
    Each element contains: ``title``, ``authors``, ``published``, ``summary`` and
    ``pdf_url``.  The helper is wrapped as an AutoGen *FunctionTool* below so it
    can be invoked by agents through the normal tool‑use mechanism.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers: List[Dict] = []
        for result in client.results(search):
            papers.append(
                {
                    "title": result.title,
                    "authors": [a.name for a in result.authors],
                    "published": result.published.strftime("%Y-%m-%d"),
                    "summary": result.summary,
                    "pdf_url": result.pdf_url,
                }
            )
        return papers
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []

# Initialize agents with error handling
def initialize_agents():
    try:
        openai_brain = get_openai_client()
        
        arxiv_researcher_agent = AssistantAgent(
            name='arxiv_search_agent',
            description='Create arXiv queries and retrieves candidates papers',
            model_client=openai_brain,
            tools=[arxiv_search],
            system_message=(
                    "Given a user topic, think of the best arXiv query. When the tool "
                    "returns, choose exactly the number of papers requested and pass "
                    "them as concise JSON to the summarizer."
                ),
        )
        
        summarizer_agent = AssistantAgent(
            name='summarizer_agent',
            description = 'An agent which summarizes the result',
            model_client=openai_brain,
            system_message=(
                    "You are an expert researcher. When you receive the JSON list of "
                    "papers, write a comprehensive literature review style report with proper formatting:\n"
                    "1. Start with a clear title: '# Literature Review: [Topic]'\n"
                    "2. Add a 2-3 sentence introduction explaining the topic's importance\n"
                    "3. Create a section '## Key Papers' with each paper formatted as:\n"
                    "   - **Title**: [Paper Title]([PDF URL])\n"
                    "   - **Authors**: [Author List]\n"
                    "   - **Published**: [Date]\n"
                    "   - **Problem**: [Brief description of the problem tackled]\n"
                    "   - **Key Contribution**: [Main contribution/innovation]\n"
                    "   - **Summary**: [2-3 sentence summary]\n\n"
                    "4. End with a '## Conclusion' section with key takeaways and future directions\n"
                    "Make the output clean, well-structured, and easy to read."
                ),
        )
        
        team = RoundRobinGroupChat(
            participants=[arxiv_researcher_agent, summarizer_agent],
            max_turns=2
        )
        
        return team
    except Exception as e:
        raise Exception(f"Failed to initialize agents: {str(e)}")

async def run_team(topic: str = 'Autogen', num_papers: int = 5):
    try:
        team = initialize_agents()
        task = f'Conduct a literature review on the topic - {topic} and return exactly {num_papers} papers.'
        
        result = await team.run(task=task)
        
        # Extract the final message content
        if hasattr(result, 'messages') and result.messages:
            # Get the last message from the conversation
            final_message = result.messages[-1]
            if hasattr(final_message, 'content'):
                return final_message.content
            else:
                return str(final_message)
        elif hasattr(result, 'content'):
            return result.content
        else:
            return str(result)
    except Exception as e:
        return f"Error generating literature review: {str(e)}"

async def get_literature_review(topic: str, num_papers: int = 5):
    """Main function to get literature review for a given topic"""
    try:
        return await run_team(topic, num_papers)
    except Exception as e:
        print(f"Error in get_literature_review: {e}")
        return f"Error generating literature review: {str(e)}"

if (__name__=='__main__'):
    asyncio.run(run_team())