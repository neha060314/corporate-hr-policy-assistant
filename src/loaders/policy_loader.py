import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from src.config.settings import Settings

class PolicyLoader:
    """
    Ingests PDF manuals and extracts clean structural LangChain Document records.
    """
    def __init__(self, directory_path: str = Settings.POLICIES_DIR):
        self.directory_path = directory_path

    def load_pdfs(self) -> List[Document]:
        documents = []
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)
            return documents

        for file in os.listdir(self.directory_path):
            if file.endswith(".pdf"):
                file_path = os.path.join(self.directory_path, file)
                try:
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"[LOADER ERROR] Failed to parse {file}: {str(e)}")
                    
        return documents