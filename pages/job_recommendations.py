# pages/job_recommendations.py
import streamlit as st
from utils.llama_api import ask_llama
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="AI Job Boards")

# Apply the global app-wide luxury alabaster light theme
apply_global_styles()

st.title("💼 Customized Recommendations")
st.caption("Discover targeted roles, salary guidelines, and organizational profiles matching your skills.")

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("""
    <div class="card" style="margin-bottom: 20px;">
        <h3 style="margin-top: 0; font-size: 1.15rem; color: #2c2523;">Your Technical Stack</h3>
        <p style="font-size: 0.85rem; color: #6e625f; margin-bottom: 15px;">Input your core tech stack below to discover high-matching market positions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    skills_input = st.text_area("List Core Skills (Comma-separated)", placeholder="Python, PostgreSQL, AWS Cloud, Docker, Git")
    
    st.write("")
    trigger = st.button("🚀 Recommend Target Opportunities", use_container_width=True)

with col_right:
    st.markdown("<h3 style='margin-top: 0; font-size: 1.15rem; color: #2c2523;'>Target Placements & Roadmaps</h3>", unsafe_allow_html=True)
    
    if trigger and skills_input:
        prompt = f"Recommend roles and salaries matching skills: {skills_input}."
        
        with st.spinner("Analyzing market directories..."):
            results_md = ask_llama(prompt)
            
        st.markdown(f"""
        <div class="card" style="border-left: 3px solid #8c7a6b !important;">
            {results_md}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Input your core skills stack on the left to load recommendations.")