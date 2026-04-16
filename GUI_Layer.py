from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
from models import Library
from PIL import Image, ImageTk


class LibraryGUI:

    def __init__(self):

        # Load library system
        self.library = Library()
        self.library.load_books()

        # MAIN WINDOW
        self.root = tk.Tk()
        self.root.title("Public Library Inventory System")
        self.root.geometry("700x550")

        # Build UI
        self.build_main_menu()

        # Start GUI loop
        self.root.mainloop()

    # ================= MAIN MENU =================

    def build_main_menu(self):

        # BACKGROUND IMAGE
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, "background_clean.png")

            bg_image = Image.open(img_path)
            bg_image = bg_image.resize((700, 550))
            self.bg = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            self.root.configure(bg="#1b4332")

        # TITLE
        title = tk.Label(
            self.root,
            text="Public Library System",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1b4332"
        )
        title.place(relx=0.5, rely=0.12, anchor="center")

        # MENU FRAME
        menu_frame = tk.Frame(self.root, bg="#1b4332", padx=40, pady=30)
        menu_frame.place(relx=0.5, rely=0.6, anchor="center")

        button_style = {
            "width": 20,
            "height": 2,
            "bg": "#2e7d32",
            "fg": "white",
            "font": ("Arial", 12, "bold")
        }

        tk.Button(menu_frame, text="Books",
                  command=self.books_menu,
                  **button_style).pack(pady=8)

        tk.Button(menu_frame, text="Customers",
                  command=self.customers_menu,
                  **button_style).pack(pady=8)

        tk.Button(menu_frame, text="Checkouts",
                  command=self.checkouts_menu,
                  **button_style).pack(pady=8)

    # ================= BOOKS MENU =================
# Check if window already exists Bug # 15 - Multiple windows stacking - FIX = Updated buttons inside to use self.books_win instead of the generic window variable so that the "anti-stacking" logic works correctly. 
    def books_menu(self):
        if hasattr(self, 'books_win') and self.books_win.winfo_exists():
            self.books_win.lift()
            return

        self.books_win = tk.Toplevel(self.root)
        self.books_win.title("Books")

        tk.Button(self.books_win, text="Add", width=20,
                  command=self.add_book).pack(pady=5)

        tk.Button(self.books_win, text="Remove", width=20,
                  command=self.remove_book).pack(pady=5)

        tk.Button(self.books_win, text="View All", width=20,
                  command=self.view_books).pack(pady=5)

        tk.Button(self.books_win, text="Search", width=20,
                  command=self.search_book).pack(pady=5)

    # ================= CUSTOMERS MENU =================
