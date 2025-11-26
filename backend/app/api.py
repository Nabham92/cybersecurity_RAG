from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from backend.app.rag.rag_inference import get_rag_answer

app = FastAPI()
templates = Jinja2Templates(directory="backend/app/templates")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def inference(data: ChatRequest):
    answer = get_rag_answer(data.prompt)
    return {
        "model": "gpt-oss:20b",
        "messages": [
            {"role": "user", "content": data.prompt},
            {"role": "system", "content": answer}
        ]
    }
