from fastapi import FastAPI
from backend.rag_inference import get_prediction_prompt,rag_inference

app=FastAPI()

@app.post("/chat")

def inference(query):
    rag_prompt=get_prediction_prompt(query)
    answer=str(rag_inference(rag_prompt))

    output={"model" : "gpt-oss:20b",
            "messages" : [ {"role" : "user" , "content" : query},
                          {"role" : "system" , "content" : answer}
                          ]
            }   
    
    return(output)



