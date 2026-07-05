import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports", "chats")
    
    @staticmethod
    def init_app():
        os.makedirs(Config.EXPORT_DIR, exist_ok=True)