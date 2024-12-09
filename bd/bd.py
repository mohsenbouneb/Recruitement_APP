import sqlite3

# Connect to the database
conn = sqlite3.connect("recrutement.db")
cursor = conn.cursor()

# Create or update the `users` table with user types "Employeur" and "Candidat"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK(user_type IN ('Employeur', 'Candidat'))
    )
''')

# Create or update the `jobs` table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        salary REAL NOT NULL,
        place TEXT NOT NULL,
        experience INTEGER NOT NULL
    )
''')

# Create or update the `candidat` table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        experience INTEGER NOT NULL,
        nom TEXT NOT NULL,
        diplome INTEGER,
        competences_techniques INTEGER,
        qualites_humaines INTEGER,
        mobilite INTEGER,
        score INTEGER,
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()