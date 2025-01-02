# database.py
import sqlite3

DB_NAME = "vacation.db"

def create_database():
    """
    Create the SQLite database and table if they don't exist,
    and populate it with 10 users if empty.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            vacation_location TEXT NOT NULL
        )
    ''')
    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        # Insert 10 users
        users = [
            ("Alice", "Paris"),
            ("Bob", "New York"),
            ("Charlie", "London"),
            ("Diana", "Tokyo"),
            ("Eve", "Sydney"),
            ("Frank", "Berlin"),
            ("Grace", "Rome"),
            ("Hank", "Dubai"),
            ("Ivy", "Barcelona"),
            ("Jack", "Bangkok")
        ]
        cursor.executemany("INSERT INTO users (username, vacation_location) VALUES (?, ?)", users)
    conn.commit()
    conn.close()

def get_all_users():
    """Fetch all usernames from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_vacation_location(user_id):
    """Fetch the vacation location for a given user ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT vacation_location FROM users WHERE id = ?", (user_id,))
    location = cursor.fetchone()
    conn.close()
    return location[0] if location else None
