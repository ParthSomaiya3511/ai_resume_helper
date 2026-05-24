import streamlit as st
from utils.llama_api import ask_llama

st.title("🤖 AI Career Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask AI about career...")

if user_input:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    response = ask_llama(user_input)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])