import json
from typing import List
from fastapi.responses import StreamingResponse
from qdrant_client.http.models.models import ScoredPoint
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
        vector_results: List[ScoredPoint] = self.qdrant_service.search_vectors(collection, question)
        llm_query: str = self.openai_service.build_llm_document_query(question, vector_results)
        return StreamingResponse(self.openai_service.call_openai_with_streaming(llm_query, data))
    
    async def ask_image(self, image_base64: str, question: str):
        return StreamingResponse(self.openai_service.read_image(image_base64, question))
    
    def ask_audio(self, audio) -> StreamingResponse:
        return StreamingResponse(self.openai_service.read_audio(audio))
    

    def summarize_json(self, history: list):
        prompt = "Summarize the content of the last assistant message and return it in a JSON format please format it as a Array with objects that are all simmilar structure, please only return the JSON nothing else"
        result: str = self.openai_service.call_openai_without_streaming(history=history, question=prompt)
        result: str = result.replace("```json", "").replace("```", "")
        json_data: list = json.loads(result)
        return json_data

