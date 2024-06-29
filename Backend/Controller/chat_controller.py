from fastapi.responses import StreamingResponse
from Services import OpenaiService 

class ChatController:

    def __init__(self):
        print("init ChatController")

    async def ask(self, question: str):
        openai_service = OpenaiService()
        return StreamingResponse(openai_service.call_openai_with_streaming(question))