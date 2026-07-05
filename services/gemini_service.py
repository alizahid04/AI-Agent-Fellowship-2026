import google.generativeai as genai


class GeminiService:
    def __init__(self, api_key):
        self.api_key = api_key

        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate(self, messages, system_prompt):

        if not self.api_key:
            raise Exception("Gemini API key is invalid or missing.")

        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=system_prompt,
        )

        history = []

        for msg in messages[:-1]:

            if msg["role"] == "user":
                role = "user"
            else:
                role = "model"

            history.append({
                "role": role,
                "parts": [msg["content"]]
            })

        chat = model.start_chat(history=history)

        response = chat.send_message(
            messages[-1]["content"]
        )

        return response.text