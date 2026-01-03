import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Database setup
def create_issue_database():
    with sqlite3.connect('issue.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT NOT NULL,
                student_id TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT NOT NULL
            )
        ''')
        conn.commit()

# Validate if ISBN exists in book.db
def is_valid_isbn(isbn):
    with sqlite3.connect('book.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE isbn = ?", (isbn,))
        return cursor.fetchone()[0] > 0  # Returns True if ISBN exists

# Validate if Student ID exists in students.db
def is_valid_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = ?", (student_id,))
        return cursor.fetchone()[0] > 0  # Returns True if Student ID exists

# Function to issue book
def issue_book():
    isbn = entry_isbn.get().strip()
    student_id = entry_student_id.get().strip()
    issue_date = entry_issue_date.get().strip()
    return_date = entry_return_date.get().strip()

    # Check if ISBN exists
    if not is_valid_isbn(isbn):
        messagebox.showerror("Error", "Invalid ISBN! This book does not exist in the database.")
        return

    # Check if Student ID exists
    if not is_valid_student(student_id):
        messagebox.showerror("Error", "Invalid Student ID! No such student found.")
        return

    # Check if return date is after issue date
    if return_date <= issue_date:
        messagebox.showerror("Error", "Return Date must be after Issue Date!")
        return

    # Save to database
    with sqlite3.connect('issue.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO issued_books (isbn, student_id, issue_date, return_date)
            VALUES (?, ?, ?, ?)
        ''', (isbn, student_id, issue_date, return_date))
        conn.commit()

    # Clear input fields
    entry_isbn.delete(0, tk.END)
    entry_student_id.delete(0, tk.END)
    entry_issue_date.delete(0, tk.END)
    entry_return_date.delete(0, tk.END)

    messagebox.showinfo("Success", "Book issued successfully!")

# Function to return to main menu
def return_to_main():
    root.destroy()
    main_script_path = resource_path("main.py")
    subprocess.run(["python", main_script_path], check=True)

# GUI setup
root = tk.Tk()
root.title("Issue a Book")
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
tk.Label(frame, text="ISBN-13:", fg="white", bg="#2E2E2E", font=font_bold).grid(row=0, column=0, padx=15, pady=10, sticky="e")
entry_isbn = tk.Entry(frame, font=font_large, width=40)
entry_isbn.grid(row=0, column=1, padx=15, pady=10, sticky="w")

tk.Label(frame, text="Student ID:", fg="white", bg="#2E2E2E", font=font_bold).grid(row=1, column=0, padx=15, pady=10, sticky="e")
entry_student_id = tk.Entry(frame, font=font_large, width=40)
entry_student_id.grid(row=1, column=1, padx=15, pady=10, sticky="w")

# Entry for Issue Date
tk.Label(frame, text="Issue Date (YYYY-MM-DD):", fg="white", bg="#2E2E2E", font=font_bold).grid(row=2, column=0, padx=15, pady=10, sticky="e")
entry_issue_date = tk.Entry(frame, font=font_large, width=40)
entry_issue_date.grid(row=2, column=1, padx=15, pady=10, sticky="w")

# Entry for Return Date
tk.Label(frame, text="Return Date (YYYY-MM-DD):", fg="white", bg="#2E2E2E", font=font_bold).grid(row=3, column=0, padx=15, pady=10, sticky="e")
entry_return_date = tk.Entry(frame, font=font_large, width=40)
entry_return_date.grid(row=3, column=1, padx=15, pady=10, sticky="w")

# Button frame
button_frame = tk.Frame(frame, bg="#2E2E2E")
button_frame.grid(row=4, column=0, columnspan=2, pady=20)

# Buttons
btn_save = tk.Button(button_frame, text="Issue Book", command=issue_book, font=font_bold, bg="black", fg="white", 
                     activebackground="#333333", width=15, height=2)
btn_save.pack(side="left", padx=10)

btn_return = tk.Button(button_frame, text="Return", command=return_to_main, font=font_bold, bg="black", fg="white", 
                       activebackground="#333333", width=15, height=2)
btn_return.pack(side="left", padx=10)

# Initialize database
create_issue_database()

# Run the application
root.mainloop()