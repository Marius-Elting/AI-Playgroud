import json
from typing import Any, List
from fastapi.responses import StreamingResponse
from qdrant_client.http.models.models import ScoredPoint
from Services.qdrant_service import QdrantService
from Services import OpenaiService 

class ChatController:
    openai_service: OpenaiService

    def __init__(self) -> None:
        self.openai_service = OpenaiService()
        self.qdrant_service = QdrantService()

    async def ask(self, question: str) -> StreamingResponse:
        return StreamingResponse(content=self.openai_service.call_openai_with_streaming(question=question))
    
    async def ask_data(self, question: str, collection) -> StreamingResponse:
        vector_results: List[ScoredPoint] = self.qdrant_service.search_vectors(collection_name=collection, query=question)
        llm_query: str = self.openai_service.build_llm_document_query(query=question, vector_result=vector_results)
        return StreamingResponse(content=self.openai_service.call_openai_with_streaming(question=llm_query))
    
    async def ask_image(self, image_base64: str, question: str) -> StreamingResponse:
        return StreamingResponse(content=self.openai_service.read_image(base64_image=image_base64, question=question))
    
    def ask_audio(self, audio) -> StreamingResponse:
        return StreamingResponse(content=self.openai_service.read_audio(audio))

    def summarize_json(self, history: list)-> list[Any]:
        prompt = "Summarize the content of the last assistant message and return it in a JSON format please format it as a Array with objects that are all simmilar structure, please only return the JSON nothing else"
        result: str = self.openai_service.call_openai_without_streaming(history=history, question=prompt)
        result: str = result.replace("```json", "").replace("```", "")
        json_data: list = json.loads(result)
        return json_data

    def generate_image(self, prompt: str) :
        return self.openai_service.generate_image(prompt=prompt)