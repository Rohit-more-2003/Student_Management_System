# 🎓 Student Management System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

A desktop-based CRUD application designed to manage student records efficiently. [cite_start]The system utilizes a graphical interface to interact with a local database, allowing for streamlined data entry and retrieval.

---

### ✨ Features

* [cite_start]**Interactive Dashboard**: Displays student ID, Name, Course, and Mobile numbers in a structured table.
* [cite_start]**Data Persistence**: Uses SQLite to store and manage student information locally in `database.db`.
* [cite_start]**Student Registration**: Includes a dedicated dialog to add new students with specific course selections like Biology, Maths, and Astronomy.
* [cite_start]**Search Functionality**: Allows users to locate specific student records by name.
* [cite_start]**Record Management**: Dynamic status bar buttons enable the editing or deletion of selected records directly from the main window.
* [cite_start]**About Section**: Provides information regarding the application's purpose and creation.

### 🛠 Tech Stack

* [cite_start]**GUI Framework**: PyQt6 (v6.10.1).
* [cite_start]**Database**: SQLite3.
* [cite_start]**Language**: Python 3.x.

### 📂 Project Structure

```text
├── main.py             # Main application logic and PyQt6 interface 
├── database.db         # SQLite database containing 'students' table [cite: 39]
├── requirements.txt    # Project dependencies (PyQt6) 
└── icons/              # UI assets 
    └── icons/
        ├── add.png     # Icon for adding records
        └── search.png  # Icon for searching records
```

---

## ⚙️ Installation & Setup

Copy and paste the entire block below into your terminal to set up and run the project:

```text
# Clone the repository, setup environment, install dependencies, and run
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system

python3 -m venv venv

source venv/bin/activate
pip install -r requirements.txt
```

---

## Run the Application

python3 main.py
