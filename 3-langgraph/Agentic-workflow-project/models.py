import operator
from typing import List, Sequence, TypedDict, Annotated
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    retry_count: int = 0
    last_source: str = ""
    validation_scores: List[dict] = []
    rag_failed: bool = False  # Track if RAG failed to provide useful info

class TopicSelection(BaseModel):
    Topic: str = Field(description="selected topic")
    Reasoning: str = Field(description="reasoning behind topic selection")