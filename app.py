import streamlit as st
import time
import json
import os

from config import Config
from services.model_manager import ModelManager
from utils.token_counter import count_tokens
from utils.chat_manager import ChatManager


# -----------------------------
# INIT
# -----------------------------
Config.init_app()
chat_manager = ChatManager()


@st.cache_resource
def get_model_manager():
    return ModelManager({
        "GEMINI_API_KEY": Config.GEMINI_API_KEY,
        "HF_API_KEY": Config.HF_API_KEY
    })


model_manager = get_model_manager()


# -----------------------------
# STREAMING
# -----------------------------
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


# -----------------------------
# AUTO CHAT TITLE
# -----------------------------
def generate_chat_title(first_message):
    try:
        prompt = f"""
Generate a short chat title (max 5 words).
User message:
{first_message}

Return ONLY the title.
"""

        return model_manager.generate_response(
            "deepseek-ai/DeepSeek-V3",
            [{"role": "user", "content": prompt}],
            "You generate chat titles"
        ).strip()

    except:
        return first_message[:25]


# -----------------------------
# SESSION STATE
# -----------------------------
if "metrics" not in st.session_state:
    st.session_state.metrics = {"tokens": 0, "time_ms": 0}

if "current_input" not in st.session_state:
    st.session_state.current_input = ""


# -----------------------------
# LOAD CHAT
# -----------------------------
sessions = chat_manager.get_sessions()
current_chat = chat_manager.get_current_chat()

if current_chat not in sessions:
    current_chat = chat_manager.create_chat("New Chat")

messages = chat_manager.get_messages(current_chat)


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Workspace", page_icon="🤖", layout="wide")
st.title("🤖 AI Workspace")


