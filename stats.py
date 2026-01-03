import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview
import sqlite3
import subprocess
import os 
import sys

# Function to fetch and display issue details
def fetch_issue_details():
    try:
        # Connect to the issue.db for issued_books data
        with sqlite3.connect('issue.db') as conn_issue:
            cursor_issue = conn_issue.cursor()

            # SQL query to join the `issued_books` table
            query = '''
            SELECT student_id, isbn, issue_date, return_date
            FROM issued_books
            '''
            cursor_issue.execute(query)
            issue_data = cursor_issue.fetchall()

            # Check if data is fetched
            if not issue_data:
                messagebox.showinfo("No Data", "No issue records found!")
                return

            # Clear existing data in the table (if any)
            for row in table.get_children():
                table.delete(row)

            # Fetch additional student and book details
            for row in issue_data:
                student_id = row[0]
                isbn = row[1]
                issue_date = row[2]
                return_date = row[3]

                # Get student name from students.db
                with sqlite3.connect('students.db') as conn_students:
                    cursor_students = conn_students.cursor()
                    cursor_students.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
                    student_name_data = cursor_students.fetchone()
                    student_name = student_name_data[0] if student_name_data else "Unknown"

                # Get book title from books.db (using 'title' instead of 'book_title')
                with sqlite3.connect('book.db') as conn_books:
                    cursor_books = conn_books.cursor()
                    cursor_books.execute("SELECT title FROM books WHERE isbn = ?", (isbn,))
                    book_title_data = cursor_books.fetchone()
                    book_title = book_title_data[0] if book_title_data else "Unknown"

                # Insert the combined data into the table
                table.insert("", "end", values=(student_id, student_name, isbn, book_title, issue_date, return_date))

            # Change the button text to "Hide"
            btn_show.config(text="Hide", command=hide_issue_details)

    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Function to hide the issue details and reset the button
def hide_issue_details():
    # Remove all rows from the table
    for row in table.get_children():
        table.delete(row)

    # Change the button text back to "Show"
    btn_show.config(text="Show", command=fetch_issue_details)

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to return to main.py
def return_to_main():
    root.destroy()
    subprocess.run(["python", "main.py"], check=True)

# GUI setup
root = tk.Tk()
root.title("Issue Details")
root.geometry("800x600")  # Adjust window size
root.minsize(800, 600)
root.configure(bg="#2E2E2E")

# Font style
font_bold = ('Arial', 12, 'bold')

# Create a frame to center the content
frame = tk.Frame(root, bg="#2E2E2E")
frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)  # Full screen resizing

# Label
tk.Label(frame, text="Issue Details", fg="white", bg="#2E2E2E", font=('Arial', 18, 'bold')).grid(row=0, column=0, padx=10, pady=20, columnspan=2)

# Treeview (Table) to display the issue details
columns = ("Student ID", "Student Name", "ISBN", "Book Title", "Issue Date", "Return Date")
table = ttk.Treeview(frame, columns=columns, show="headings", height=12)  # Adjust row height

# Define columns headings
for col in columns:
    table.heading(col, text=col, anchor="center")
    table.column(col, anchor="center", width=120)  # Slightly narrower columns

# Add a vertical scrollbar to the table
scrollbar = tk.Scrollbar(frame, orient="vertical", command=table.yview)
scrollbar.grid(row=1, column=2, sticky="ns")
table.configure(yscrollcommand=scrollbar.set)

# Place the table in the frame
table.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Button to fetch and show data (or hide it)
btn_show = tk.Button(frame, text="Show", command=fetch_issue_details, font=font_bold, bg="black", fg="white", activebackground="#333333", width=15, height=2)
btn_show.grid(row=2, column=0, pady=(5, 5), padx=(10, 5), sticky="ew")

# Return button (placed on the right of the Show button)
btn_return = tk.Button(frame, text="Return", command=return_to_main, font=font_bold, bg="black", fg="white", activebackground="#333333", width=15,
                        height=2)
btn_return.grid(row=2, column=1, pady=(5, 5), padx=(5, 10), sticky="ew")

# Add some space below the buttons (reduced to 1/3 of the previous amount)
frame.grid_rowconfigure(3, weight=1)  # Empty row to add spacing

# Make the frame resizable in both directions
frame.grid_rowconfigure(1, weight=1)  # Make row 1 (table) resizable
frame.grid_columnconfigure(0, weight=1)  # Make column 0 (Show button) resizable
frame.grid_columnconfigure(1, weight=1)  # Make column 1 (Return button) resizable

# Run the application
root.mainloop()
