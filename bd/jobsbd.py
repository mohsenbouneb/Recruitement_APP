import sqlite3

# Connect to the database
with sqlite3.connect("recrutement.db") as conn:
    cursor = conn.cursor()

    # Sample jobs data to insert into the database
    jobs_data = [
        ("Software Engineer", 60000, "New York", 3),
        ("Data Scientist", 70000, "San Francisco", 2),
        ("Web Developer", 55000, "Los Angeles", 1),
        ("Product Manager", 80000, "Chicago", 4),
        ("UX/UI Designer", 65000, "Seattle", 2),
        ("Project Manager", 75000, "Boston", 5),
        ("DevOps Engineer", 72000, "Austin", 3),
        ("Database Administrator", 68000, "Dallas", 3),
        ("Front-End Developer", 60000, "San Francisco", 1),
        ("Back-End Developer", 65000, "Chicago", 2),
        ("Full Stack Developer", 70000, "Austin", 4),
        ("Mobile App Developer", 70000, "Los Angeles", 3),
        ("Network Engineer", 65000, "Miami", 4),
        ("Cybersecurity Analyst", 75000, "Seattle", 2),
        ("System Administrator", 60000, "New York", 3),
        ("Cloud Engineer", 72000, "Dallas", 3),
        ("QA Tester", 55000, "San Francisco", 1),
        ("Technical Support", 50000, "Chicago", 2),
        ("Business Analyst", 68000, "Los Angeles", 3),
        ("HR Manager", 75000, "Boston", 5)
    ]

    # Insert the jobs data into the jobs table
    cursor.executemany("""
        INSERT INTO jobs (type, salary, place, experience)
        VALUES (?, ?, ?, ?)
    """, jobs_data)

    # Commit the changes
    conn.commit()

    print("20 jobs have been added to the database.")
