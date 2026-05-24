import streamlit as st
from utils.llama_api import ask_llama

st.set_page_config(layout="wide")

st.title("💼 AI Job Recommendations")

skills = st.text_area(
    "Enter Your Skills"
)

if st.button("Recommend Jobs"):

    prompt = f"""
    Based on these skills recommend:

    1. Best job roles
    2. Salary range
    3. Companies
    4. Career roadmap

    Skills:
    {skills}
    """

    result = ask_llama(prompt)

    st.write(result)