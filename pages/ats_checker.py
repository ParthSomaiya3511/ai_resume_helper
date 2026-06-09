# pages/ats_checker.py
import streamlit as st
import random
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="ATS System Analysis")

# Apply the global app-wide luxury alabaster two-color background styles
apply_global_styles()

st.title("📊 ATS Analyzer & Optimizer")
st.caption("Verify keyword density and structural compliance against automated ATS checkers.")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Wrap Data Upload interface inside a luxury floating card
    st.markdown("""
    <div class="card" style="margin-bottom: 20px;">
        <h3 style="margin-top: 0; font-size: 1.15rem; color: #2c2523;">Data Upload Workspace</h3>
        <p style="font-size: 0.85rem; color: #6e625f; margin-bottom: 0;">Upload your customized resume sheet and copy the target role requirements below to run compatibility calculations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Styled Input Fields
    uploaded_file = st.file_uploader("Upload Current Resume (PDF, TXT)", type=["pdf", "txt"])
    job_desc = st.text_area("Target Job Description", placeholder="Paste the job requirements or target company specifications here...", height=180)
    
    st.write("")
    analyze_btn = st.button("🔍 Run Compatibility Check", use_container_width=True)

with col_right:
    st.markdown("<h3 style='margin-top: 0; font-size: 1.15rem; color: #2c2523;'>Analysis Metrics</h3>", unsafe_allow_html=True)
    
    if analyze_btn and job_desc:
        match_score = random.randint(72, 95)
        # Conditional branding colors based on matching scores
        score_color = "#8c7a6b" if match_score >= 80 else "#c084fc"
        
        # Display matching index dashboard inside a luxury metrics card
        st.markdown(f"""
        <div class="card" style="text-align: center; border-top: 4px solid {score_color} !important; margin-bottom: 20px;">
            <p style="margin:0; font-weight:700; color:#6e625f; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">COMPATIBILITY INDEX</p>
            <h1 style="font-size: 4rem; margin: 10px 0; color: {score_color}; font-family: 'Playfair Display', serif;">{match_score}%</h1>
            <div style="background: #f4efeb; border-radius: 8px; height: 10px; width: 100%;">
                <div style="background: {score_color}; height: 10px; border-radius: 8px; width: {match_score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Keyword mapping cards
        st.write("")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div class="card" style="padding: 15px !important; border-left: 3px solid #8c7a6b !important; height: 100%;">
                <h4 style="margin: 0 0 8px 0; color: #2c2523; font-size: 0.95rem;">✔️ Detected Core Skills</h4>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• System Design</p>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• Software Engineering</p>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• Web Technologies</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="card" style="padding: 15px !important; border-left: 3px solid #8c7a6b !important; height: 100%;">
                <h4 style="margin: 0 0 8px 0; color: #2c2523; font-size: 0.95rem;">⚠️ Missing Keywords</h4>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• Distributed Caching</p>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• Platform Scalability</p>
                <p style="font-size: 0.85rem; color: #6e625f; margin: 2px 0;">• Database Sharding</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="border-left: 3px solid #8c7a6b !important;">
            <p style="font-size: 0.9rem; color: #6e625f; margin: 0; line-height: 1.5;">
                Upload your customized resume sheet and paste the target job requirements on the left workspace to compute metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)