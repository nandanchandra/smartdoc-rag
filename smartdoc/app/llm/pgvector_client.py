from app.llm.ollama_client import ollama_client
from app.utils.switch_db_url import get_db_url
from langchain_postgres import PGVector


class PGVectorClient:

    def __init__(self):
        self.connection_string = get_db_url(async_mode=False)
        self.embedding_function = ollama_client.embedder

    def generate_document_embeddings(self, user_id: int, text: str, file_name: str):

        collection_name = f"user_{user_id}_docs_{file_name}"

        chunks = ollama_client.generate_chunks(text)

        vector_store = PGVector(
            connection=self.connection_string,
            collection_name=collection_name,
            embeddings=self.embedding_function,
        )
        vector_store.add_texts(
            texts=[chunk for chunk in chunks],
            metadatas=[
                {"file_name": file_name, "user_id": user_id} for chunk in chunks
            ],
        )

        return collection_name


pgvector_client = PGVectorClient()