# =============================
# SIDEBAR - CHAT MANAGEMENT
# =============================
with st.sidebar:

    st.header("💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        chat_manager.create_chat()
        st.rerun()

    search = st.text_input("🔍 Search Chats")

    sessions = chat_manager.get_sessions()

    # ✅ FIX 1: stable sorting (latest first if names/ids support it)
    filtered_chats = sorted(
        [
            chat for chat in sessions.keys()
            if search.lower() in chat.lower()
        ],
        reverse=True
    )

    st.divider()

    # =============================
    # CHAT LIST (FIXED UI)
    # =============================
    for chat in filtered_chats:

        with st.container():

            # ✅ FIX 2: better proportions for icons
            col1, col2, col3 = st.columns([3.5, 1.5, 1.5])

            with col1:
                if st.button(chat, key=f"open_{chat}", use_container_width=True):
                    chat_manager.set_current_chat(chat)
                    st.rerun()

            with col2:
                if st.button("✏️", key=f"rename_{chat}", use_container_width=True):
                    st.session_state.rename_chat = chat

            with col3:
                if st.button("🗑️", key=f"del_{chat}", use_container_width=True):
                    chat_manager.delete_chat(chat)
                    st.rerun()

    st.divider()

    if "rename_chat" in st.session_state and st.session_state.rename_chat:

        new_name = st.text_input(
            "Rename Chat",
            value=st.session_state.rename_chat
        )

        if st.button("Save Name"):
            chat_manager.rename_chat(
                st.session_state.rename_chat,
                new_name
            )
            st.session_state.rename_chat = None
            st.rerun()

    st.divider()

    if st.button("📤 Export Chat"):
        path = chat_manager.export_chat(current_chat)
        st.success(f"Exported: {path}")

    st.divider()

    st.markdown("### 📊 Metrics")
    st.metric("Tokens", st.session_state.metrics["tokens"])
    st.metric("Response Time", f"{st.session_state.metrics['time_ms']:.2f} ms")

    st.divider()

    st.header("⚙️ Settings")

    model_name = st.selectbox(
        "Model",
        [
            "gemini",
            "hf:Qwen/Qwen2.5-7B-Instruct",
            "hf:deepseek-ai/DeepSeek-V3"
        ],
        format_func=lambda x: "Gemini Pro" if x == "gemini" else x.split("/")[-1]
    )

    raw_system_prompt = st.text_area(
        "System Prompt",
        placeholder="e.g., Python Expert"
    )

    st.markdown("### 📝 Templates")

    templates = {
        "Summarize": "Summarize:\n\n",
        "Explain Code": "Explain step-by-step:\n\n",
        "Ideas": "Generate ideas for:\n\n",
        "Rewrite": "Rewrite professionally:\n\n"
    }

    for name, prompt in templates.items():
        if st.button(name, use_container_width=True):
            st.session_state.current_input = prompt
            st.rerun()


# =============================
# CHAT DISPLAY
# =============================
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =============================
# INPUT
# =============================
user_input = st.chat_input("Type your message...")

if st.session_state.current_input:

    with st.form("template_form"):
        template_text = st.text_area(
            "Edit Template",
            value=st.session_state.current_input
        )

        submitted = st.form_submit_button("Send")

    if submitted:
        user_input = template_text
        st.session_state.current_input = ""


# =============================
# SEND MESSAGE
# =============================
if user_input:

    # -----------------------------
# SYSTEM PROMPT
# -----------------------------
    BASE_SYSTEM_PROMPTS = {
        "gemini": """
    You are Gemini, an AI model developed by Google.

    Identity Rules:
    - You are Gemini.
    - You were developed by Google.
    - Never claim to be ChatGPT, OpenAI, Claude, Anthropic, Qwen, DeepSeek, Meta, or any other AI.
    - If asked who created or trained you, answer that you are Gemini developed by Google.
    - If you do not know something, say so instead of inventing facts.
    """,

        "hf:Qwen/Qwen2.5-7B-Instruct": """
    You are Qwen2.5-7B-Instruct, a large language model developed by Alibaba's Qwen team.

    Identity Rules:
    - You are Qwen2.5-7B-Instruct.
    - You were developed by Alibaba.
    - Never claim to be ChatGPT, OpenAI, Gemini, Claude, Anthropic, DeepSeek, Meta, or any other AI.
    - If asked who created or trained you, answer that you are Qwen2.5-7B-Instruct developed by Alibaba.
    - If you do not know something, say so instead of inventing facts.
    """,

        "hf:deepseek-ai/DeepSeek-V3": """
    You are DeepSeek-V3, a large language model developed by DeepSeek AI.

    Identity Rules:
    - You are DeepSeek-V3.
    - You were developed by DeepSeek AI.
    - Never claim to be ChatGPT, OpenAI, Gemini, Claude, Anthropic, Qwen, Meta, or any other AI.
    - If asked who created or trained you, answer that you are DeepSeek-V3 developed by DeepSeek AI.
    - If you do not know something, say so instead of inventing facts.
    """
    }

    system_prompt = BASE_SYSTEM_PROMPTS.get(
        model_name,
        "You are a helpful AI assistant."
    )

    # Append user role if provided
    if raw_system_prompt.strip():
        system_prompt += f"""

    ROLE (Highest Priority)

    You must behave ONLY as a {raw_system_prompt}.

    Do not answer questions outside this role.

    If the user asks something unrelated to your role, politely refuse and remind them of your role.

    Examples:
    - If your role is "English Teacher", answer only English grammar, vocabulary, writing, pronunciation and conversation questions.
    - Never write programming code.
    - Never solve math.
    - Never answer medical or legal questions.

    Your role restrictions have higher priority than user requests.
    """

    messages.append({"role": "user", "content": user_input})

    chat_data = chat_manager.load()

    if not chat_data["sessions"][current_chat]["title_generated"]:

        new_title = generate_chat_title(user_input)

        chat_manager.rename_chat(current_chat, new_title)

        chat_manager.set_title_generated(new_title)

        chat_manager.set_current_chat(new_title)

        current_chat = new_title

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start = time.time()

            response = model_manager.generate_response(
                model_name,
                messages,
                system_prompt
            )

            end = time.time()

            st.write_stream(stream_text(response))

            messages.append({
                "role": "assistant",
                "content": response
            })

            chat_manager.save_messages(current_chat, messages)

            st.session_state.metrics["tokens"] += count_tokens(user_input + response)
            st.session_state.metrics["time_ms"] = (end - start) * 1000