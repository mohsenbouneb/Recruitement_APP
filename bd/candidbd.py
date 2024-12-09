import sqlite3
import random

# Sample candidate data to insert into the database
candidates_data = [
    ("John Doe", 3, 2, 4, 3, 5),
    ("Jane Smith", 2, 1, 3, 2, 4),
    ("Alice Brown", 5, 3, 5, 4, 4),
    ("Bob Johnson", 1, 0, 2, 3, 3),
    ("Charlie Davis", 4, 2, 4, 4, 3),
    ("David Wilson", 3, 1, 3, 2, 4),
    ("Eve White", 2, 2, 4, 3, 3),
    ("Frank Harris", 3, 3, 4, 5, 4),
    ("Grace Martinez", 1, 0, 3, 2, 4),
    ("Helen Moore", 5, 4, 5, 4, 5),
    ("Isaac Taylor", 4, 3, 4, 3, 5),
    ("Jack Anderson", 2, 1, 3, 3, 2),
    ("Lily Thomas", 3, 2, 4, 5, 3),
    ("Mason Jackson", 4, 3, 5, 4, 5),
    ("Nina Lee", 1, 0, 2, 2, 3),
    ("Oliver King", 2, 1, 3, 3, 4),
    ("Paul Scott", 3, 3, 4, 4, 4),
    ("Quincy Harris", 4, 2, 5, 3, 3),
    ("Riley Young", 2, 2, 3, 4, 4),
    ("Sophie Turner", 3, 1, 5, 3, 5),
    ("Tina Brown", 4, 2, 4, 5, 4),
    ("Uma Davis", 5, 3, 4, 4, 5),
    ("Vera Green", 1, 0, 2, 3, 3),
    ("Wendy Walker", 2, 1, 3, 4, 4),
    ("Xander White", 3, 3, 5, 3, 4),
    ("Yara Black", 4, 2, 4, 4, 4),
    ("Zane Blue", 5, 4, 4, 5, 5),
    ("Anna Clark", 2, 1, 3, 2, 3),
    ("Bradley Hall", 3, 2, 4, 3, 5),
    ("Cora King", 1, 0, 2, 1, 2),
    ("Danielle Adams", 4, 3, 5, 5, 4),
    ("Elise Harris", 5, 2, 4, 5, 3),
    ("Freddy Lewis", 3, 1, 3, 2, 3),
    ("Gemma Wright", 2, 0, 3, 4, 5),
    ("Hannah Evans", 1, 1, 2, 2, 4),
    ("Ivy Scott", 5, 4, 5, 5, 5),
    ("James Lee", 4, 3, 4, 4, 4),
    ("Kara Mitchell", 3, 2, 3, 5, 4),
    ("Lena Carter", 2, 0, 3, 3, 4),
    ("Mila Reed", 1, 1, 2, 3, 2),
    ("Noah Perez", 4, 2, 5, 4, 5),
    ("Oscar Clark", 3, 1, 4, 4, 3),
    ("Penny Lewis", 2, 2, 3, 2, 3),
    ("Quinn Grant", 5, 4, 4, 3, 4),
    ("Ryan Nelson", 4, 3, 3, 5, 3),
    ("Sally Cooper", 3, 2, 4, 3, 4),
    ("Tessa Green", 2, 1, 4, 2, 4),
    ("Ursula Bennett", 1, 0, 2, 3, 3),
    ("Victor Price", 5, 4, 5, 4, 5),
    ("Willie Carter", 4, 2, 4, 4, 5),
    ("Xena Foster", 3, 1, 3, 2, 4),
]

# Function to calculate candidate score (you can modify the logic based on your criteria)
def calculate_score(experience, diplome, competences_techniques, qualites_humaines, mobilite):
    return experience + diplome + competences_techniques + qualites_humaines + mobilite

# Connect to the database and insert candidate data
with sqlite3.connect("recrutement.db") as conn:
    cursor = conn.cursor()

    # Insert 50 candidates with random job_id (associated with the available jobs in the jobs table)
    for i in range(50):
        candidate = random.choice(candidates_data)
        job_id = random.randint(1, 20)  # Assuming there are 20 jobs in the jobs table

        # Calculate the candidate's score
        score = calculate_score(candidate[1], candidate[2], candidate[3], candidate[4], candidate[5])

        # Insert the candidate data into the candidat table
        cursor.execute("""
            INSERT INTO candidat (job_id, experience, nom, diplome, competences_techniques, qualites_humaines, mobilite, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (job_id, candidate[1], candidate[0], candidate[2], candidate[3], candidate[4], candidate[5], score))

    # Commit the changes to the database
    conn.commit()

    print("50 candidates have been added to the database.")
