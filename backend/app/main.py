from fastapi import FastAPI
from backend.app.rag.rag_inference import get_rag_prompt,get_rag_answer
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt : str

app=FastAPI()

BASE_URL=r"http://localhost:8000"

@app.post("/chat")

def inference(data : ChatRequest):
    print(data.prompt)    
    answer=str(get_rag_answer(data.prompt))
    print(answer)    
    output={"model" : "gpt-oss:20b",
            "messages" : [ {"role" : "user" , "content" : data.prompt},
                          {"role" : "system" , "content" : answer}
                          ]
            }   
    
    return(output)



