# SDEV_220_Final_Project_CodeCrafters
The purpose of this repository is for the sharing and collaboration of our SDEV 220 project for IvyTech.
# 📚 Library Inventory Management System
### SDEV 220 Final Project — Code Crafters | IvyTech Community College

A Python-based Library Inventory Management System with a graphical user interface (GUI) built for HypotheticalReaders Inc., a fictional public library organization. The system allows library staff to manage books, customers, and checkouts through an intuitive desktop application.

---

## 👥 Team — Code Crafters

| Name | GitHub | Role |
|------|--------|------|
| Shawn Barker | [@nearshawnbo](https://github.com/nearshawnbo) | Project Leader / Data Systems & Architecture Lead |
| Ivan Manuel | [@vahnflare](https://github.com/vahnflare) | GUI & Application Logic Lead |
| Harold Rogers | [@Harold3131](https://github.com/Harold3131) | QC & Bug Fix Lead |

---

## 🗂️ Project Management
- **Trello Board:** https://trello.com/b/2Dq8FH6A/sdev-220-final-project
- **GitHub Repo:** https://github.com/nearshawnbo/SDEV_220_Final_Project_CodeCrafters

---

## 🚀 Features

- Add, remove, update, and search books by title, author, or ID
- Add, remove, and update library customers
- Check books in and out with date tracking
- View all books and customers
- Track overdue books and flag overdue customers
- Persistent data storage using SQLite
- Full graphical user interface built with Tkinter

---

## 🏗️ System Architecture

The system is built in three layers:

| File | Purpose |
|------|---------|
| `database.py` | SQLite database connection, table initialization, and all CRUD functions |
| `models.py` | Object-oriented classes — `Book`, `Customer`, and `Library` |
| `GUI_Layer.py` | Tkinter graphical user interface — all windows, forms, and buttons |
| `main.py` | Application entry point |

### Classes
- **Book** — Represents a single book with attributes and availability checking
- **Customer** — Represents a library member with overdue book lookup
- **Library** — Manages all operations, bridging the GUI and database layers

### Collections Used
- `list` — Stores book objects in memory
- `dict` — Enables fast book lookup by ID
- `tuple` — Stores fixed field names for books and customers

---

## 🛠️ Requirements & Setup

### Dependencies
```
Python 3.x
tkinter (built into Python)
Pillow (PIL)
sqlite3 (built into Python)
```

### Install Dependencies
```bash
pip install Pillow
```

### Run the Application
```bash
python main.py
```

> ⚠️ Make sure `background_clean.png` is in the same directory as the Python files before running.

---

## ✅ Minimum Requirements Compliance

| Requirement | Status |
|-------------|--------|
| Graphical User Interface | ✔ Tkinter GUI |
| At least three interacting classes | ✔ Book, Customer, Library |
| Use of collections (lists, dictionaries, tuples) | ✔ All three used |
| Error-free execution | ✔ Tested and verified |
| Complete documentation | ✔ Proposal, Bug Fix Log, Final Report |
