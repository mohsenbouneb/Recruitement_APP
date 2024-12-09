import sqlite3
from tkinter import Tk, Label, Button, Entry, Frame, messagebox

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
            messagebox.showinfo("Login Successful", f"Welcome, {user_type} {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or user type.")

# Function to display login form
def show_login_form(user_type):
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text=f"{user_type} Login", font=("Arial", 24)).pack(pady=20)

    global username_entry, password_entry

    Label(root, text="Username:", font=("Arial", 14)).pack(pady=5)
    username_entry = Entry(root, font=("Arial", 14))
    username_entry.pack(pady=5)

    Label(root, text="Password:", font=("Arial", 14)).pack(pady=5)
    password_entry = Entry(root, show="*", font=("Arial", 14))
    password_entry.pack(pady=5)

    Button(root, text="Login", font=("Arial", 14), command=lambda: validate_login(user_type)).pack(pady=20)

    Button(root, text="Back", font=("Arial", 14), command=show_role_selection).pack(pady=10)

# Function to display role selection screen
def show_role_selection():
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Choose Your Role", font=("Arial", 24)).pack(pady=50)

    Button(root, text="Recruteur", font=("Arial", 18), command=lambda: show_login_form("Employeur"), width=15).pack(pady=20)
    Button(root, text="Candidat", font=("Arial", 18), command=lambda: show_login_form("Candidat"), width=15).pack(pady=20)

# Main window setup
root = Tk()
root.title("Login System")
root.geometry("1200x700")
root.resizable(False, False)

# Initialize with role selection screen
show_role_selection()

# Run the application
root.mainloop()
