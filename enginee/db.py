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

# Create contacts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE
)
""")

# Insert practical, day-to-day data into sys_command
sys_commands = [
    ('file_explorer', 'explorer'),
    ('task_manager', 'taskmgr'),
    ('settings', 'ms-settings:')
]
cursor.executemany("INSERT INTO sys_command (name, path) VALUES (?, ?)", sys_commands)

# Insert practical, day-to-day data into web_command
web_commands = [
    ('google', 'https://www.google.com'),
    ('gmail', 'https://mail.google.com'),
    ('maps', 'https://www.google.com/maps')
]
cursor.executemany("INSERT INTO web_command (name, url) VALUES (?, ?)", web_commands)

# Insert sample contacts
sample_contacts = [
    ('Archana Birla ', '9009472375'),
    ('Arzita Gupta', '8696189734')
]
cursor.executemany("INSERT OR IGNORE INTO contacts (name, phone_number) VALUES (?, ?)", sample_contacts)

# Commit changes and close the connection
con.commit()
con.close()

print("All tables created and sample data inserted successfully!")
