def decision_prompt(query: str, context: str) -> str:
    decision_prompt = f""" You are an decision-making agent. Based on the provided context, Your job is to decide if a given query can be answered with the provided context.
    If context can answer the query, respond with "YES". If not, respond with "NO".
    Do not provide any additional information or explanation, just respond with "YES" or "NO".
    query: {query}
    Context: {context}
    Answer:
    """
    return decision_prompt


def response_generation(user_query, retrieved_docs):
    
    # retrived docs
    context = "\n\n------\n\n".join(retrieved_docs)

    response_prompt = f"""
    Your are an intelligent AI Assistant, you'll be provided with a query and context, your job is to answer the query based only on the provided context.
    If you do not find any relevant context to the query, respond clearly and politely with "No relevant context were found. You may try rephrasing your question for better results" — strictly do not make up an answer.
    Present the response in a **conversational** and **easy-to-read** format. Avoid sounding robotic or overly formal.
    Structure your answer using headings, bullet points, bold text, or numbering — whichever improves clarity
    User Query: {user_query}
    Context: {context}
    Answer:
    
    """.strip()
    
    return response_prompt


def generate_relevance_score(query, document):
    
    return f""" 
    Your are an intelligent AI Assistant, you'll be provided with a query and a document, your job is to analyze the query and document
    rate the relevance of this document to the query on a scale from 1 to 5.
    
    - strictly return a float between 1 to 5
    - Do NOT include any introductory text, labels, or explanations
    
    Query: {query}
    
    Document: {document}
    
    """

