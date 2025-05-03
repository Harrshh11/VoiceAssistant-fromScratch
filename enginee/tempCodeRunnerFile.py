import sqlite3

# Connect to the database
con = sqlite3.connect("Sara.db")
cursor = con.cursor()

# Create sys_command table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL
)
""")

# Create web_command table
cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL
)
""")

# Insert sample data into sys_command
sys_commands = [
    ('notepad', 'notepad'),
    ('calculator', 'calc'),
    ('chrome', 'chrome')
]

cursor.executemany("INSERT INTO sys_command (name, path) VALUES (?, ?)", sys_commands)

# Insert sample data into web_command
web_commands = [
    ('youtube', 'https://www.youtube.com'),
    ('google', 'https://www.google.com'),
    ('github', 'https://www.github.com')
]

cursor.executemany("INSERT INTO web_command (name, url) VALUES (?, ?)", web_commands)

# Commit changes and close the connection
con.commit()
con.close()

print("Tables created and sample data inserted successfully!")
