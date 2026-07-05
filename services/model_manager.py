from services.gemini_service import GeminiService
from services.huggingface_service import HuggingFaceService


class ModelManager:
    def __init__(self, keys):
        self.gemini = GeminiService(keys["GEMINI_API_KEY"])
        self.huggingface = HuggingFaceService(keys["HF_API_KEY"])

    def generate_response(self, model_name, messages, system_prompt):

        if model_name == "gemini":
            return self.gemini.generate(
                messages,
                system_prompt
            )

        elif model_name.startswith("hf:"):
            return self.huggingface.generate(
                messages,
                system_prompt,
                model_name
            )

        else:
            raise ValueError(f"Unsupported model: {model_name}")