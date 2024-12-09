import sqlite3
from tkinter import Tk, Label, Button, Entry, Frame, messagebox, ttk
import os

# Function to show jobs based on filters (only name filter)
def show_filtered_jobs():
    filter_name = name_filter_entry.get()

    # Clear existing rows in the jobs list
    for row in jobs_tree.get_children():
        jobs_tree.delete(row)

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM jobs WHERE type LIKE ?"
        cursor.execute(query, ('%' + filter_name + '%',))
        jobs = cursor.fetchall()

        for job in jobs:
            jobs_tree.insert("", "end", values=job)

# Function to go back to the login page
def back_to_login():
    root.destroy()  # Close the main window
    os.system("python login.py")  # Launch the login window (assuming login.py is in the same directory)

# Function to apply for a job
def apply_for_job():
    selected_item = jobs_tree.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Aucun emploi sélectionné.")
        return

    job_id = jobs_tree.item(selected_item)['values'][0]

    # Collect candidate information
    experience = experience_entry.get()
    nom = nom_entry.get()
    diplome = diplome_entry.get()
    competences_techniques = competences_entry.get()
    qualites_humaines = qualites_entry.get()
    mobilite = mobilite_entry.get()

    # Check if all fields are filled
    if not (experience and nom and diplome and competences_techniques and qualites_humaines and mobilite):
        messagebox.showerror("Erreur", "Tous les champs sont requis.")
        return

    try:
        score = calculate_score(int(experience), int(diplome), int(competences_techniques), int(qualites_humaines), int(mobilite))

        # Insert the application into the database
        with sqlite3.connect("recrutement.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO candidat (job_id, experience, nom, diplome, competences_techniques, qualites_humaines, mobilite, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (job_id, int(experience), nom, int(diplome), int(competences_techniques), int(qualites_humaines), int(mobilite), score))
            conn.commit()
            messagebox.showinfo("Succès", "Vous avez postulé avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de la candidature : {e}")

# Function to calculate the score (you can adjust the formula based on your needs)
def calculate_score(experience, diplome, competences_techniques, qualites_humaines, mobilite):
    return experience + diplome + competences_techniques + qualites_humaines + mobilite

# Main window setup
root = Tk()
root.title("Tableau de bord du candidat")
root.geometry("1200x850")
root.configure(bg="#2c2c2c")  # Dark background

Label(root, text="Tableau de bord du candidat", font=("Helvetica", 24), bg="#2c2c2c", fg="#ffffff").pack(pady=10)

# Filter section (only name filter now)
filter_frame = Frame(root, bg="#2c2c2c")
filter_frame.pack(pady=10)

Label(filter_frame, text="Filtrer par nom d'emploi :", font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=0, column=0, padx=5)
name_filter_entry = Entry(filter_frame, font=("Helvetica", 14), bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
name_filter_entry.grid(row=0, column=1, padx=5)

filter_button = Button(filter_frame, text="Filtrer", font=("Helvetica", 14), bg="#4caf50", fg="#ffffff", command=show_filtered_jobs)
filter_button.grid(row=0, column=2, padx=10)

# Jobs list section
jobs_tree = ttk.Treeview(root, columns=("ID", "Type", "Salaire", "Lieu", "Expérience"), show="headings", style="Custom.Treeview")
jobs_tree.heading("ID", text="ID")
jobs_tree.heading("Type", text="Type")
jobs_tree.heading("Salaire", text="Salaire")
jobs_tree.heading("Lieu", text="Lieu")
jobs_tree.heading("Expérience", text="Expérience")
jobs_tree.pack(pady=20)

# Application form section
form_frame = Frame(root, bg="#2c2c2c")
form_frame.pack(pady=20)

form_labels = ["Expérience:", "Nom:", "Diplôme:", "Compétences techniques:", "Qualités humaines:", "Mobilité:"]
form_entries = []

for idx, text in enumerate(form_labels):
    Label(form_frame, text=text, font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=idx, column=0, padx=5, pady=5)
    entry = Entry(form_frame, font=("Helvetica", 14), bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
    entry.grid(row=idx, column=1, padx=5, pady=5)
    form_entries.append(entry)

experience_entry, nom_entry, diplome_entry, competences_entry, qualites_entry, mobilite_entry = form_entries

apply_button = Button(form_frame, text="Postuler", font=("Helvetica", 14), bg="#4caf50", fg="#ffffff", command=apply_for_job)
apply_button.grid(row=len(form_labels), columnspan=2, pady=10)

Button(root, text="Déconnexion", font=("Helvetica", 14), bg="#f44336", fg="#ffffff", command=back_to_login).pack(side="right", padx=10, pady=10)

# Style configuration for treeview
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Custom.Treeview", background="#3c3c3c", foreground="#ffffff", fieldbackground="#3c3c3c")
style.map("Custom.Treeview", background=[("selected", "#4caf50")])

# Show all jobs initially
show_filtered_jobs()

root.mainloop()
