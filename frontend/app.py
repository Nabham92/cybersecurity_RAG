import gradio as gr 
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8001"

def chat_fn(prompt,history):

    message={"prompt" : prompt}
    print(message)
    request_url=BASE_URL+"/chat"

    print(request_url)

    response=requests.post(request_url,json=message)

    print(response.status_code)
    res = response.json()

    last_message = res["messages"][-1]["content"]

    return last_message

if __name__=="__main__" : 
    gr.ChatInterface(chat_fn).launch(debug=True)