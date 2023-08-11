import sqlite3


def init_db():
    with sqlite3.connect("appdata.db") as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            details TEXT NOT NULL
        )
        """)
        db.commit()

def add_entry(title, details):
    with sqlite3.connect("appdata.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO entries (title, details) VALUES (?, ?)", (title, details))
        db.commit()


def search_entries(query):
    with sqlite3.connect("appdata.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM entries WHERE title LIKE ?", ('%' + query + '%',))
        return cursor.fetchall()


init_db()  # Initialize the database when the module is imported
