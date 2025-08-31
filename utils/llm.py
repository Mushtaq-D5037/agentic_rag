import time
import requests
from utils import prompts
from configure import (
    GROQ_API_KEY,
    GROQ_API_URL,
    GROQ_MODEL,
    GROQ_MODEL2
)
import importlib
importlib.reload(prompts)


# Validate config
if not GROQ_API_KEY or not GROQ_MODEL:
    raise EnvironmentError("Missing GROQ_API_KEY or GROQ_MODEL in environment variables.")


def call_llm_api(payload: dict) -> str:
    """
    Makes a POST request to the LLM API and returns the response content.
    Retries on 429 Too Many Requests using exponential backoff.
    """
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 429:
            raise requests.exceptions.HTTPError("429 Too Many Requests")

        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()

    except requests.exceptions.HTTPError as e:
        raise
    except requests.exceptions.RequestException as e:
        raise
    except KeyError:
        raise


def generate_relevance_score(query: str, document: str) -> str:
    """
    Generates a relevance score between the query and a document.
    """
    if not query or not document:
        raise ValueError("Both query and document must be non-empty strings.")
    payload = {
        "model": GROQ_MODEL2,
        "messages": [
            {"role": "user", "content": prompts.generate_relevance_score(query, document)}
        ],
        "temperature": 0.5
    }
    return call_llm_api(payload)


def generate_response( query: str, 
                       retrieved_results: str,
                       prompt_template= None, 
                       model_name:str = None
                    ) -> str:
    
    start_time = time.time()
    
    # Your existing validation and payload creation here...
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    # getting model from front-end
    model_to_use = model_name or GROQ_MODEL  # fallback to env variable
    print("ModelName:", model_name)

    payload = {
        "model": model_to_use,
        "messages": [
            # {"role": "user", "content": prompts.response_generation(query, retrieved_results)}
            {"role": "user", "content": prompt_template}
        ],
        "temperature": 0.7
    }
 
    try:
        response = call_llm_api(payload)
        end_time = time.time()
        elapsed_ms = int((end_time - start_time) * 1000)

        
        return response, elapsed_ms

    except Exception as e:
        print(f"Error generating response for query: {query}. Exception: {e}")
        raise





    

    
    
