# pages/resume_history.py
import streamlit as st
import sqlite3
import os
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="History Portal")

# Apply the global app-wide luxury alabaster light theme
apply_global_styles()

st.title("Saved Configurations")
st.caption("Browse and review previous design configurations.")

# Connect to database securely
os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/resumes.db")
cursor = conn.cursor()

# Enforce active schema validations
try:
    cursor.execute("SELECT id, resume FROM history LIMIT 1")
except sqlite3.OperationalError:
    cursor.execute("DROP TABLE IF EXISTS history")
    cursor.execute("CREATE TABLE history(id INTEGER PRIMARY KEY AUTOINCREMENT, resume TEXT)")
    conn.commit()

cursor.execute("SELECT id, resume FROM history ORDER BY id DESC")
rows = cursor.fetchall()
conn.close()

if rows:
    # Render logs in custom cards
    for row in rows:
        st.markdown(f"""
        <div class="card" style="margin-bottom: 16px; border-left: 3px solid #8c7a6b !important;">
            <h4 style="margin: 0 0 6px 0; color: #2c2523;">📝 Configuration Record #{row[0]}</h4>
            <p style="margin: 0; color: #6e625f; font-size: 0.95rem; line-height: 1.4;">{row[1]}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No saved records detected. Save a configuration within the Resume Builder to record an entry.")