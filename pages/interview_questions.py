import streamlit as st
from utils.llama_api import ask_llama

st.set_page_config(layout="wide")

st.title("🎤 AI Interview Preparation")

role = st.text_input(
    "Enter Job Role"
)

if st.button("Generate Interview Q&A"):

    prompt = f"""
    Generate professional interview preparation for {role}.

    For every question provide:

    1. Interview Question
    2. Professional Answer
    3. Tips
    4. Difficulty Level

    Generate:
    - HR Questions
    - Technical Questions
    - Behavioral Questions
    """

    result = ask_llama(prompt)

    st.write(result)