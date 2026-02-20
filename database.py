import sqlite3

DB_NAME = "library.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


#Initializes the Database
def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        #Books Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
            available_copies INTEGER NOT NULL CHECK (
                available_copies >= 0 AND
                available_copies <= total_copies
            )
        );
        """)

        # Customer Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT
        );
        """)

        # Checkout Table 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Checkouts (
            checkout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            checkout_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        );
        """)
        conn.commit()

# Book CRUD
def add_book(title, author, total_copies):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Books (title, author, total_copies, available_copies)
            VALUES (?, ?, ?, ?)
        """, (title, author, total_copies, total_copies))
        conn.commit()

#Delete Book
def delete_book(book_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
        conn.commit()



def get_book_by_id(book_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE book_id = ?", (book_id,))
        return cursor.fetchone()

def search_book(title=None, book_id=None, author=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        if book_id is not None:
            cursor.execute("SELECT * FROM Books WHERE book_id = ?", (book_id,))
        elif title is not None:
            cursor.execute("SELECT * FROM Books WHERE title LIKE ?", (f"%{title}%",))
        elif author is not None:
            cursor.execute("SELECT * FROM Books WHERE author LIKE ?", (f"%{author}%",))
        else:
            return None

        return cursor.fetchall() 

#Customer CRUD
def create_customer(first_name, last_name, phone):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Customers (first_name, last_name, phone)
            VALUES (?, ?, ?)
        """, (first_name, last_name, phone))
        conn.commit()

#Checkout CRUD
def log_checkout(book_id, customer_id, checkout_date, due_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Checkouts (book_id, customer_id, checkout_date, due_date)
            VALUES (?, ?, ?, ?)
        """, (book_id, customer_id, checkout_date, due_date))
        cursor.execute("""
            UPDATE Books
            SET available_copies = available_copies - 1
            WHERE book_id = ? AND available_copies > 0
        """, (book_id,))
        conn.commit()

def log_return(checkout_id, return_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Checkouts
            SET return_date = ?
            WHERE checkout_id = ?
        """, (return_date, checkout_id))
        cursor.execute("""
            UPDATE Books
            SET available_copies = available_copies + 1
            WHERE book_id = (
                SELECT book_id FROM Checkouts WHERE checkout_id = ?
            )
        """, (checkout_id,))
        conn.commit()



