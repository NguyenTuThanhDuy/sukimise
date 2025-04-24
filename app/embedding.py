import logging
from abc import ABC, abstractmethod

from app.config import BaseConfig as Conf
from app.utils import preprocess_text_decorator
from langchain_openai.embeddings.base import OpenAIEmbeddings
from openai import OpenAIError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class IEmbeddingVector(ABC):

    @abstractmethod
    def create_embedding_vector(self, input_text: str):
        raise NotImplementedError()


class EmbeddingVector(IEmbeddingVector):

    def __init__(self) -> None:
        self.embed = OpenAIEmbeddings(
            api_key=Conf.OPENAI_API_KEY,
            model=Conf.OPENAI_EMBEDDING_MODEL,
            dimensions=Conf.OPENAI_EMBEDDING_DIMENSIONS,
        )

    @preprocess_text_decorator
    def create_embedding_vector(self, *, input_text: str):
        try:
            embedded_response = self.embed.embed_query(input_text)
            return embedded_response
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError("Error generating embedding vector from OpenAI.") from e
        except Exception as e:
            logger.error(f"Unexpected error while generating embedding: {e}")
            raise RuntimeError("An unexpected error occurred.") from e
