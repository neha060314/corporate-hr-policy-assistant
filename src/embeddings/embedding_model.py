from langchain_huggingface import HuggingFaceEmbeddings
from src.config.settings import Settings

class EmbeddingModelFactory:
    """
    Instantiates local resource embedding generation abstractions.
    """
    @staticmethod
    def get_embedding_model() -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(
            model_name=Settings.EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'}
        )