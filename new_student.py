import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os 
import re
import logging  # Import the logging module
import sys

# Set up logging configuration
logging.basicConfig(filename='student_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Database setup
def create_database():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                father_name TEXT NOT NULL,
                home_address TEXT NOT NULL,
                school TEXT NOT NULL
            )
        ''')
        conn.commit()

# Function to validate full name
def is_valid_name(name):
    return bool(re.match(r"^[A-Za-z]+\s[A-Za-z]+$", name))  # Ensures at least two words (First & Last)

# Function to save student data
def save_student():
    student_id = entry_student_id.get().strip()
    name = entry_name.get().strip()
    father_name = entry_father_name.get().strip()
    home_address = entry_home_address.get().strip()
    school = entry_school.get().strip()

    # Validate Student ID (4-digit number)
    if not student_id.isdigit() or len(student_id) != 4:
        messagebox.showwarning("Input Error", "Student ID must be exactly 4 digits.")
        return

    # Validate names (must be full names)
    if not is_valid_name(name):
        messagebox.showwarning("Input Error", "Student Name must include first and last name.")
        return
    if not is_valid_name(father_name):
        messagebox.showwarning("Input Error", "Father's Name must include first and last name.")
        return

    # Ensure all fields are filled
    if not all([student_id, name, father_name, home_address, school]):
        messagebox.showwarning("Input Error", "All fields are mandatory!")
        return

    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        
        # Check for duplicate student ID
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = ?", (student_id,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Input Error", "This Student ID already exists.")
            return

        # Insert data into database
        cursor.execute(''' 
            INSERT INTO students (student_id, name, father_name, home_address, school)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, name, father_name, home_address, school))
        conn.commit()

    # Log the student added to a file
    logging.info(f"Student Added: {student_id} - {name}")

    # Clear input fields
    for entry in [entry_student_id, entry_name, entry_father_name, entry_home_address, entry_school]:
        entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Student added successfully!")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to return to main menu
def return_to_main():
    root.destroy()
    subprocess.run(["python", "main.py"], check=True)

# GUI setup
root = tk.Tk()
root.title("Add New Student")
root.geometry("900x600")
root.minsize(900, 600)
root.configure(bg="#2E2E2E")

# Font styles
font_bold = ('Arial', 14, 'bold')
font_large = ('Arial', 16)

# Create a frame to center content
frame = tk.Frame(root, bg="#2E2E2E")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Labels and Entry fields
fields = [
    ("Student ID:", "entry_student_id"),
    ("Name:", "entry_name"),
    ("Father's Name:", "entry_father_name"),
    ("Home Address:", "entry_home_address"),
    ("School:", "entry_school")
]

entries = {}

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(frame, text=label_text, fg="white", bg="#2E2E2E", font=font_bold).grid(row=i, column=0, padx=15, pady=10, sticky="e")
    entry = tk.Entry(frame, font=font_large, bg="white", fg="black", insertbackground="black", width=40)
    entry.grid(row=i, column=1, padx=15, pady=10, sticky="w")
    entries[var_name] = entry

entry_student_id = entries["entry_student_id"]
entry_name = entries["entry_name"]
entry_father_name = entries["entry_father_name"]
entry_home_address = entries["entry_home_address"]
entry_school = entries["entry_school"]

# Button frame
button_frame = tk.Frame(frame, bg="#2E2E2E")
button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

# Buttons
btn_save = tk.Button(button_frame, text="Save", command=save_student, font=font_bold, bg="black", fg="white", activebackground="#333333",
                      width=15, height=2)
btn_save.pack(side="left", padx=10)

btn_return = tk.Button(button_frame, text="Return", command=return_to_main, font=font_bold, bg="black", fg="white", activebackground
                       ="#333333", width=15, height=2)
btn_return.pack(side="left", padx=10)

# Initialize database
create_database()

# Run the application
root.mainloop()
