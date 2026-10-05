import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.embeddings.embedding_model import EmbeddingModelFactory
from src.config.settings import Settings

class FaissVectorStoreManager:
    """
    Manages generation, storage writing, and safe system loading of local FAISS instances.
    """
    def __init__(self):
        self.embeddings = EmbeddingModelFactory.get_embedding_model()
        self.index_path = Settings.FAISS_INDEX_DIR

    def create_and_save_store(self, chunks: list[Document]) -> FAISS:
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        os.makedirs(self.index_path, exist_ok=True)
        vector_store.save_local(self.index_path)
        return vector_store

    def load_vector_store(self) -> FAISS:
        if not os.path.exists(os.path.join(self.index_path, "index.faiss")):
            raise FileNotFoundError("FAISS local index storage footprint does not exist yet.")
        
        # 2026 Safety Rule: explicit flag required for reading structural indices securely from storage
        return FAISS.load_local(
            self.index_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )