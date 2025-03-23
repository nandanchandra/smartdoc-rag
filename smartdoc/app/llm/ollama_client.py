from app.llm.utils.pre_process_text import text_splitter
from app.settings import settings
from langchain_ollama import OllamaEmbeddings
from loguru import logger


class OllamaClient:

    def __init__(self):
        self.model = settings.ollama_model
        self.embedder = OllamaEmbeddings(model=self.model)
        logger.info("OllamaClient initialized with model: %s", self.model)

    def generate_chunks(self, text: str):
        chunks = text_splitter.split_text(text)
        logger.info(f"Document split into {len(chunks)} chunks for embedding.")
        return chunks


ollama_client = OllamaClient()
