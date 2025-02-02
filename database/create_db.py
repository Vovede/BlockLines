import sqlite3

conn = sqlite3.connect('bd.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores 
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Score INTEGER)
""")

conn.commit()
