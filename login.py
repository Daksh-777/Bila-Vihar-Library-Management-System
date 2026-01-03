import tkinter as tk
from tkinter import messagebox
import os

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if not captcha_var.get():
        messagebox.showerror("Captcha Error", "Please verify that you are not a robot.")
        return
    
    if username == "admin" and password == "password":
        open_main_script()
    elif username == "admin" and password != "password":
        messagebox.showerror("Login Failed", "Invalid Password")
    elif username != "admin" and password == "password":
        messagebox.showerror("Login Failed", "Invalid Username")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def open_main_script():
    root.destroy()
    os.system("python main.py")

def close_app():
    root.destroy()

def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

def exit_app(event=None):
    root.destroy()

# Main Window
root = tk.Tk()
root.title("Bala Vihar Library Management System")
root.geometry("1100x700")  # Increased size
root.configure(bg="#333333")  # Dark grey background

# Bind keys
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_app)

# Frame
frame = tk.Frame(root, bg="#444444", padx=50, pady=50, relief="solid", bd=2)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
tk.Label(frame, text="ACCOUNT LOGIN", font=("Arial", 22, "bold"), fg="white", bg="#444444").pack(pady=15)

# Username Label
tk.Label(frame, text="USERNAME", font=("Arial", 12, "bold"), fg="white", bg="#444444").pack(anchor="w")
# Username Entry 
username_entry = tk.Entry(frame, font=("Arial", 14), width=35, relief="solid", bg="white", fg="black", bd=1)
username_entry.pack(pady=5)

# Password Label
tk.Label(frame, text="PASSWORD", font=("Arial", 12, "bold"), fg="white", bg="#444444").pack(anchor="w")
# Password Entry 
password_entry = tk.Entry(frame, font=("Arial", 14), width=35, relief="solid", bg="white", fg="black", bd=1, show="*")
password_entry.pack(pady=5)

# Captcha Checkbox
captcha_var = tk.BooleanVar()
captcha_check = tk.Checkbutton(frame, text="I'm not a robot", variable=captcha_var, bg="#444444", fg="white", font=("Arial", 12, "bold"), selectcolor="#444444")
captcha_check.pack(pady=12)

# Login Button
btn_login = tk.Button(frame, text="LOG IN", font=("Arial", 14, "bold"), bg="black", fg="white", width=25, height=2, command=validate_login)
btn_login.pack(pady=15)

# Close Button 
btn_close = tk.Button(root, text="Close", font=("Arial", 12), bg="black", fg="white", command=close_app)
btn_close.place(relx=0.95, rely=0.05, anchor="ne")

root.mainloop()
