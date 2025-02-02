import sqlite3

conn = sqlite3.connect('bd.db')
cursor = conn.cursor()


class historyDB():
    def __init__(self):
        self.conn = sqlite3.connect('bd.db')
        self.cursor = self.conn.cursor()

    def add(self, data):
        self.cursor.execute("""
            INSERT INTO scores (Date, Score)
            VALUES (?, ?)
        """, (data["Date"], data["Score"]))
        self.conn.commit()

    def clear(self):
        self.cursor.execute("""DELETE FROM scores""")
        self.conn.commit()
