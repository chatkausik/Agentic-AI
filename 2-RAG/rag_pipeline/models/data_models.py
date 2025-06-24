from dataclasses import dataclass
from typing import Any, Dict
import numpy as np

@dataclass
class DocumentChunk:
    """Represents a semantic chunk of document content"""
    text: str
    metadata: Dict[str, Any]
    embedding: np.ndarray = None
    chunk_id: str = None