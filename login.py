import sqlite3
from tkinter import Tk, Label, Button, Entry, Frame, messagebox
import subprocess

# Function to handle login validation
def validate_login(user_type):
    username = username_entry.get()
    password = password_entry.get()

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND user_type = ?", 
                       (username, password, user_type))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Connexion réussie", f"Bienvenue, {user_type} {username}!")
            if user_type == "Employeur":
                subprocess.Popen(["python", "jobs_dash.py"])
            elif user_type == "Candidat":
                subprocess.Popen(["python", "candidat_dash.py"])
            root.destroy()
        else:
            messagebox.showerror("Échec de la connexion", "Identifiants ou type d'utilisateur incorrects.")

# Function to handle user registration
def handle_register(user_type):
    username = username_entry.get()
    password = password_entry.get()

    with sqlite3.connect("recrutement.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", 
                           (username, password, user_type))
            conn.commit()
            messagebox.showinfo("Inscription réussie", f"{user_type} {username} inscrit avec succès!")
            show_role_selection()
        except sqlite3.IntegrityError:
            messagebox.showerror("Échec de l'inscription", "Nom d'utilisateur déjà existant.")

# Function to display login/register form
def show_form(user_type):
    for widget in root.winfo_children():
        widget.destroy()

    Frame(root, bg="#2E2E2E", height=100).pack(fill="x")

    Label(root, text=f"{user_type} Connexion", font=("Helvetica", 24), bg="#2E2E2E", fg="white").pack(pady=20)

    global username_entry, password_entry

    Label(root, text="Nom d'utilisateur:", font=("Helvetica", 14), bg="#2E2E2E", fg="white").pack(pady=5)
    username_entry = Entry(root, font=("Helvetica", 14), bg="#6C757D", fg="white", insertbackground="white", relief="flat")
    username_entry.pack(pady=5, padx=20, ipadx=5, ipady=5)

    Label(root, text="Mot de passe:", font=("Helvetica", 14), bg="#2E2E2E", fg="white").pack(pady=5)
    password_entry = Entry(root, show="*", font=("Helvetica", 14), bg="#6C757D", fg="white", insertbackground="white", relief="flat")
    password_entry.pack(pady=5, padx=20, ipadx=5, ipady=5)

    Button(root, text="Connexion", font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat", command=lambda: validate_login(user_type)).pack(pady=20)
    
    Button(root, text="Inscription", font=("Helvetica", 14), bg="#007BFF", fg="white", relief="flat", command=lambda: handle_register(user_type)).pack(pady=10)
    Button(root, text="Retour", font=("Helvetica", 14), bg="#6C757D", fg="white", relief="flat", command=show_role_selection).pack(pady=10)

# Function to display role selection screen
def show_role_selection():
    for widget in root.winfo_children():
        widget.destroy()

    Frame(root, bg="#1E1E1E", height=100).pack(fill="x")

    Label(root, text="Choisissez votre rôle", font=("Helvetica", 24), bg="#1E1E1E", fg="white").pack(pady=50)

    Button(root, text="Recruteur", font=("Helvetica", 18), bg="#FFC107", fg="black", relief="flat", command=lambda: show_form("Employeur"), width=15).pack(pady=20)
    Button(root, text="Candidat", font=("Helvetica", 18), bg="#17A2B8", fg="white", relief="flat", command=lambda: show_form("Candidat"), width=15).pack(pady=20)

# Main window setup
root = Tk()
root.title("Système de Connexion")
root.geometry("1200x700")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

# Initialize with role selection screen
show_role_selection()

# Run the application
root.mainloop()