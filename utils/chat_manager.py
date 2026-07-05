import json
import os
from datetime import datetime


CHAT_FILE = "chat_sessions.json"


class ChatManager:

    def __init__(self):
        self.file = CHAT_FILE

        if not os.path.exists(self.file):
            self.save({
                "current_chat": "New Chat",
                "sessions": {
                    "New Chat": {
                        "messages": [],
                        "title_generated": False,
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now())
                    }
                }
            })

    # -----------------------------
    # LOAD / SAVE
    # -----------------------------
    def load(self):
        try:
            with open(self.file, "r") as f:
                data = json.load(f)

            # MIGRATION (old format support)
            if "sessions" in data:
                for chat, value in data["sessions"].items():
                    if isinstance(value, list):
                        data["sessions"][chat] = {
                            "messages": value,
                            "title_generated": False,
                            "created_at": str(datetime.now()),
                            "updated_at": str(datetime.now())
                        }

            return data

        except:
            return {
                "current_chat": "New Chat",
                "sessions": {}
            }

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    # -----------------------------
    # CHAT OPERATIONS
    # -----------------------------
    def get_sessions(self):
        return self.load()["sessions"]

    def get_current_chat(self):
        return self.load()["current_chat"]

    def set_current_chat(self, chat_name):
        data = self.load()
        data["current_chat"] = chat_name
        self.save(data)

    def create_chat(self, name=None):

        data = self.load()

        if name is None:
            base = "New Chat"
            count = 1

            while f"{base} {count}" in data["sessions"]:
                count += 1

            name = f"{base} {count}"

        data["sessions"][name] = {
            "messages": [],
            "title_generated": False,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }

        data["current_chat"] = name

        self.save(data)

        return name

    def delete_chat(self, chat_name):

        data = self.load()

        if chat_name not in data["sessions"]:
            return

        del data["sessions"][chat_name]

        if len(data["sessions"]) == 0:
            self.save({
                "current_chat": "New Chat",
                "sessions": {
                    "New Chat": {
                        "messages": [],
                        "title_generated": False,
                        "created_at": str(datetime.now()),
                        "updated_at": str(datetime.now())
                    }
                }
            })
            return

        if data["current_chat"] == chat_name:
            data["current_chat"] = list(data["sessions"].keys())[0]

        self.save(data)

    def rename_chat(self, old_name, new_name):

        if old_name == new_name:
            return

        data = self.load()

        if new_name in data["sessions"]:
            return

        data["sessions"][new_name] = data["sessions"].pop(old_name)

        if data["current_chat"] == old_name:
            data["current_chat"] = new_name

        self.save(data)

    # -----------------------------
    # MESSAGE HANDLING
    # -----------------------------
    def get_messages(self, chat_name):

        data = self.load()

        chat = data["sessions"].get(chat_name, {})
        return chat.get("messages", [])

    def save_messages(self, chat_name, messages):

        data = self.load()

        if chat_name not in data["sessions"]:
            return

        data["sessions"][chat_name]["messages"] = messages
        data["sessions"][chat_name]["updated_at"] = str(datetime.now())

        self.save(data)

    # -----------------------------
    # TITLE FLAG
    # -----------------------------
    def is_title_generated(self, chat_name):

        data = self.load()

        return data["sessions"].get(chat_name, {}).get("title_generated", False)

    def set_title_generated(self, chat_name):

        data = self.load()

        if chat_name in data["sessions"]:
            data["sessions"][chat_name]["title_generated"] = True
            self.save(data)

    # -----------------------------
    # EXPORT
    # -----------------------------
    def export_chat(self, chat_name):

        os.makedirs("exports/chats", exist_ok=True)

        filename = f"exports/chats/{chat_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w") as f:
            json.dump(
                self.get_messages(chat_name),
                f,
                indent=4
            )

        return filename