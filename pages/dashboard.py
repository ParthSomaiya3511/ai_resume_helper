import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Dashboard Analytics")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("ATS Score","92%")

with col2:
    st.metric("Resume Rank","Top 10%")

with col3:
    st.metric("Skill Match","88%")

with col4:
    st.metric("Job Matches","24")

df = pd.DataFrame({
    "Skills":["Python","SQL","AI","Communication"],
    "Score":[90,80,85,75]
})

fig = px.bar(
    df,
    x="Skills",
    y="Score",
    title="Skill Analytics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)