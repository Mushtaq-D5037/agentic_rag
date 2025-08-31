from utils import llm

def format_search_results(results):
    return "----".join(doc['body'] for doc in results)

def re_rank_docs(docs_list, query):
    for doc in docs_list:
        score = llm.generate_relevance_score(query, doc["body"])
        doc["llm_score"] = float(score) if score.replace('.', '', 1).isdigit() else score  # cast if possible
        print(score, doc['title'])

    # Sort docs by llm_score descending
    docs_list.sort(key=lambda x: x["llm_score"] if isinstance(x["llm_score"], float) else 0.0, reverse=True)
    sorted_docs = docs_list
    return sorted_docs