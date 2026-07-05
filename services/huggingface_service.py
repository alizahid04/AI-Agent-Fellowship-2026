import requests


class HuggingFaceService:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Hugging Face API key is required.")

        self.api_key = api_key.strip()
        self.base_url = "https://router.huggingface.co/v1/chat/completions"

    def generate(self, messages, system_prompt="", model_id="hf:Qwen/Qwen2.5-7B-Instruct"):

        model = model_id.replace("hf:", "")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        chat_messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        chat_messages.extend(messages)

        payload = {
            "model": model,
            "messages": chat_messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False,
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            if "choices" not in data:
                raise Exception(f"Unexpected response:\n{data}")

            return data["choices"][0]["message"]["content"].strip()

        except requests.exceptions.HTTPError:
            try:
                error = response.json()
            except Exception:
                error = response.text

            raise Exception(
                f"Hugging Face Error ({response.status_code}):\n{error}"
            )

        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Connection Error:\n{e}")

        except requests.exceptions.Timeout:
            raise Exception("Request timed out.")

        except Exception as e:
            raise Exception(f"Unexpected error:\n{e}")