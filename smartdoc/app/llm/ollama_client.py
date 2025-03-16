from app.settings import settings
from langchain.embeddings import OllamaEmbeddings
from loguru import logger


class OllamaClient:

    def __init__(self, model: str = None):
        self.model = model or settings.ollama_model
        self.embedder = OllamaEmbeddings(model=self.model)
        logger.info("OllamaClient initialized with model: %s", self.model)


ollama_client = OllamaClient()