# part of fix for (critical) Bugs 7 & 11
    def customers_menu(self):
        if hasattr(self, 'cust_win') and self.cust_win.winfo_exists():
            self.cust_win.lift()
            return

        self.cust_win = tk.Toplevel(self.root)
        self.cust_win.title("Customers")

        tk.Button(self.cust_win, text="Add", width=20,
                  command=self.add_customer).pack(pady=5)

        tk.Button(self.cust_win, text="Remove", width=20,
                  command=self.remove_customer).pack(pady=5)

        tk.Button(self.cust_win, text="Check-In/Out History", width=20,
          command=self.update_customer_ui).pack(pady=5)

        tk.Button(self.cust_win, text="View All", width=20,
                  command=self.view_customers).pack(pady=5)
        
    # Fix for Grid Layout View-All Customers
    def view_customers(self):
        customers = self.library.get_all_customers()
        window = tk.Toplevel(self.root)
        window.title("Customer Directory")

        headers = ["ID", "First Name", "Last Name", "Phone"]

        # HEADER ROW
        for col, text in enumerate(headers):
            tk.Label(
                window,
                text=text,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        # DATA ROWS
        for row_index, c in enumerate(customers, start=1):
            for col_index, value in enumerate(c):
                tk.Label(
                    window,
                    text=value,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=row_index, column=col_index, sticky="nsew")
    def remove_customer(self):
        window = tk.Toplevel(self.root)
        window.title("Remove Customer")

        tk.Label(window, text="Customer ID").pack()
        c_id = tk.Entry(window)
        c_id.pack()

        def delete():
            if not messagebox.askyesno("Confirm", "Are you sure?"):
                return

            result = self.library.remove_customer(int(c_id.get()))
            if "Error" in result:
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Customer Removed")
                window.destroy()

        tk.Button(window, text="Delete", command=delete).pack(pady=10)
    # Fix for Customer Update Window
    def update_customer_ui(self):
        history = self.library.get_active_checkouts()

        window = tk.Toplevel(self.root)
        window.title("Customer Check-in/out History")

        # ===== COLUMN HEADERS =====
        headers = [
            "Checkout ID",
            "Customer Name",
            "Book Title",
            "Checkout Date",
            "Due Date"
        ]

        for col, text in enumerate(headers):
            tk.Label(
                window,
                text=text,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        # ===== NO DATA CASE =====
        if not history:
            tk.Label(
                window,
                text="No active checkouts found"
            ).grid(row=1, column=0, columnspan=5)
            return

        # ===== DATA ROWS =====
        for row_index, h in enumerate(history, start=1):

            # EXPECTED FORMAT:
            # h = (checkout_id, first_name, last_name, book_title, checkout_date, due_date)

            checkout_id = h[0]
            customer_name = f"{h[1]} {h[2]}"
            book_title = h[3]
            checkout_date = h[4]
            due_date = h[5]

            row = [
                checkout_id,
                customer_name,
                book_title,
                checkout_date,
                due_date
            ]

            for col_index, value in enumerate(row):
                tk.Label(
                    window,
                    text=value,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=row_index, column=col_index, sticky="nsew")

    # Modified to enable add_customer button to work
    def add_customer(self):
        window = tk.Toplevel(self.root)
        window.title("Add Customer")

        tk.Label(window, text="First Name").pack()
        first = tk.Entry(window)
        first.pack()

        tk.Label(window, text="Last Name").pack()
        last = tk.Entry(window)
        last.pack()

        tk.Label(window, text="Phone").pack()
        phone = tk.Entry(window)
        phone.pack()

        def save():
            self.library.add_customer(first.get(), last.get(), phone.get())
            messagebox.showinfo("Success", "Customer Added")
            window.destroy()

        tk.Button(window, text="Save", command=save).pack(pady=10)
    # ================= CHECKOUT MENU =================
# Part of (critical) Bug fix for 8, 9, & 11 - Dead Buttons - FIX = Arguments to buttons for line 332 (critical) Bug fix
    def checkouts_menu(self):
        window = tk.Toplevel(self.root)
        window.title("Checkouts")

        tk.Button(window, text="Checkout", width=20,
                  command=self.checkout_book).pack(pady=5)

        tk.Button(window, text="Checkin", width=20,
                  command=self.checkin_book).pack(pady=5)

        tk.Button(window, text="View Overdue", width=20,
                  command=self.view_overdue).pack(pady=5)
        
    # Fix for checkout_book
    def checkout_book(self):
        window = tk.Toplevel(self.root)
        window.title("Checkout Book")

        today = datetime.now().strftime("%Y-%m-%d")  # ✅ AUTO DATE

        tk.Label(window, text="Customer ID").pack()
        cust_id = tk.Entry(window)
        cust_id.pack()

        tk.Label(window, text="Book ID").pack()
        book_id = tk.Entry(window)
        book_id.pack()

        tk.Label(window, text="Due Date (YYYY-MM-DD)").pack()
        due_date = tk.Entry(window)
        due_date.pack()
  
        def checkout():
            result = self.library.checkout_book(
                int(book_id.get()),
                int(cust_id.get()),
                today,  
                due_date.get()
            )

            messagebox.showinfo("Checkout Result", result)

        tk.Button(window, text="Checkout", command=checkout).pack(pady=10)

    # Fix for checkin_book()
    def checkin_book(self):
        window = tk.Toplevel(self.root)
        window.title("Checkin Book")

        tk.Label(window, text="Checkout ID").pack()
        checkout_id = tk.Entry(window)
        checkout_id.pack()

        tk.Label(window, text="Return Date (YYYY-MM-DD)").pack()
        return_date = tk.Entry(window)
        return_date.pack()

        def checkin():   # ✅ INSIDE method
            result = self.library.return_book(
                int(checkout_id.get()),
                return_date.get(),
                0
            )
            messagebox.showinfo("Result", result)

        tk.Button(window, text="Checkin", command=checkin).pack(pady=10)
 
    # Fix for View Overdue
    def view_overdue(self):
        overdue = self.library.get_overdue_books()

        window = tk.Toplevel(self.root)
        window.title("Overdue Books")

        headers = ["Customer Name", "Book Title", "Due Date"]

        for col, text in enumerate(headers):
            tk.Label(
                window,
                text=text,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        if not overdue:
            tk.Label(
                window,
                text="No overdue books",
                fg="green"
            ).grid(row=1, column=0, columnspan=3)
            return

        for row_index, o in enumerate(overdue, start=1):

            # Handle possible tuple formats safely
            if len(o) == 4:
                customer_name = o[2]
                book_title = o[1]
                due_date = o[3]
            elif len(o) == 3:
                customer_name = o[0]
                book_title = o[1]
                due_date = o[2]
            else:
                customer_name = str(o)
                book_title = ""
                due_date = ""

            row = [customer_name, book_title, due_date]

            for col_index, value in enumerate(row):
                tk.Label(
                    window,
                    text=value,
                    fg="red" if col_index == 2 else "black",
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=row_index, column=col_index, sticky="nsew")
    # ================= BOOK FUNCTIONS =================

    def add_book(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")

        tk.Label(window, text="Title").pack()
        title = tk.Entry(window)
        title.pack()

        tk.Label(window, text="Author").pack()
        author = tk.Entry(window)
        author.pack()

        tk.Label(window, text="Copies").pack()
        copies = tk.Entry(window)
        copies.pack()

        def save():
            try:
                self.library.add_book(
                    title.get(), author.get(), int(copies.get()))
                messagebox.showinfo("Success", "Book Added")
                window.destroy()
            except:
                messagebox.showerror("Error", "Copies must be a number")

        tk.Button(window, text="Save", command=save).pack(pady=10)

    def remove_book(self):
        window = tk.Toplevel(self.root)
        window.title("Remove Book")

        tk.Label(window, text="Book ID").pack()
        book_id = tk.Entry(window)
        book_id.pack()

# Fix for Bug # 14 - No confirmation of delete - FIX = Added prompt where users are asked "Are you sure?" before data is removed.

        def delete():
            if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
                return

            try:
                result = self.library.remove_book(int(book_id.get()))
                if "Error" in result:
                    messagebox.showerror("Error", result)
                else:
                    messagebox.showinfo("Success", "Book Removed")
                    window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter numeric ID")

        tk.Button(window, text="Remove Book",
                  command=delete).pack(pady=10)
        
# Fix for (critical) Bug # 12 - View_Books shows limited info - FIX = Modified code to show more info in view_books.       
# Added Fix for Grid Layout for View-All Books
    def view_books(self):
        books = self.library.get_all_books()
        window = tk.Toplevel(self.root)
        window.title("Library Inventory")

        headers = ["ID", "Title", "Author", "Total", "Available"]

        # HEADER ROW
        for col, text in enumerate(headers):
            tk.Label(
                window,
                text=text,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")

        # DATA ROWS
        for row_index, b in enumerate(books, start=1):
            for col_index, value in enumerate(b):
                tk.Label(
                    window,
                    text=value,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=row_index, column=col_index, sticky="nsew")

# Fix for (critical) Bug # 6 - No search by ID or Author in GUI - FIX = Modified code to expand search window to accept more than just the title. Added input fields for Author and Book ID.

    def search_book(self):
        window = tk.Toplevel(self.root)
        window.title("Search Inventory")

        tk.Label(window, text="Title").pack()
        title_entry = tk.Entry(window)
        title_entry.pack()

        tk.Label(window, text="Author").pack()
        author_entry = tk.Entry(window)
        author_entry.pack()

        tk.Label(window, text="Book ID").pack()
        id_entry = tk.Entry(window)
        id_entry.pack()

        def search():
            t = title_entry.get().strip()
            a = author_entry.get().strip()
            i = id_entry.get().strip()

            results = []

            if i:
                try:
                    results = self.library.search_book(book_id=int(i))
                except ValueError:
                    messagebox.showerror("Error", "ID must be a number")
                    return

            elif t:
                results = self.library.search_book(title=t)

            elif a:
                results = self.library.search_book(author=a)

            else:
                messagebox.showwarning("Input Error", "Enter search criteria")
                return

            if not results:
                messagebox.showinfo("Results", "No books found")
                return

            # ===== RESULTS WINDOW =====
            res_win = tk.Toplevel(window)
            res_win.title("Search Results")

            headers = ["ID", "Title", "Author", "Available"]

            # HEADER ROW
            for col, text in enumerate(headers):
                tk.Label(
                    res_win,
                    text=text,
                    font=("Arial", 10, "bold"),
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=0, column=col, sticky="nsew")

            # DATA ROWS
            for row_index, b in enumerate(results, start=1):
                for col_index, value in enumerate(b):
                    tk.Label(
                        res_win,
                        text=value,
                        borderwidth=1,
                        relief="solid",
                        padx=5,
                        pady=5
                    ).grid(row=row_index, column=col_index, sticky="nsew")

        tk.Button(window, text="Search",
                command=search).pack(pady=10)

if __name__ == "__main__":
    LibraryGUI()