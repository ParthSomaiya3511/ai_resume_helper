import streamlit as st
import sqlite3

st.set_page_config(layout="wide")

st.title("🕘 Resume History")

conn = sqlite3.connect(
    "database/resumes.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume TEXT
)
""")

conn.commit()

cursor.execute(
    "SELECT * FROM history"
)

rows = cursor.fetchall()

if rows:

    for row in rows:

        st.markdown(f"""
        <div class="card">

        <h3>Resume #{row[0]}</h3>

        <p>{row[1]}</p>

        </div>
        """, unsafe_allow_html=True)

else:

    st.info("No Resume History Found")