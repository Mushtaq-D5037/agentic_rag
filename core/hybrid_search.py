from utils import ( 
embed, 
llm
)
from utils.qdrant_connect import qdrant_vDB
from qdrant_client import models
from configure import (
DENSE_EMBEDDING_NAME,
SPARSE_EMBEDDING_NAME,
LATE_INTERACTION_EMBEDDING_NAME,
QDRANT_COLLECTION_NAME   
)
import importlib
import configure
from utils import prompts
importlib.reload(configure)
importlib.reload(prompts)

# # Initialize Qdrant client
client = qdrant_vDB().get_qdrant_client()

def full_rrf_search(dense_query_vector, sparse_query_vector_obj, late_query_vector, COLLECTION, limit_1=25, limit_2=7):
    prefetch = [
        models.Prefetch(
            query=dense_query_vector,
            using=DENSE_EMBEDDING_NAME,
            limit=limit_1,
        ),
        models.Prefetch(
            query=models.SparseVector(**sparse_query_vector_obj),
            using=SPARSE_EMBEDDING_NAME,
            limit=limit_1,
        ),
        models.Prefetch(
            query=late_query_vector,
            using=LATE_INTERACTION_EMBEDDING_NAME,
            limit=limit_1,
        ),
    ]

    results = client.query_points(
        collection_name=COLLECTION,
        prefetch=prefetch,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        with_payload=True,
        limit=limit_2,
    )
    return results


def retreive_relevant_docs(query, search_type=full_rrf_search, topK=5):
    
    
    print('Searching for relevant documents in the vector database...')
    dense_query_vector = embed.dense_embedding(query)
    sparse_query_vector_obj = embed.sparse_embedding(query)[0].as_object()
    late_query_vector = embed.late_interaction_embedding(query)[0]

    search_results =  search_type(dense_query_vector, sparse_query_vector_obj, late_query_vector, QDRANT_COLLECTION_NAME)

    docs_with_meta = []

    for hit in search_results.points:
        # Extract metadata & scores
        article_number = hit.payload.get('article_number')
        article_title = hit.payload.get('article_title')
        article_description = hit.payload.get('article_description')
        article_law = hit.payload.get('article_law_no')
        article_page_number = hit.payload.get('article_page_number')
        article_source=hit.payload.get('article_source')
        qdrant_id = hit.id
        qdrant_score = hit.score  # similarity score from Qdrant

        # Format full text of the document to send to LLM
        article_full = (
            f"Article Law:{article_law}\n\n"
            f"Article Number:{article_number}\n\n"
            f"Article Title:{article_title}\n\n"
            f"Article Description:{article_description}"
        )

        # appending 
        docs_with_meta.append({
            "qdrant_id": qdrant_id,
            "qdrant_score": qdrant_score,
            "article_number": article_number,
            "article_title": article_title,
            "article_law": article_law,
            "article_full": article_full,  # for scoring below
            "article_page_number":article_page_number,
            "article_source":article_source
        })

    # Deduplicate based on article_full text
    seen = set()
    unique_docs = []
    for d in docs_with_meta:
        if d["article_full"] not in seen:
            seen.add(d["article_full"])
            unique_docs.append(d)

    print("Re-ranking docs using LLM...")
    # Re-ranking with LLM relevance scores
    for doc in unique_docs:
        score = llm.generate_relevance_score(query, doc["article_full"])
        doc["llm_score"] = float(score) if score.replace('.', '', 1).isdigit() else score  # cast if possible
        print(score, doc['article_number'])

    # Sort docs by llm_score descending
    unique_docs.sort(key=lambda x: x["llm_score"] if isinstance(x["llm_score"], float) else 0.0, reverse=True)
    sorted_docs = unique_docs[:topK]
    
    # Prepare metadata-only list for logging (exclude article_full)
    metadata = [
        {
        "qdrant_id": d["qdrant_id"],
        "qdrant_score": d["qdrant_score"],
        "llm_score": d["llm_score"],
        "article_number": d["article_number"],
        "article_title": d["article_title"],
        "article_law": d["article_law"],
        "article_page_number": d["article_page_number"],
        "article_source":d["article_source"]
        } 
        for d in sorted_docs
        ]
    
    
    # adding source to each document to track for source citation
    retrieved_docs = [f"SOURCE [{i+1}]:\n{d['article_full']}" for i, d in enumerate(sorted_docs)]

    return retrieved_docs

