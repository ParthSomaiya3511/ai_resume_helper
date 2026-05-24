import sqlite3

conn = sqlite3.connect("database/resumes.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume TEXT,
    result TEXT
)
""")

conn.commit()