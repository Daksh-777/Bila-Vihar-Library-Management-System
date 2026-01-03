# Bila-Vihar-Library-Management-System
A desktop-based **Library Management System** built in Python using `tkinter` for the GUI. Designed to handle core library operations: user authentication, book registration, search, issue, and return — all with persistent data storage.
---

## 🎯 Features

- 🔐 **User Login & Session Control**
  - Secure credential validation
  - Error messages for invalid inputs
  - Role-based access (admin/user implied)

- 📖 **Book Management**
  - Add new books with ISBN, title, author, publisher
  - Search books by ISBN or title
  - View all registered books in a tabular format

- 🔄 **Issue & Return System**
  - Record book issuance with borrower ID and date
  - Track return status and update availability
  - Prevent duplicate issues or returns without valid records

- ⚙️ **Data Persistence**
  - Stores all records in structured text files 
  - Maintains state across application restarts

- 🖥️ **User-Friendly Interface**
  - Clean, dark-themed GUI with modal windows
  - Input validation and real-time feedback via pop-up dialogs
  - Intuitive navigation with icons and buttons

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** — for GUI components and event handling
- **File I/O** — for persistent storage (or **SQLite** if used)
- **Custom Logic** — for business rules (e.g., preventing re-issue, validating ISBNs)

---
