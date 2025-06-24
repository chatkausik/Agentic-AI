from typing import List
import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class SemanticChunker:
    """Implements semantic chunking using sentence similarity"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained('gpt2')
        
    def chunk_text(self, text: str, max_chunk_size: int = 512, 
                   similarity_threshold: float = 0.7) -> List[str]:
        """Perform semantic chunking based on sentence similarity"""
        sentences = sent_tokenize(text)
        if not sentences:
            return []
            
        # Get embeddings for all sentences
        sentence_embeddings = self.model.encode(sentences)
        
        chunks = []
        current_chunk = [sentences[0]]
        current_tokens = len(self.tokenizer.encode(sentences[0]))
        
        for i in range(1, len(sentences)):
            sentence = sentences[i]
            sentence_tokens = len(self.tokenizer.encode(sentence))
            
            # Check if adding this sentence would exceed token limit
            if current_tokens + sentence_tokens > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens
                continue
            
            # Calculate similarity with last sentence in current chunk
            similarity = cosine_similarity(
                [sentence_embeddings[i-1]], 
                [sentence_embeddings[i]]
            )[0][0]
            
            if similarity >= similarity_threshold:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks