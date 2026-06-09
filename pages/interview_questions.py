# pages/interview_questions.py
import streamlit as st
from utils.llama_api import ask_llama
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="AI Prep Portal")

# Apply the global app-wide luxury alabaster light theme
apply_global_styles()

st.title("🎤 AI Interview Simulator")
st.caption("Generate role-specific mock behavioral and systems questions designed to match FAANG and modern standards.")

col_setup, col_questions = st.columns([1, 1.4], gap="large")

with col_setup:
    st.markdown("""
    <div class="card" style="margin-bottom: 20px;">
        <h3 style="margin-top: 0; font-size: 1.15rem; color: #2c2523;">Simulator Settings</h3>
        <p style="font-size: 0.85rem; color: #6e625f; margin-bottom: 15px;">Configure the simulator parameters to match your targeted experience level.</p>
    </div>
    """, unsafe_allow_html=True)
    
    target_role = st.text_input("Target Position Title", placeholder="Software Engineer II", value="Python")
    complexity = st.select_slider("Interview Difficulty", ["Entry", "Mid-Level", "Senior/Staff"])
    
    st.write("")
    generate = st.button("⚡ Generate Simulation Setup", use_container_width=True)

with col_questions:
    st.markdown("<h3 style='margin-top: 0; font-size: 1.15rem; color: #2c2523;'>Active Question Board</h3>", unsafe_allow_html=True)
    
    if generate and target_role:
        prompt = f"Generate 3 systems and coding interview preparation questions for a {complexity} {target_role} developer role."
        
        with st.spinner("Synthesizing specialized rubrics..."):
            questions_md = ask_llama(prompt)
            st.session_state.active_questions = questions_md
            
    if "active_questions" in st.session_state:
        st.markdown(f"""
        <div class="card" style="border-top: 4px solid #8c7a6b !important;">
            {st.session_state.active_questions}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Input your target role and click 'Generate Simulation Setup' to load your personalized interview prep dashboard.")