import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.models import PointStruct
from Services.openai_service import OpenaiService


# docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
class QdrantService:

    def __init__(self) -> None:
        self.openai_service = OpenaiService()
        self.client = QdrantClient("http://localhost:6333")
        pass
    
    def create_collection(self, collection_name: str):
        if self.client.collection_exists(collection_name=collection_name) == True:
            print(f"Collection '{collection_name}' already exists")
        else:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE,
                ),
            )
        print(f"Connected to Qdrant and created collection '{collection_name}'")

    def insert_vectors(self, content):
        embeddings = self.openai_service.create_embedding(content)
        self.create_collection("exceldocuments")
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=data.embedding,
                payload={"text": text},
            )
            for idx, (data, text) in enumerate(zip(embeddings.data, content))
        ]
        self.client.upsert("exceldocuments", points)
        print(f"Inserted {len(points)} vectors into collection")

    def search_vectors(self, collection_name: str, query: str):
        embeddings = self.openai_service.create_embedding(query).data[0].embedding
        vector_results = self.client.search(
            collection_name=collection_name,
            query_vector=embeddings,
        )
        return vector_results

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(collection_name=collection_name)
        print(f"Deleted collection '{collection_name}'")
