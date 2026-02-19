import sqlite3


#Initializes teh Database
def initialize_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()


    # Enables Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")


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
    conn.close()



