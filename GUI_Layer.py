import tkinter as tk
from tkinter import messagebox
from models import Library
from PIL import Image, ImageTk


class LibraryGUI:

    def __init__(self):

        self.library = Library()
        self.library.load_books()

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

        # BUTTON PANEL
        button_frame = tk.Frame(self.root, bg="#1b4332", padx=20, pady=20)
        button_frame.place(relx=0.5, rely=0.55, anchor="center")

        button_style = {
            "width": 22,
            "height": 2,
            "bg": "#2e7d32",
            "fg": "white",
            "font": ("Arial", 11, "bold"),
            "bd": 0,
            "activebackground": "#43a047",
            "activeforeground": "white"
        }

        buttons = [
            ("Add Book", self.add_book_menu),
            ("View Books", self.view_books),
            ("Search Book", self.search_book),
            ("Checkout Book", self.checkout_book)
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, **button_style)
            btn.pack(pady=6)
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

        self.root.mainloop()

    # HOVER EFFECT
    def on_enter(self, e):
        e.widget["bg"] = "#43a047"

    def on_leave(self, e):
        e.widget["bg"] = "#2e7d32"
    
    # ADD MENU BOOK
    def add_book_menu(self):

        window = tk.Toplevel(self.root)
        window.title("Book Management")
        window.geometry("250x200")

        tk.Button(window,
                text="Add Book",
                width=20,
                command=self.add_book).pack(pady=10)

        tk.Button(window,
                text="Remove Book",
                width=20,
                command=self.remove_book).pack(pady=10)

        tk.Button(window,
                text="Add Customer",
                width=20,
                command=self.add_customer).pack(pady=10)

    # ADD BOOK
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
            self.library.add_book(title.get(), author.get(), int(copies.get()))
            messagebox.showinfo("Success", "Book Added")

        tk.Button(window, text="Save", command=save).pack(pady=10)
    
    def remove_book(self):

        window = tk.Toplevel(self.root)
        window.title("Remove Book")

        tk.Label(window, text="Book ID").pack()
        book_id = tk.Entry(window)
        book_id.pack()

        def delete():
            self.library.remove_book(int(book_id.get()))
            messagebox.showinfo("Success", "Book Removed")

        tk.Button(window, text="Delete", command=delete).pack(pady=10)
    
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

        tk.Button(window, text="Save", command=save).pack(pady=10)

    # VIEW BOOKS
    def view_books(self):

        books = self.library.get_all_books()

        window = tk.Toplevel(self.root)
        window.title("Books")

        for book in books:
            text = f"{book[1]} | {book[2]}"
            tk.Label(window, text=text).pack()

    # SEARCH BOOK
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
                text = f"{book[1]} | {book[2]}"
                tk.Label(result_window, text=text).pack()

        tk.Button(window, text="Search", command=search).pack(pady=10)

    # CHECKOUT BOOK
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

        def checkout_book():
            self.library.checkout_book(
                int(book_id.get()),
                int(customer_id.get()),
                checkout.get(),
                due.get()
            )
            messagebox.showinfo("Success", "Book Checked Out")

        tk.Button(window, text="Checkout", command=checkout_book).pack(pady=10)