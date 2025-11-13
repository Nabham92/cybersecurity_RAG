import os
from ollama import Client
from backend.create_db import get_client
from backend.format_prompt import filter_metadata
from config import COLLECTION_NAME,METADATAS_TO_INCLUDE

def get_ollama_client():
    os.environ["OLLAMA_API_KEY"] = r"95ebea5be5164fa2ba9b0a7c1f36b227.ei7XxrMXMYf_DWqiaTzh4ba6"

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )

    return(client)

def get_collection():
    client=get_client()
    collection=client.get_collection(COLLECTION_NAME)
    return(collection)

def retrieve(query,n_results):

    collection=get_collection()
    retrieval=collection.query(query_texts=[query],n_results=n_results)

    return(retrieval)

def get_message(prompt):

    messages = [{   'role': 'user',
            'content': prompt},]
    
    return(messages)

def get_rag_prompt(query,n_results=1):
    retrieval=retrieve(query,n_results)
    retrieval["metadatas"]=filter_metadata(retrieval,METADATAS_TO_INCLUDE,n_results)

    rag_prompt=f"""{query} Answer leveraging the following context 
        Documents : {retrieval["documents"]},
    Metadata : {retrieval["metadatas"]}"""

    return(rag_prompt)

def get_message(prompt):

    messages = [{   'role': 'user',
            'content': prompt},]
    
    return(messages)

def get_prediction_prompt(description,n_results=3):
    retrieval=retrieve(description,n_results=n_results)

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
                {description}

                Retrieved context:
                Document : {retrieval["documents"]},
                 Metadatas : {retrieval["metadatas"]},
                 Similarity : { [1 - d for d in retrieval["distances"][0]] }
        """
    
    return(rag_prompt)

def rag_inference(prompt):
    client = get_ollama_client()
    messages = get_message(prompt)

    print(messages)

    full_text = ""

    for part in client.chat('gpt-oss:20b', messages=messages, stream=True):
        message = part.get("message", {})
        chunk = message.get("content")

        
        if chunk:
            full_text += chunk
            print(chunk, end="", flush=True)

    return full_text

from backend.format_prompt import get_rag_prompt

def get_rag_answer(query,n_results=5): 
    rag_prompt=get_rag_prompt(query,n_results=n_results)
    return(rag_inference(rag_prompt))

if __name__=="__main__":
    query=input("Ask : ")
    #get_rag_answer(query)

