import sqlite3

conn = sqlite3.connect("bd.db")
cursor = conn.cursor()


def get():
    cursor.execute("""SELECT Score FROM scores""")
    best = max(cursor.fetchall())
    return best
