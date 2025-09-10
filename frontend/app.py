import streamlit as st
import requests

API_URL = "https://pythontutor.onrender.com"  # Update this when deployed

st.set_page_config(page_title="Python Tutor Chatbot", page_icon="🐍", layout="centered")
st.title("🐍 Python Tutor Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Helper: build history for backend
def build_history_for_backend():
    history = []
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            history.append(f"User: {msg['content']}")
        else:
            history.append(f"Tutor: {msg['content']}")
    return history

# Chat input
if prompt := st.chat_input("Ask me a Python question..."):
    # Show user message immediately
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to FastAPI
    history_payload = build_history_for_backend()
    payload = {"query": prompt, "history": history_payload}

    try:
        resp = requests.post(API_URL, json=payload)
        if resp.status_code == 200:
            answer = resp.json().get("answer", "⚠️ No response from tutor.")
        else:
            answer = f"⚠️ Error {resp.status_code}: {resp.text}"
    except Exception as e:
        answer = f"⚠️ Connection error: {str(e)}"

    # Show tutor response
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
