import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

class qdrant_vDB:
    def __init__(self):
        self.qdrant_cluster_url = os.getenv('QDRANT_CLUSTER_URL')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')

    def get_qdrant_client(self):
        qdrant_client = QdrantClient(url=self.qdrant_cluster_url,
                                     api_key=self.qdrant_api_key
                                    )
        return qdrant_client