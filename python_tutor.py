import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st 

load_dotenv()  # Load .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page settings
st.set_page_config(page_title="Python Tutor Chatbot", page_icon="🐍")
st.title("🐍 Python Tutor Chatbot")
st.write("Ask me anything about Python! (I won’t answer non-Python questions)")

# Keep chat history in session
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a senior Python tutor. "
                                      "Explain clearly with examples. "
                                      "Do not answer non-Python questions."}
    ]

# Display past messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Chat input box
user_input = st.chat_input("Type your Python question...")
if user_input:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content

    # Display chatbot reply
    st.chat_message("assistant").write(reply)

    # Save reply to history
    st.session_state["messages"].append({"role": "assistant", "content": reply})
