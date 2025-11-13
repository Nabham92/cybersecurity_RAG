import gradio as gr 
from backend.rag_inference import get_rag_answer, get_prediction_prompt,rag_inference

def chat_fn(message, history):
    prompt=get_prediction_prompt(message)
    return str(rag_inference(prompt))

gr.ChatInterface(chat_fn).launch(debug=True)