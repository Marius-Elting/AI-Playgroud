from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams

# Connect to the Qdrant instance


class QdrantService:

    def __init__(self) -> None:

        self.client = QdrantClient("http://localhost:6333")
        pass
    
    def create_collection(self, collection_name: str, vector_size: int = 128, distance: str = "Cosine"):
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config={
                "default": VectorParams(size=vector_size, distance=distance)
            }
        )
        print(f"Connected to Qdrant and created collection '{collection_name}'")

    def insert_vectors(self, collection_name: str, vectors: list, ids: list):
        self.client.insert_vectors(
            collection_name=collection_name,
            vectors=vectors,
            ids=ids
        )
        print(f"Inserted {len(vectors)} vectors into collection '{collection_name}'")

    def search_vectors(self, collection_name: str, query_vector: list, top: int = 5):
        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            top=top
        )
        return search_result

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(collection_name=collection_name)
        print(f"Deleted collection '{collection_name}'")


