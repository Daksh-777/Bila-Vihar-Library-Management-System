import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import os 

# Database Function to check if the book is issued
def is_book_issued(isbn, student_id):
    with sqlite3.connect('issue.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM issued_books WHERE isbn = ? AND student_id = ?", (isbn, student_id))
        return cursor.fetchone()  # Returns None if not found

# Function to delete the book record from the issued_books table
def delete_book_record(isbn, student_id):
    with sqlite3.connect('issue.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM issued_books WHERE isbn = ? AND student_id = ?", (isbn, student_id))
        conn.commit()

# Save the record and delete from the issue.db
def save_return():
    isbn = entry_isbn.get().strip()
    student_id = entry_student_id.get().strip()
    return_date = entry_return_date.get().strip()

    # Check if all fields are filled
    if not isbn or not student_id or not return_date:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    # Check if the ISBN and Student ID exist in issued_books
    issued_book = is_book_issued(isbn, student_id)
    if not issued_book:
        messagebox.showerror("Error", "No record found for this student and ISBN!")
        return

    # Delete book record from issue.db
    delete_book_record(isbn, student_id)

    # Clear the fields
    entry_isbn.delete(0, tk.END)
    entry_student_id.delete(0, tk.END)
    entry_return_date.delete(0, tk.END)

    messagebox.showinfo("Success", "Book returned and record saved successfully!")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to return to the main menu
def return_to_main():
    root.destroy()
    subprocess.run(["python", "main.py"], check=True)

# GUI setup
root = tk.Tk()
root.title("Return a Book")
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

tk.Label(frame, text="Return Date (YYYY-MM-DD):", fg="white", bg="#2E2E2E", font=font_bold).grid(row=2, column=0, padx=15, pady=10, sticky="e")
entry_return_date = tk.Entry(frame, font=font_large, width=40)
entry_return_date.grid(row=2, column=1, padx=15, pady=10, sticky="w")

# Button frame
button_frame = tk.Frame(frame, bg="#2E2E2E")
button_frame.grid(row=3, column=0, columnspan=2, pady=20)

# Buttons
btn_save = tk.Button(button_frame, text="Save", command=save_return, font=font_bold, bg="black", fg="white", activebackground="#333333", width=15,
                      height=2)
btn_save.pack(side="left", padx=10)

btn_back = tk.Button(button_frame, text="Return", command=return_to_main, font=font_bold, bg="black", fg="white", activebackground="#333333", 
                     width=15, height=2)
btn_back.pack(side="left", padx=10)

# Run the application
root.mainloop()
