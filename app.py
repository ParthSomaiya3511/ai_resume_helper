import streamlit as st
from utils.gemini_api import ask_gemini
from utils.llama_api import ask_llama
from utils.resume_parser import extract_text
from utils.ai_engine import ask_ai

# Page Config

st.set_page_config(
    page_title="AI Resume Helper",
    layout="wide"
)

# Load CSS

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title

st.title("🚀 AI Resume Helper")

# Upload Resume

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.success("Resume Uploaded Successfully")

    option = st.selectbox(
        "Choose AI Feature",
        [
            "Resume Summary",
            "ATS Checker",
            "Skill Suggestions",
            "Job Match",
            "Improve Resume"
        ]
    )

    if st.button("Generate AI Response"):

        with st.spinner("AI is analyzing resume..."):

            if option == "Resume Summary":

                prompt = f"""
                Analyze this resume and create a professional summary:

                {resume_text}
                """

                result = ask_ai(prompt)

            elif option == "ATS Checker":

                prompt = f"""
                Check ATS score of this resume
                and provide improvements:

                {resume_text}
                """

                result = ask_llama(prompt)

            elif option == "Skill Suggestions":

                prompt = f"""
                Suggest missing skills for this resume:

                {resume_text}
                """

                result = ask_ai(prompt)

            elif option == "Job Match":

                job_desc = st.text_area("Paste Job Description")

                prompt = f"""
                Compare resume with job description.

                Resume:
                {resume_text}

                Job:
                {job_desc}
                """

                result = ask_llama(prompt)

            elif option == "Improve Resume":

                prompt = f"""
                Improve this resume professionally:

                {resume_text}
                """

                result = ask_ai(prompt)

            st.markdown("## 🤖 AI Result")

            st.write(result)