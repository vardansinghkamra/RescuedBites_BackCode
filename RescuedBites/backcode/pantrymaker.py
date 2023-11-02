import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db', check_same_thread=False)
cur = conn.cursor()

# Create the pantry table
cur.execute('''CREATE TABLE IF NOT EXISTS pantry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        ingredients TEXT,
        FOREIGN KEY (username) REFERENCES users(username)
    )''')

# Commit the changes and close the connection
conn.commit()
conn.close()