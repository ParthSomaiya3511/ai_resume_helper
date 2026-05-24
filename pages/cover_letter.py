import streamlit as st
from utils.llama_api import ask_llama

st.set_page_config(layout="wide")

st.title("✉️ AI Cover Letter")

try:

    job_role = st.text_input("Job Role")

    company = st.text_input("Company Name")

    if st.button("Generate Cover Letter"):

        prompt = f"""
        Write professional cover letter for:

        Job Role: {job_role}
        Company: {company}
        """

        result = ask_llama(prompt)

        st.write(result)

except Exception as e:

    st.error(e)