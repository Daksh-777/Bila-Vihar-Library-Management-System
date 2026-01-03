import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

# Function to show tooltips
def show_tooltip(event, text):
    tooltip_label.config(text=text)
    tooltip_label.place(x=event.x_root - root.winfo_rootx(), y=40)

# Function to hide tooltips
def hide_tooltip(event):
    tooltip_label.place_forget()

# Function to close the app
def close_app():
    root.destroy()

# Function to open a new window with the content of a Python file
def open_file_window(file_path):
    root.destroy()
    new_window = tk.Tk()
    new_window.title(file_path)
    new_window.geometry("900x600")
    new_window.configure(bg="#424242")
    with open(file_path, 'r') as file:
        content = file.read()
    text_widget = tk.Text(new_window, wrap='word', bg="white", fg="black")
    text_widget.insert('1.0', content)
    text_widget.pack(expand=True, fill='both')
    new_window.mainloop()

# Function to execute a Python file
def execute_file(file_path):
    root.destroy()
    os.system(f'python {file_path}')

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Main Window
root = tk.Tk()
root.title("Library Management System")
root.geometry("900x600")
root.configure(bg="#424242")  # Change background color to dark grey

# Bind Escape key to close the app
root.bind("<Escape>", lambda event: close_app())

# Navigation Bar
nav_frame = tk.Frame(root, bg="white", height=60, relief="raised", bd=2)  # Change background color to white and add border
nav_frame.pack(fill="x", pady=10)

# Heading Text
heading_frame = tk.Frame(root, bg="#424242")
heading_frame.pack(pady=10)

welcome_label = tk.Label(heading_frame, text="WELCOME TO THE", font=("Arial", 16, "bold"), fg="white", bg="#424242")
welcome_label.pack()

heading_label = tk.Label(heading_frame, text="BALA VIHAR LIBRARY MANAGEMENT SYSTEM", font=("Arial", 24, "bold"), fg="white", bg="#424242")
heading_label.pack()

# Tooltip Label
tooltip_label = tk.Label(root, bg="#424242", fg="white", font=("Arial", 10), padx=5, pady=2)  # Change background color to dark grey

# Function to resize icons and adjust spacing
def resize_icons(event):
    width = nav_frame.winfo_width()
    num_icons = len(icons)
    icon_size = 75 if width >= 900 else 50
    spacing = (width - (icon_size * num_icons)) // (num_icons + 1)
    for i, btn in enumerate(nav_frame.winfo_children()):
        btn.config(width=icon_size, height=icon_size)
        btn.grid_configure(padx=spacing // 2)

# Function to resize elements when window is minimized
def resize_elements(event):
    if root.attributes('-fullscreen'):
        welcome_label.config(font=("Arial", 20, "bold"))  # H1 size
        heading_label.config(font=("Arial", 30, "bold"))  # Larger size
    else:
        welcome_label.config(font=("Arial", 14, "bold"))  # H3 size
        heading_label.config(font=("Arial", 20, "bold"))  # Smaller size
    resize_icons(event)

# Button Icons
icons = ["newstudent.png", "newbook.png", "stats.png", "issue.png", "return.png", "logout.png"]
tooltips = ["New Student", "New Book", "Statistics", "Issue Book", "Return Book", "Logout"]
file_paths = ["new_student.py", "new_book.py", "stats.py", "issue_book.py", "return_book.py", "login.py"]

# Ensure each icon is the same size and equidistant
for i, icon in enumerate(icons):
    img = tk.PhotoImage(file=icon).subsample(2, 2)  # Resize images to 75px
    if icon == "logout.png":
        command = lambda file_path=file_paths[i]: execute_file(file_path)
    else:
        command = lambda file_path=file_paths[i]: execute_file(file_path)
    btn = tk.Button(nav_frame, image=img, bg="white", relief="flat", command=command, width=75, height=75)
    btn.image = img  # Keep a reference to prevent garbage collection
    btn.grid(row=0, column=i, padx=20, pady=10)  # Adjust padx for equidistant spacing
    btn.bind("<Enter>", lambda event, text=tooltips[i]: show_tooltip(event, text))
    btn.bind("<Leave>", hide_tooltip)
    # Add a square border around the icons with white inside
    btn.config(borderwidth=2, relief="solid", highlightbackground="white", highlightcolor="white", highlightthickness=2)

# Center the icons
nav_frame.grid_columnconfigure(tuple(range(len(icons))), weight=1)

# Bind the resize event to adjust icon sizes and spacing
root.bind("<Configure>", resize_elements)

root.mainloop()