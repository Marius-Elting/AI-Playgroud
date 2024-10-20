import io
import json
from typing import Any
from fastapi import FastAPI, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
import uvicorn

from Ingestion.export_xls import ExcelExporter
from Controller import ChatController, DocumentController
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

@app.post("/api/chat/ask")
async def ask(question:str =  Form(...)) -> StreamingResponse:
    chat_controller = ChatController()
    return await chat_controller.ask(question=question)


@app.post("/api/chat/ask_document")
async def ask_document(question:str =  Form(...), collection: str = Form(...)) -> StreamingResponse:
    chat_controller = ChatController()
    return await chat_controller.ask_data(question=question, collection=collection)

@app.post("/api/chat/ask_image")
async def upload_image_and_question(image: UploadFile, message: str = Form(...)) -> StreamingResponse:
    image_data = await image.read() 
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    chat_controller = ChatController()
    return await chat_controller.ask_image(image_base64=image_base64, question=message)

@app.post("/api/chat/upload_audio")
async def ask_question_adio(audio: UploadFile) -> StreamingResponse:
    audio_data: bytes = await audio.read()
    buffer = io.BytesIO(initial_bytes=audio_data)
    buffer.name = "file.webm" 
    chat_controller = ChatController()
    return chat_controller.ask_audio(audio=buffer)


@app.post("/api/chat/upload")
async def upload_file(file: UploadFile = File(...)):
    document_controller = DocumentController()
    if str(file.filename).endswith(".xls") or str(file.filename).endswith(".xlsx"):
        return document_controller.ingest_excel(file)
    elif str(file.filename).endswith(".pdf"):
        file_data = await file.read()
        return document_controller.ingest_pdf(document=file_data)
    return {"filename": file.filename}


@app.post('/api/chat/get_excel')
def get_data(history: list = Form(...)) -> StreamingResponse:
    excel_exporter: ExcelExporter = ExcelExporter()
    chat_controller: ChatController = ChatController()
    json_data: list[Any] = chat_controller.summarize_json(history=json.loads(history[0]))
    return excel_exporter.export_data_to_excel(data=json_data)



@app.post('/api/chat/generate_image')
def generate_image(prompt: str = Form(...)) :
   return {"image": ChatController().generate_image(prompt=prompt)}




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    x = []
    while True:
        data = await websocket.receive_text()
        print(data)
        x.append(data)
        print(x)
        await websocket.send_text(f"Message text was: {data}")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.chat = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def send_other_users(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint_client(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        await manager.send_other_users(f"Client #{client_id} joined the chat", websocket=websocket)
        while True:
            data = await websocket.receive_text()
            manager.chat.append(f"Client #{client_id} says: {data}")
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.send_other_users(f"Client #{client_id} says: {data}", websocket=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
