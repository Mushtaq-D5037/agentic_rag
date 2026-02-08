"""
Configuration and constants for License Optimizer
"""

# License SKU IDs (Real Microsoft GUIDs)
LICENSE_SKUS = {
    "E5": "6fd2c87f-b296-42f0-b197-1e91e994b900",
    "E3": "05e9a617-0261-4cee-bb44-138d3ef5d965",
    "BUSINESS_PREMIUM": "f245ecc8-75af-4f8e-b61f-27d8114de5f3"
}

# Pricing (USD per month)
LICENSE_COSTS = {
    "6fd2c87f-b296-42f0-b197-1e91e994b900": {"name": "E5", "monthly": 57, "annual": 684},
    "05e9a617-0261-4cee-bb44-138d3ef5d965": {"name": "E3", "monthly": 36, "annual": 432},
    "f245ecc8-75af-4f8e-b61f-27d8114de5f3": {"name": "Business Premium", "monthly": 22, "annual": 264}
}

# Business Rules
INACTIVE_THRESHOLD_DAYS = 90
NEW_HIRE_GRACE_PERIOD_DAYS = 60

# Executive titles (exclude from auto-downgrade recommendations)
EXECUTIVE_KEYWORDS = [
    "CEO", "CFO", "CIO", "COO", "CHRO", "CMO", 
    "Chief", "VP", "Vice President", 
    "General Counsel", "President"
]

# Ollama settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# OLLAMA_MODEL = "llama3.1"
OLLAMA_MODEL = "llama3-groq-tool-use:8b"
OLLAMA_TEMPERATURE = 0.3

# MCP Server settings
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8000
MCP_BASE_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}"

# RAG settings
RAG_DATA_DIR = "rag_data"
FAISS_INDEX_PATH = f"{RAG_DATA_DIR}/license_knowledge.faiss"
EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RAG_TOP_K = 3  # Number of similar documents to retrieve

# File paths
DATA_DIR = "data"
OUTPUT_DIR = "outputs"
USERS_FILE = f"{DATA_DIR}/users_licenses.csv"
FEATURES_FILE = f"{DATA_DIR}/premium_features_usage.csv"
