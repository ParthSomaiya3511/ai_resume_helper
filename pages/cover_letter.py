# pages/cover_letter.py
import streamlit as st
from utils.llama_api import ask_llama
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="AI Cover Letter Workspace")

# Apply the global app-wide luxury alabaster light theme
apply_global_styles()

st.title("✉️ AI Cover Letter Workspace")
st.caption("Generate dynamic, tailored cover letters designed to align with corporate profiles.")

col_inputs, col_output = st.columns([1, 1.2], gap="large")

with col_inputs:
    st.markdown("""
    <div class="card" style="margin-bottom: 20px;">
        <h3 style="margin-top: 0; font-size: 1.15rem; color: #2c2523;">Target Opportunity</h3>
        <p style="font-size: 0.85rem; color: #6e625f; margin-bottom: 15px;">Specify your target role and enterprise coordinates to focus the AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form input fields
    job_role = st.text_input("Target Job Title", placeholder="Senior Platform Engineer")
    company = st.text_input("Company Name", placeholder="Acme Technologies Inc.")
    tone = st.selectbox("Narrative Tone", ["Professional & Confident", "Direct & Sincere", "Innovative & Energetic"])
    
    st.write("")
    gen_btn = st.button("⚡ Draft Cover Letter", use_container_width=True)

with col_output:
    st.markdown("<h3 style='margin-top: 0; font-size: 1.15rem; color: #2c2523;'>Formatted Draft Preview</h3>", unsafe_allow_html=True)
    
    if gen_btn and job_role and company:
        prompt = f"Draft a professional cover letter for a {job_role} position at {company}. Tone: {tone}."
        
        with st.spinner("Refining layout..."):
            letter_output = ask_llama(prompt)
            
        st.markdown(f"""
        <div class="card" style="font-family: 'Playfair Display', Georgia, serif; white-space: pre-wrap; color: #2c2523; line-height: 1.6; font-size: 1rem; border-left: 3px solid #8c7a6b !important;">
{letter_output}
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.download_button(
            label="⬇ Download Cover Letter (.txt)",
            data=letter_output,
            file_name=f"Cover_Letter_{company.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Input your target position details on the left and click 'Draft Cover Letter' to populate your preview workspace.")