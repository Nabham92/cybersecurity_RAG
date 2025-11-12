import os
from ollama import Client

def get_ollama_client():
    #os.environ["OLLAMA_API_KEY"] = 

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )

    return(client)

def rag_inference(prompt) : 
    client= get_ollama_client()

    messages = [
    {
        'role': 'user',
        'content': prompt,
    },
    ]

    for part in client.chat('gpt-oss:20b', messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)

from format_prompt import get_rag_prompt

def main(query,n_results=5): 
    rag_prompt=get_rag_prompt(query,n_results=n_results)

    rag_inference(rag_prompt)
    return()

if __name__=="__main__":
    query=input("Ask : ")
    main(query)

