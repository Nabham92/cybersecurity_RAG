import chromadb
from config import COLLECTION_NAME,METADATAS_TO_INCLUDE
from backend.create_db import get_client

def get_collection():
    client=get_client()
    collection=client.get_collection(COLLECTION_NAME)
    return(collection)

def retrieve(query,n_results):

    collection=get_collection()
    retrieval=collection.query(query_texts=[query],n_results=n_results)

    return(retrieval)

def filter_metadata(retrieval,METADATAS_TO_INCLUDE,n_results):
    meta={}
    for i in range(0,n_results):
        for key in METADATAS_TO_INCLUDE:
            meta[key]=retrieval["metadatas"][0][i][key]

    return(meta)


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


def get_prediction_prompt(description):
    retrieval=retrieve(description,n_results=3)

    

    rag_prompt=f""" You are a cybersecurity analyst specialized in CVSS:3.1 scoring.

                Your task is to predict the most likely CVSS:3.1 vector based on:
                1) the vulnerability description
                2) the RAG-retrieved similar vulnerabilities

                Steps:
                - First output the predicted vector (strict format).
                - Then briefly justify each metric (AV, AC, PR, UI, S, C, I, A).
                - Do not output a score or severity.

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
                {retrieval["documents"]}
        """
    
    messages=get_message(rag_prompt)
    
    return(messages)

