import sqlite3
from tkinter import Tk, Label, Button, Entry, Frame, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Function to add a new job on the same page
def clear_form_frame():
    # Remove all widgets from the form frame
    for widget in form_frame.winfo_children():
        widget.destroy()

def show_add_job_form():
    clear_form_frame()  # Clear the form frame

    Label(form_frame, text="Ajouter un emploi",font=("Arial", 18), bg="#2c2c2c", fg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    Label(form_frame, text="Type:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=1, column=0, pady=5, sticky="w")
    type_entry = Entry(form_frame)
    type_entry.grid(row=1, column=1, pady=5)

    Label(form_frame, text="Salaire:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=2, column=0, pady=5, sticky="w")
    salary_entry = Entry(form_frame)
    salary_entry.grid(row=2, column=1, pady=5)

    Label(form_frame, text="Lieu:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=3, column=0, pady=5, sticky="w")
    place_entry = Entry(form_frame)
    place_entry.grid(row=3, column=1, pady=5)

    Label(form_frame, text="Experience:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=4, column=0, pady=5, sticky="w")
    experience_entry = Entry(form_frame)
    experience_entry.grid(row=4, column=1, pady=5)


    def submit_job():
        job_type = type_entry.get()
        salary = salary_entry.get()
        place = place_entry.get()
        experience = experience_entry.get()

        if not (job_type and salary and place and experience):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            with sqlite3.connect("recrutement.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO jobs (type, salary, place, experience) VALUES (?, ?, ?, ?)",
                               (job_type, float(salary), place, int(experience)))
                conn.commit()
                messagebox.showinfo("Success", "Job added successfully.")
                show_all_jobs()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    submit_button = Button(form_frame, text="Ajouter",font=("Helvetica", 14), bg="#4caf50", fg="#ffffff", command=submit_job)
    submit_button.grid(row=5, columnspan=2, pady=10)

# Function to go back to login
def back_to_login():
    root.destroy()  # Close the main window
    os.system("python login.py")  # Launch the login window (assuming login.py is in the same directory)

# Function to delete a job
def delete_job():
    selected_item = jobs_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No job selected.")
        return

    job_id = jobs_tree.item(selected_item)['values'][0]

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        messagebox.showinfo("Success", "Job deleted successfully.")
        show_all_jobs()

# Function to modify a job (same page)
def modify_job():
    selected_item = jobs_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Aucun travail sélectionné.")
        return

    job_id = jobs_tree.item(selected_item)["values"][0]

    # Clear previous form
    for widget in form_frame.winfo_children():
        widget.destroy()

    Label(form_frame, text="Type:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=0, column=0, pady=5)
    type_entry = Entry(form_frame)
    type_entry.grid(row=0, column=1, pady=5)

    Label(form_frame, text="Salaire:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=1, column=0, pady=5)
    salary_entry = Entry(form_frame)
    salary_entry.grid(row=1, column=1, pady=5)

    Label(form_frame, text="Lieu:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=2, column=0, pady=5)
    place_entry = Entry(form_frame)
    place_entry.grid(row=2, column=1, pady=5)

    Label(form_frame, text="Experience:",font=("Helvetica", 14), bg="#2c2c2c", fg="#ffffff").grid(row=3, column=0, pady=5)
    experience_entry = Entry(form_frame)
    experience_entry.grid(row=3, column=1, pady=5)

    # Fetch current job details
    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT type, salary, place, experience FROM jobs WHERE id = ?", (job_id,))
        job = cursor.fetchone()

    type_entry.insert(0, job[0])
    salary_entry.insert(0, job[1])
    place_entry.insert(0, job[2])
    experience_entry.insert(0, job[3])

    def submit_changes():
        job_type = type_entry.get()
        salary = salary_entry.get()
        place = place_entry.get()
        experience = experience_entry.get()

        if not (job_type and salary and place and experience):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            with sqlite3.connect("recrutement.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE jobs SET type = ?, salary = ?, place = ?, experience = ? WHERE id = ?",
                               (job_type, float(salary), place, int(experience), job_id))
                conn.commit()
                messagebox.showinfo("Success", "Job modified successfully.")
                show_all_jobs()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    modify_button = Button(form_frame, text="Modifier",font=("Helvetica", 14), bg="#4caf50", fg="#ffffff", command=submit_changes)
    modify_button.grid(row=4, columnspan=2, pady=10)

# Function to show candidates for the selected job and their scores
def show_candidates_for_job():
    selected_item = jobs_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No job selected.")
        return

    job_id = jobs_tree.item(selected_item)['values'][0]

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nom, c.score 
            FROM candidat c 
            WHERE c.job_id = ? 
        """, (job_id,))
        candidates = cursor.fetchall()

    if not candidates:
        messagebox.showinfo("No Candidates", "No candidates have applied for this job.")
        return

    candidates_window = Tk()
    candidates_window.title("Candidates for the Job")

    candidates_tree = ttk.Treeview(candidates_window, columns=("Name", "Score"), show="headings")
    candidates_tree.heading("Name", text="Nom")
    candidates_tree.heading("Score", text="Score")
    candidates_tree.pack(pady=10)

    for candidate in candidates:
        candidates_tree.insert("", "end", values=candidate)

# Function to show a graph of candidates' scores for the selected job
def show_job_candidates_scores_graph():
    selected_item = jobs_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No job selected.")
        return

    job_id = jobs_tree.item(selected_item)['values'][0]

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nom, c.score 
            FROM candidat c 
            WHERE c.job_id = ? 
        """, (job_id,))
        data = cursor.fetchall()

    if not data:
        messagebox.showinfo("Aucun candidat", "Aucun candidat n'a postulé pour cet emploi.")
        return

    names = [row[0] for row in data]
    scores = [row[1] for row in data]

    fig, ax = plt.subplots()
    ax.bar(names, scores, color='skyblue')
    ax.set_xlabel("Candidatures")
    ax.set_ylabel("Notes")
    ax.set_title("Candidatures' Notes pour le poste")

    graph_window = Tk()
    graph_window.title("Candidatures' Notes pour le poste")

    canvas = FigureCanvasTkAgg(fig, graph_window)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Function to display all jobs
def show_all_jobs():
    for row in jobs_tree.get_children():
        jobs_tree.delete(row)

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        for job in cursor.fetchall():
            jobs_tree.insert("", "end", values=job)

# Main window setup
root = Tk()
root.title("Jobs Dashboard")
root.geometry("1200x750")
root.resizable(False, False)
root.configure(bg="#2c2c2c") 
Label(root, text="Tableau de Bord des Offres d'Emploi", font=("Arial", 24, "bold"), bg="#2c2c2c", fg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

frame = Frame(root)
frame.grid(row=0, column=0, columnspan=2, pady=10)
frame.configure(bg="#2c2c2c") 
button_frame = Frame(root)
button_frame.grid(row=3, column=0, sticky="nw", padx=10, pady=10)
button_frame.configure(bg="#2c2c2c")
# Shared form frame on the right
form_frame = Frame(root)
form_frame.grid(row=3, column=0, sticky="ne", padx=10, pady=10)
form_frame.configure(bg="#2c2c2c")

# Frame for jobs_tree
tree_frame = Frame(root, bg="#2c2c2c")  # Set the frame's background color
tree_frame.grid(row=2, column=0, columnspan=2, padx=100, pady=10)

# Create the Treeview widget
jobs_tree = ttk.Treeview(tree_frame, columns=("ID", "Type", "Salary", "Place", "Experience"), show="headings")

# Set column headings
jobs_tree.heading("ID", text="ID")
jobs_tree.heading("Type", text="Type")
jobs_tree.heading("Salary", text="Salaire")
jobs_tree.heading("Place", text="Lieu")
jobs_tree.heading("Experience", text="Expérience")
jobs_tree.column("Type", width=300)
jobs_tree.column("Salary", width=100)
# Create a style for Treeview
style = ttk.Style()
style.configure("Custom.Treeview", 
                background="#3c3c3c", 
                foreground="#ffffff", 
                fieldbackground="#3c3c3c", 
                font=("Helvetica", 12))  # Adjust font as needed

style.map("Custom.Treeview", background=[("selected", "#4caf50")])  # Selected row color

# Apply the style to the jobs_tree widget
jobs_tree.configure(style="Custom.Treeview")

# Add the Treeview to the frame
jobs_tree.pack(fill="both", expand=True)  # You can still use `pack()` inside this frame
# Create a frame to hold the buttons

# Add buttons to the frame, placed under each other
Button(button_frame, text="Ajouter un emploi", font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff", command=show_add_job_form, width=25).grid(row=0, column=0, pady=5)
Button(button_frame, text="Supprimer un emploi",font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff",  command=delete_job, width=25).grid(row=1, column=0, pady=5)
Button(button_frame, text="Modifier un emploi", font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff", command=modify_job, width=25).grid(row=2, column=0, pady=5)
Button(button_frame, text="Afficher tous les emplois", font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff", command=show_all_jobs, width=25).grid(row=3, column=0, pady=5)
Button(button_frame, text="Afficher les candidats", font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff", command=show_candidates_for_job, width=25).grid(row=4, column=0, pady=5)
Button(button_frame, text="Afficher le graphique ", font=("Helvetica", 14), bg="#0a1a57", fg="#ffffff",command=show_job_candidates_scores_graph, width=25).grid(row=5, column=0, pady=5)
Button(button_frame, text="Déconnexion",font=("Helvetica", 14), bg="#f44336", fg="#ffffff", command=back_to_login, width=25).grid(row=6, column=0, pady=5)


show_all_jobs()

root.mainloop()
