import sqlite3
conn = sqlite3.connect('health_compass.db', timeout=20)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        mail TEXT UNIQUE NOT NULL,
        location TEXT,
        password TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS health_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        health_parameters TEXT,
        result TEXT,
        type TEXT,  -- New column for storing the type of prediction
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

c.execute("PRAGMA table_info(health_data)")
columns = [column[1] for column in c.fetchall()]

if 'type' not in columns:
    c.execute('''
        ALTER TABLE health_data ADD COLUMN type TEXT
    ''')

conn.commit()
conn.close()
