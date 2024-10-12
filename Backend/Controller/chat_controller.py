from fastapi.responses import StreamingResponse
from Services.qdrant_service import QdrantService
from Services import OpenaiService 

class ChatController:
    openai_service: OpenaiService

    def __init__(self):
        self.openai_service = OpenaiService()
        self.qdrant_service = QdrantService()

    async def ask(self, question: str):
        return StreamingResponse(self.openai_service.call_openai_with_streaming(question))
    
    async def ask_data(self, question: str, collection):
        data = "data"
        vector_results = self.qdrant_service.search_vectors(collection, question)
        llm_query = self.openai_service.build_llm_document_query(question, vector_results)
        return StreamingResponse(self.openai_service.call_openai_with_streaming(llm_query, data))
    
    async def ask_image(self, image_base64: str, question: str):
        return StreamingResponse(self.openai_service.read_image(image_base64, question))
    
    def ask_audio(self, audio) -> StreamingResponse:
        return StreamingResponse(self.openai_service.read_audio(audio))
    

