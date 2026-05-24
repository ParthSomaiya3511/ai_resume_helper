import streamlit as st
from utils.pdf_generator import generate_resume_pdf
import os

st.set_page_config(layout="wide")

# Load CSS

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("🚀 AI Resume Builder")

# Layout

left,right = st.columns([1,1.2])

# ================= LEFT PANEL =================

with left:

    st.subheader("Resume Editor")

    # Template

    template = st.selectbox(
        "Choose Resume Template",
        [
            "Modern Blue",
            "Dark Professional",
            "Minimal White"
        ]
    )

    # Theme Color

    theme = st.color_picker(
        "Choose Theme Color",
        "#2563eb"
    )

    # Profile Upload

    profile = st.file_uploader(
        "Upload Profile Image",
        type=["png","jpg","jpeg"]
    )

    # Form

    name = st.text_input("Full Name")

    role = st.text_input("Professional Role")

    email = st.text_input("Email")

    phone = st.text_input("Phone")

    summary = st.text_area("Professional Summary")

    skills = st.text_area("Skills")

    experience = st.text_area("Experience")

    education = st.text_area("Education")

    certifications = st.text_area("Certifications")

    # Drag & Drop Sections

    sections = st.multiselect(
        "Choose Resume Sections",
        [
            "Summary",
            "Skills",
            "Experience",
            "Education",
            "Certifications"
        ],
        default=[
            "Summary",
            "Skills",
            "Experience"
        ]
    )

    # Generate PDF

    if st.button("Generate Professional Resume"):

        generate_resume_pdf(
            name,
            role,
            email,
            phone,
            summary,
            skills,
            experience,
            education,
            certifications,
            theme
        )

        st.success("Resume Generated Successfully")

        with open("resume.pdf","rb") as file:

            st.download_button(
                "⬇ Download Resume PDF",
                file,
                file_name="AI_Resume.pdf"
            )

# ================= RIGHT PANEL =================

with right:

    st.subheader("Live Resume Preview")

    # Profile Image

    if profile:

        image_path = "uploads/profile.png"

        with open(image_path,"wb") as f:
            f.write(profile.read())

        profile_url = image_path

    else:

        profile_url = "assets/default_profile.png"

    # Resume Preview

    st.markdown(f"""
    <div class="resume-preview">

        <div class="resume-container">

            <!-- Sidebar -->

            <div class="resume-sidebar"
                 style="background:{theme};">

                <img src="{profile_url}"
                     class="profile-img">

                <h2>{name}</h2>

                <p>{role}</p>

                <hr>

                <h3>Contact</h3>

                <p>📧 {email}</p>

                <p>📱 {phone}</p>

                <h3>Skills</h3>

                <p>{skills}</p>

            </div>

            <!-- Main -->

            <div class="resume-main">

                {"<h2 class='section-title'>Summary</h2><p>"+summary+"</p>" if "Summary" in sections else ""}

                {"<h2 class='section-title'>Experience</h2><p>"+experience+"</p>" if "Experience" in sections else ""}

                {"<h2 class='section-title'>Education</h2><p>"+education+"</p>" if "Education" in sections else ""}

                {"<h2 class='section-title'>Certifications</h2><p>"+certifications+"</p>" if "Certifications" in sections else ""}

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)