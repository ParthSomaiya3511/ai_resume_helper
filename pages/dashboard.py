# pages/dashboard.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="Performance Analytics Portal")

# Apply the global app-wide luxury alabaster two-color background styles
apply_global_styles()

st.title("📊 Performance Analytics")
st.caption("Track matching diagnostics, profile completions, and active search metrics.")

# --- HIGH-END CUSTOM KPI CONTAINERS ---
col1, col2, col3, col4 = st.columns(4)

metrics_data = [
    ("ATS Average", "92%", "📈 +4.1% Progress"),
    ("Resume Quality", "Top 3%", "🔥 Luxury Grade"),
    ("Skill Alignment", "95%", "🎯 Optimal Match"),
    ("Applications Tracking", "34 Roles", "💼 Active Search")
]

# Map each KPI into a beautifully styled, custom HTML card container
for col, (title, value, status) in zip([col1, col2, col3, col4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="card" style="padding: 20px !important; border-left: 3px solid #8c7a6b !important; height: 100%;">
            <p style="margin: 0; font-size: 0.8rem; font-weight: 700; color: #6e625f; text-transform: uppercase; letter-spacing: 0.5px;">
                {title}
            </p>
            <h2 style="margin: 8px 0; font-size: 2.2rem; color: #2c2523; font-family: 'Playfair Display', serif; font-weight: 600;">
                {value}
            </h2>
            <span style="color: #8c7a6b; font-size: 0.85rem; font-weight: 600;">
                {status}
            </span>
        </div>
        """, unsafe_allow_html=True)

st.write("")
st.write("")

# --- DIAGNOSTIC VISUALIZATION ---
st.markdown("<h3>Diagnostic Visualization</h3>", unsafe_allow_html=True)

df = pd.DataFrame({
    "Technology Focus": ["Web Design", "PHP Engine", "WordPress CMS", "Laravel MVC", "SEO Tools"],
    "Competency Score": [95, 88, 92, 84, 90]
})

# Plotly styling with warm tones
fig = px.bar(
    df,
    x="Technology Focus",
    y="Competency Score",
    color="Competency Score",
    color_continuous_scale=["#e6dfd9", "#8c7a6b"], # Transitioning from Sand Clay to Luxury Taupe
    title="Core Technology Alignment Score"
)

# Set high-end background transparent adjustments
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#2c2523",
    font_family="Plus Jakarta Sans",
    title_font_family="Playfair Display",
    title_font_size=16
)

# Thin, elegant gridline adjustments
fig.update_yaxes(gridcolor="rgba(230, 223, 217, 0.4)")

st.plotly_chart(fig, use_container_width=True)