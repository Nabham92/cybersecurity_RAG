import gradio as gr 
from backend.app.rag.rag_inference import get_rag_answer
import requests


BASE_URL=r"http://127.0.0.1:8001"

def chat_fn(prompt):

    message={"prompt" : prompt}

    request_url=BASE_URL+"/chat"
    print(request_url)

    response=requests.post(request_url,json=message)

    print(response.status_code)

    return response

#gr.ChatInterface(chat_fn).launch(debug=True)

if __name__=="__main__" : 
    chat_fn("hi")