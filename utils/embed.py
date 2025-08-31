# importing py files
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from configure import EMBEDDING_MODEL_NAME


dense_embedding_model= SentenceTransformer(EMBEDDING_MODEL_NAME, cache_folder ='../../.models/huggingface', trust_remote_code=True)
bm25_embedding_model = SparseTextEmbedding("Qdrant/bm25", cache_dir='../../.models/fastembed')
colbert_embedding_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0", cache_dir='../../.models/fastembed')
    
    
def dense_embedding(text: str) -> list:
    """
    Returns a 768-dim embedding vector normalized.
    """
    embedding = dense_embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
    
def sparse_embedding(text:str) -> list:
    
    bm25_embeddings = list(bm25_embedding_model.passage_embed(text))
    return bm25_embeddings

def late_interaction_embedding(text:str) -> list:
    colbert_embeddings = list(colbert_embedding_model.passage_embed(text))

    return colbert_embeddings
