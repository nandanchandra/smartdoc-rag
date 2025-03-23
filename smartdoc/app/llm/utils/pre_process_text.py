from typing import List

from app.settings import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger


class TextSplitter:

    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        if not text:
            logger.error("Empty text provided for splitting.")
            return []

        return self.splitter.split_text(text)


text_splitter = TextSplitter()
