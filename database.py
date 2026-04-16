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

# Book CRUD 6 Functions - Bug Fix # 16 - Empty fields on Add Book, Bug Fix # 18. Zero or negative copies. FIX = Added checks to ensure fields aren't blank and that copy counts are valid before sending them to database.
def add_book(title, author, total_copies):
    # Bug 16: Check for empty fields
    if not title.strip() or not author.strip():
        return "Error: Title and Author cannot be empty."
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Bug 18: The CHECK constraint in your SQL will trigger an IntegrityError if total_copies < 0
            cursor.execute("""
                INSERT INTO Books (title, author, total_copies, available_copies)
                VALUES (?, ?, ?, ?)
            """, (title, author, total_copies, total_copies))
            conn.commit()
            return "Success"
    except sqlite3.IntegrityError:
        return "Error: Total copies must be a positive number."

# Fix for Bug # 2 - Remove book with active checkouts, Critical Bug # 4 - Invalid Book ID on remove - FIX = Updated delete_book and delete_customer to catch active checkouts and check if the ID actually exists 
def delete_book(book_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Books WHERE book_id = ?", (book_id,))
            if cursor.rowcount == 0:
                return "Error: Book ID not found."
            conn.commit()
            return "Success"
    except sqlite3.IntegrityError:
        return "Error: Cannot delete book. It is currently checked out by a customer."


def update_book(title, author, total_copies, book_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE Books SET title =?, author = ?, total_copies = ?, available_copies = ? - (total_copies - available_copies)
                         WHERE book_id = ?""",(title, author, total_copies, total_copies,book_id, ))
        conn.commit()

def get_all_books():
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books")
        return cursor.fetchall()

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

#Customer CRUD 5 Functions # Fix for Bug # 17 - Empty fields on Add Customer - FIX = Added checks to ensure fields aren't blank and that copy counts are valid before sending them to the database.
def create_customer(first_name, last_name, phone):
    # Bug 17: Check for empty fields
    if not first_name.strip() or not last_name.strip():
        return "Error: Customer name cannot be empty."
        
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Customers (first_name, last_name, phone)
            VALUES (?, ?, ?)
        """, (first_name, last_name, phone))
        conn.commit()
        return "Success"

# Critical Bug Fix # 3 - Remove customer with active checkouts - FIX = Updated delete_customer to catch active checkouts and check if the ID actually exists in (database.py) folder.
def delete_customer(customer_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
            if cursor.rowcount == 0:
                return "Error: Customer ID not found."
            conn.commit()
            return "Success"
    except sqlite3.IntegrityError:
        return "Error: Cannot delete customer. They still have books checked out."

def get_all_customers():
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        return cursor.fetchall()
     
def update_customer(first_name, last_name, phone, customer_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Customers SET first_name = ?, last_name = ?, phone = ? WHERE customer_id = ?",(first_name, last_name, phone, customer_id,))
        conn.commit()

def delete_customer(customer_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute( " DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
        conn.commit()
#Checkout CRUD 5 Functions # Fix for Bug # 1 - Checkout with no available copies - FIX = New code checks if book actually exists before trying to check it out.
def log_checkout(book_id, customer_id, checkout_date, due_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available_copies FROM Books WHERE book_id = ?", (book_id,))
        result = cursor.fetchone()
        
        if not result:
            return "Error: Book ID does not exist."
            
        if result[0] > 0:
            cursor.execute("""
                INSERT INTO Checkouts (book_id, customer_id, checkout_date, due_date)
                VALUES (?, ?, ?, ?)
            """, (book_id, customer_id, checkout_date, due_date))
            cursor.execute("""
                UPDATE Books
                SET available_copies = available_copies - 1
                WHERE book_id = ?
            """, (book_id,))
            conn.commit()
            return "Success"
        else:
            return "Error: No available copies left for this book."

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

def get_active_checkouts():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute (""" 
            SELECT Checkouts.checkout_id, Customers.first_name, Customers.last_name, 
                   Books.title, Checkouts.checkout_date, Checkouts.due_date
            FROM Checkouts 
            INNER JOIN Customers ON Checkouts.customer_id = Customers.customer_id
            INNER JOIN Books ON Checkouts.book_id = Books.book_id
            WHERE return_date IS NULL
            """)
        return cursor.fetchall()

def get_checkouts_by_customer (customer_id):     
       with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute ("""
            SELECT Checkouts.checkout_id, Customers.first_name, Customers.last_name, 
                   Books.title, Checkouts.checkout_date, Checkouts.due_date
            FROM Checkouts
            INNER JOIN Customers ON Checkouts.customer_id = Customers.customer_id
            INNER JOIN Books ON Checkouts.book_id = Books.book_id
            WHERE Customers.customer_id = ? """, (customer_id,)) 
        return cursor.fetchall()
              
def get_overdue_books ():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Checkouts.checkout_id, Customers.first_name, Customers.last_name, 
                   Books.title, Checkouts.checkout_date, Checkouts.due_date
            FROM Checkouts
            INNER JOIN Customers ON Checkouts.customer_id = Customers.customer_id
            INNER JOIN Books ON Checkouts.book_id = Books.book_id
            WHERE due_date < DATE('now') AND  return_date IS NULL""")
        return cursor.fetchall()
    
def get_overdue_books_by_customer (customer_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Checkouts.checkout_id, Customers.first_name, Customers.last_name, 
                   Books.title, Checkouts.checkout_date, Checkouts.due_date
            FROM Checkouts
            INNER JOIN Customers ON Checkouts.customer_id = Customers.customer_id
            INNER JOIN Books ON Checkouts.book_id = Books.book_id
            WHERE due_date < DATE('now') AND  return_date IS NULL AND Checkouts.customer_id = ?""", (customer_id,))
        return cursor.fetchall()
    
def purge_all_data ():
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute ("DELETE FROM Checkouts")
        cursor.execute ("DELETE FROM Customers")
        cursor.execute ("DELETE FROM Books")
        conn.commit()

def get_overdue_books(current_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Checkouts.checkout_id, Books.title, Customers.first_name, Checkouts.due_date
            FROM Checkouts
            JOIN Books ON Checkouts.book_id = Books.book_id
            JOIN Customers ON Checkouts.customer_id = Customers.customer_id
            WHERE Checkouts.return_date IS NULL AND Checkouts.due_date < ?
        """, (current_date,))
        return cursor.fetchall()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized and tables created successfully.")