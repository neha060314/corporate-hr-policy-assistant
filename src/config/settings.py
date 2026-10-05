import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Centralized 2026 configuration management. Asserting requirements early 
    to ensure production safety.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Updated to Gemini 3.1 Flash Lite - the 2026 baseline performance standard
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.1-flash-lite")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    POLICIES_DIR = os.path.join(BASE_DIR, "policies")
    FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

    @classmethod
    def validate_config(cls):
        if not cls.GOOGLE_API_KEY:
            raise ValueError("CRITICAL ERROR: GOOGLE_API_KEY is missing from environment layout.")

Settings.validate_config()