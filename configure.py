# configure.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

#  === Qdrant ===
DENSE_EMBEDDING_NAME  = os.getenv('QDRANT_DENSE_EMBEDDING_VECTOR_NAME')
SPARSE_EMBEDDING_NAME = os.getenv('QDRANT_SPARSE_EMBEDDING_VECTOR_NAME')
LATE_INTERACTION_EMBEDDING_NAME = os.getenv('QDRANT_LATE_INTERACTION_EMBEDDING_VECTOR_NAME')
QDRANT_COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME')

# === Embedding & LLM Config ===
# EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME") 
GROQ_API_KEY= os.getenv('GROQ_API_KEY')
GROQ_API_URL= os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
GROQ_MODEL  = os.getenv('GROQ_MODEL')
GROQ_MODEL2 = os.getenv('GROQ_MODEL2')
