import os
from ollama import Client
from backend.app.database.vector_store import get_chroma_client,get_collection
from config import COLLECTION_NAME,METADATAS_TO_INCLUDE
from dotenv import load_dotenv

load_dotenv()

def get_ollama_client():
    os.environ["OLLAMA_API_KEY"] = os.getenv("API_KEY")

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )
    return(client)

def retrieve(query,collection_name,n_results=3):

    client=get_chroma_client()

    collection=get_collection(client,collection_name)

    retrieval=collection.query(query_texts=[query],n_results=n_results)
    
    return(retrieval)

def get_message(prompt):

    messages = [{   'role': 'user',
            'content': prompt},]
    
    return(messages)

def get_rag_prompt(prompt,collection_name=COLLECTION_NAME,n_results=3):

    retrieval=retrieve(prompt,collection_name,n_results=n_results)

    rag_prompt=f""" You are a cybersecurity analyst specialized in CVSS:3.1 scoring.

                Your task is to predict the most likely CVSS:3.1 vector based on:
                1) the vulnerability description
                2) the RAG-retrieved similar vulnerabilities

                Steps:
                - First output the predicted vector (strict format).
                - Then briefly justify each metric (AV, AC, PR, UI, S, C, I, A).
                - Output a score or severity.
                - Suggest fixes and what to investigate.

                Output format (STRICT):
                Vector: CVSS:3.1/AV:X/AC:X/PR:X/UI:X/S:X/C:X/I:X/A:X
                Justification:
                - AV: ...
                - AC: ...
                - PR: ...
                - UI: ...
                - S: ...
                - C: ...
                - I: ...
                - A: ...

                Input description:
                {prompt}

                Retrieved context:
                Document : {retrieval["documents"]},
                 Metadatas : {retrieval["metadatas"]},
                 Similarity : { [1 - d for d in retrieval["distances"][0]] }
        """
    
    return(rag_prompt)

def get_rag_answer(prompt):

    ollama_client = get_ollama_client()

    prompt=get_rag_prompt(prompt,COLLECTION_NAME)

    messages = get_message(prompt)

    full_text = ""

    for part in ollama_client.chat('gpt-oss:20b', messages=messages, stream=True):
        message = part.get("message", {})
        chunk = message.get("content")

        if chunk:
            full_text += chunk
            print(chunk, end="", flush=True)

    return full_text

if __name__=="__main__":
    get_rag_answer()

