# importing py files
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from configure import EMBEDDING_MODEL_NAME


dense_embedding_model= SentenceTransformer(EMBEDDING_MODEL_NAME, cache_folder ='../.models/huggingface', trust_remote_code=True)
bm25_embedding_model = SparseTextEmbedding("Qdrant/bm25", cache_dir='../.models/fastembed')
colbert_embedding_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0", cache_dir='../.models/fastembed')
    
    
def dense_embedding(text: str) -> list:
    """
    Returns a 768-dim embedding vector normalized.
    """
    embedding = dense_embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
    
    # From fastembed
    # dense_embedding_model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    # dense_embeddings = list(dense_embedding_model.passage_embed(dataset["text"][0:1]))
    # len(dense_embeddings)
    # print(len(dense_embeddings[0]))

    # return dense_embeddings

def sparse_embedding(text:str) -> list:
    
    bm25_embeddings = list(bm25_embedding_model.passage_embed(text))
    return bm25_embeddings

def late_interaction_embedding(text:str) -> list:
    colbert_embeddings = list(colbert_embedding_model.passage_embed(text))

    return colbert_embeddings


# # Testing 
# text = 'Article 34 - Employee Wage: Work permits from the Ministry are mandatory for both employers and employees'
# dense_embedding = dense_embedding(text)
# sparse_embedding = sparse_embedding(text)
# late_embedding = late_interaction_embedding(text)
# print(len(dense_embedding))
# print(sparse_embedding[0].as_object())
# print(len(late_embedding[0]))