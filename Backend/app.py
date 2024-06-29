from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from Controller import ChatController

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

class Item(BaseModel):
    question: str

@app.post("/api/chat/ask")
async def ask(question):
    chat_controller = ChatController()
    return await chat_controller.ask(question)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
