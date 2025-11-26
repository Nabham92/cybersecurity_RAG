import os
from ollama import Client
from backend.app.database.vector_store import get_chroma_client,get_collection
from backend.config import COLLECTION_NAME
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

    rag_prompt=rag_prompt = f"""
            You are a cybersecurity analyst.

            Using ONLY the retrieved CVE documents,
            produce a structured analytical summary that includes the following sections:

            1. **Vulnerability Types**
            - List and count attack types (SQLi, XSS, RCE, File Upload, Command Injection…)

            2. **CWE Patterns**
            - Extract CWE families present in the documents.

            3. **Affected Products / Technologies**
            - Name the products, platforms, CMS, plugins, or services impacted.

            4. **Severity Overview**
            - Summarize severity levels present (Low/Medium/High/Critical).

            5. **Attack Vector & Complexity**
            - Mention whether the attacks are Remote/Local
            - Privileges required (PR)
            - User interaction required (UI)

            6. **Impact Summary**
            - Confidentiality / Integrity / Availability effects.

            7. **Short Summary**
            - A 2–3 sentence overview connecting the main patterns.

            Input Query:
            {prompt}

            Retrieved CVE Context:
            {retrieval["documents"]}

            Respond only with structured, factual information from the documents.
            """

    return(rag_prompt)

def normalize_output(text):
    import re
    # remplacer 3+ retours par 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # supprimer les retours inutiles après un mot court
    text = re.sub(r"(?<!\.)\n(?!\n)", " ", text)
    return text

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
            #print(chunk, end="", flush=True)

    return normalize_output(full_text)

if __name__=="__main__":
    get_rag_answer("hi")

