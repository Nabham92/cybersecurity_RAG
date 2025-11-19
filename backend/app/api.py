from fastapi import FastAPI
from app.rag.rag_inference import get_rag_prompt,get_rag_answer
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt : str

app=FastAPI()

@app.post("/chat")

def inference(data : ChatRequest):    
    answer=get_rag_answer(data.prompt)    
    output={"model" : "gpt-oss:20b",
            "messages" : [ {"role" : "user" , "content" : data.prompt},
                          {"role" : "system" , "content" : answer}
                          ]
            }   
    
    return(output)



