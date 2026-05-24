import streamlit as st

from utils.pdf_generator import generate_resume_pdf

st.set_page_config(layout="wide")

st.title("🚀 AI Resume Builder")

col1, col2 = st.columns([1,1])

with col1:

    st.subheader("Resume Details")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone")

    skills = st.text_area("Skills")

    experience = st.text_area("Experience")

    education = st.text_area("Education")

    if st.button("Generate Professional Resume"):

        generate_resume_pdf(
            name,
            email,
            phone,
            skills,
            experience,
            education
        )

        st.success("Professional Resume Generated")

        with open("resume.pdf", "rb") as file:

            st.download_button(
                "⬇ Download Resume",
                file,
                file_name="Professional_Resume.pdf"
            )

with col2:

    st.subheader("Live Resume Preview")

    st.markdown(f"""
    <div class="card">

    <h1>{name}</h1>

    <p>{email}</p>

    <p>{phone}</p>

    <hr>

    <h3>Skills</h3>

    <p>{skills}</p>

    <h3>Experience</h3>

    <p>{experience}</p>

    <h3>Education</h3>

    <p>{education}</p>

    </div>
    """, unsafe_allow_html=True)