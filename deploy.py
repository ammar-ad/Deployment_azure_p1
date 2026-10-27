import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
API_KEY = os.getenv("API_KEY")
DEPLOYMENT = os.getenv("AZURE_AI_DEPLOYMENT")

if not ENDPOINT or not API_KEY or not DEPLOYMENT:
    st.error("Set all three Azure environment variables first.")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url=ENDPOINT.rstrip("/") + "/")

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful chatbot. Answer simply and clearly.And when asked introduce yourself as Ammar personal assisstant and dont say OPenAi say you were build and created by Ammar."}
    ]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

user_input = st.chat_input("Type here")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    except Exception as e:
        st.session_state.messages.pop()
        st.error(str(e))