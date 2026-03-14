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

        # BACKGROUND IMAGE
        bg_image = Image.open("background_clean.png")
        bg_image = bg_image.resize((700, 550))
        self.bg = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # TITLE
        title = tk.Label(
            self.root,
            text="Public Library System",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1b4332"
        )
        title.place(relx=0.5, rely=0.12, anchor="center")

        # ================= MAIN MENU =================

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

        self.root.mainloop()

    # ================= BOOKS MENU =================

    def books_menu(self):

        window = tk.Toplevel(self.root)
        window.title("Books")

        tk.Button(window, text="Add", width=20,
                  command=self.add_book).pack(pady=5)

        tk.Button(window, text="Remove", width=20,
                  command=self.remove_book).pack(pady=5)

        tk.Button(window, text="Update", width=20).pack(pady=5)

        tk.Button(window, text="View All", width=20,
                  command=self.view_books).pack(pady=5)

        tk.Button(window, text="Search", width=20,
                  command=self.search_book).pack(pady=5)

    # ================= CUSTOMER MENU =================

    def customers_menu(self):

        window = tk.Toplevel(self.root)
        window.title("Customers")

        tk.Button(window, text="Add", width=20,
                  command=self.add_customer).pack(pady=5)

        tk.Button(window, text="Remove", width=20).pack(pady=5)

        tk.Button(window, text="Update", width=20).pack(pady=5)

        tk.Button(window, text="Search", width=20).pack(pady=5)

    # ================= CHECKOUT MENU =================

    def checkouts_menu(self):

        window = tk.Toplevel(self.root)
        window.title("Checkouts")

        tk.Button(window, text="Checkout", width=20,
                  command=self.checkout_book).pack(pady=5)

        tk.Button(window, text="Checkin", width=20).pack(pady=5)

        tk.Button(window, text="View Overdue", width=20).pack(pady=5)

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
                self.library.add_book(title.get(), author.get(), int(copies.get()))
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

        def delete():
            try:
                self.library.remove_book(int(book_id.get()))
                messagebox.showinfo("Success", "Book Removed")
                window.destroy()
            except:
                messagebox.showerror("Error", "Invalid Book ID")

        tk.Button(window, text="Delete", command=delete).pack(pady=10)

    def view_books(self):

        books = self.library.get_all_books()

        window = tk.Toplevel(self.root)
        window.title("Books")

        for book in books:
            text = f"{book[0]} | {book[1]} | {book[2]}"
            tk.Label(window, text=text).pack()

    def search_book(self):

        window = tk.Toplevel(self.root)
        window.title("Search Book")

        tk.Label(window, text="Title").pack()
        title = tk.Entry(window)
        title.pack()

        def search():
            results = self.library.search_book(title=title.get())

            result_window = tk.Toplevel(window)

            for book in results:
                text = f"{book[0]} | {book[1]} | {book[2]}"
                tk.Label(result_window, text=text).pack()

        tk.Button(window, text="Search", command=search).pack(pady=10)

    # ================= CUSTOMER =================

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

    # ================= CHECKOUT =================

    def checkout_book(self):

        window = tk.Toplevel(self.root)
        window.title("Checkout Book")

        tk.Label(window, text="Book ID").pack()
        book_id = tk.Entry(window)
        book_id.pack()

        tk.Label(window, text="Customer ID").pack()
        customer_id = tk.Entry(window)
        customer_id.pack()

        tk.Label(window, text="Checkout Date").pack()
        checkout = tk.Entry(window)
        checkout.pack()

        tk.Label(window, text="Due Date").pack()
        due = tk.Entry(window)
        due.pack()

        def checkout_action():
            try:
                self.library.checkout_book(
                    int(book_id.get()),
                    int(customer_id.get()),
                    checkout.get(),
                    due.get()
                )
                messagebox.showinfo("Success", "Book Checked Out")
                window.destroy()
            except:
                messagebox.showerror("Error", "Invalid Input")

        tk.Button(window, text="Checkout",
                  command=checkout_action).pack(pady=10)
