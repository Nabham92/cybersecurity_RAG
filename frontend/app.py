import gradio as gr 
from backend.app.rag.rag_inference import get_rag_answer

def chat_fn(message, history):
    answer=get_rag_answer(message)
    return str(answer)

gr.ChatInterface(chat_fn).launch(debug=True)