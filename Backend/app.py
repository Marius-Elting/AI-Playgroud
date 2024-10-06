from typing import Annotated
from fastapi import FastAPI, File, Form
from pydantic import BaseModel
import uvicorn

from Controller import ChatController
from fastapi import UploadFile
import base64
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Item(BaseModel):
    question: str

@app.post("/api/chat/ask")
async def ask(question):
    chat_controller = ChatController()
    return await chat_controller.ask(question)

@app.post("/api/chat/ask_image")
async def upload_image_and_question(image: UploadFile, message: str = Form(...)):
    image_data = await image.read() 
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    chat_controller = ChatController()
    return await chat_controller.ask_image(image_base64=image_base64, question=message)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
