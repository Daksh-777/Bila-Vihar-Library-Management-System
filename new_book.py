import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os 
import re
import sys

# Database setup
def create_database():
    with sqlite3.connect('book.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        conn.commit()
    print("Database initialized.")  # Debugging

# Function to validate ISBN-13 format (XXX-XXXXXXXXXX)
def is_valid_isbn(isbn):
    return bool(re.match(r"^\d{3}-\d{10}$", isbn))  # 3 digits + hyphen + 10 digits

# Function to validate year
def is_valid_year(year):
    return year.isdigit() and len(year) == 4 and 0 <= int(year) <= 2025

# Function to save book data
def save_book():
    isbn = entry_isbn.get().strip()
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    publisher = entry_publisher.get().strip()
    year = entry_year.get().strip()

    print("Save button clicked.")  # Debugging

    # Validate ISBN-13 format
    if not is_valid_isbn(isbn):
        messagebox.showwarning("Input Error", "ISBN-13 must be in format XXX-XXXXXXXXXX (3 digits - 10 digits).")
        print("Invalid ISBN-13 format.")  # Debugging
        return

    # Validate Year
    if not is_valid_year(year):
        messagebox.showwarning("Input Error", "Year must be a 4-digit number between 0000 and 2025.")
        print("Invalid Year format.")  # Debugging
        return

    # Ensure all fields are filled
    if not all([isbn, title, author, publisher, year]):
        messagebox.showwarning("Input Error", "All fields are mandatory!")
        print("Some fields are empty.")  # Debugging
        return

    try:
        with sqlite3.connect('book.db') as conn:
            cursor = conn.cursor()

            # Check if ISBN already exists
            cursor.execute("SELECT COUNT(*) FROM books WHERE isbn = ?", (isbn,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Input Error", "This ISBN-13 already exists.")
                print("Duplicate ISBN detected.")  # Debugging
                return

            # Insert data into database
            cursor.execute('''
                INSERT INTO books (isbn, title, author, publisher, year)
                VALUES (?, ?, ?, ?, ?)
            ''', (isbn, title, author, publisher, int(year)))
            conn.commit()

        print("Book added to database!")  # Debugging

        # Clear input fields
        for entry in [entry_isbn, entry_title, entry_author, entry_publisher, entry_year]:
            entry.delete(0, tk.END)

        messagebox.showinfo("Success", "New Book added successfully!")
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        messagebox.showerror("Database Error", f"An error occurred: {e}")

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
root.title("Add New Book")
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
    ("ISBN-13:", "entry_isbn"),
    ("Book Title:", "entry_title"),
    ("Author Name:", "entry_author"),
    ("Publisher:", "entry_publisher"),
    ("Publication Year:", "entry_year")
]

entries = {}

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(frame, text=label_text, fg="white", bg="#2E2E2E", font=font_bold).grid(row=i, column=0, padx=15, pady=10, sticky="e")
    entry = tk.Entry(frame, font=font_large, bg="white", fg="black", insertbackground="black", width=40)
    entry.grid(row=i, column=1, padx=15, pady=10, sticky="w")
    entries[var_name] = entry

entry_isbn = entries["entry_isbn"]
entry_title = entries["entry_title"]
entry_author = entries["entry_author"]
entry_publisher = entries["entry_publisher"]
entry_year = entries["entry_year"]

# Button frame
button_frame = tk.Frame(frame, bg="#2E2E2E")
button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

# Buttons
btn_save = tk.Button(button_frame, text="Save", command=save_book, font=font_bold, bg="black", fg="white", activebackground="#333333", width=15,
                      height=2)
btn_save.pack(side="left", padx=10)

btn_return = tk.Button(button_frame, text="Return", command=return_to_main, font=font_bold, bg="black", fg="white", activebackground="#333333", 
                       width=15, height=2)
btn_return.pack(side="left", padx=10)

# Initialize database
create_database()

# Run the application
root.mainloop()
