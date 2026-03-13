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
        self.root.geometry("600x500")
       

        # Load background image
        bg_image = Image.open("background_clean.png")

        # Resize image to window size
        bg_image = bg_image.resize((600, 500))

        self.bg = ImageTk.PhotoImage(bg_image)

        # Place image as background
        bg_label = tk.Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(
            self.root,
            text="Public Library System",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#2c6e49"
        )

        title.place(relx=0.5, rely=0.15, anchor="center")
        button_frame = tk.Frame(self.root, bg="#1b4332", bd=2, padx=20, pady=20)
        button_frame.place(relx=0.5, rely=0.6, anchor="center")

        button_style = {
            "width": 20,
            "height": 2,
            "bg": "#2e7d32",
            "fg": "white",
            "font": ("Arial", 11, "bold"),
            "bd": 0,
            "activebackground": "#43a047",
            "activeforeground": "white"
        }

        btn1 = tk.Button(button_frame, text="Add Book", command=self.add_book, **button_style)
        btn1.pack(pady=5)
        btn1.bind("<Enter>", self.on_enter)
        btn1.bind("<Leave>", self.on_leave)

        btn2 = tk.Button(button_frame, text="View Books", command=self.view_books, **button_style)
        btn2.pack(pady=5)
        btn2.bind("<Enter>", self.on_enter)
        btn2.bind("<Leave>", self.on_leave)

        btn3 = tk.Button(button_frame, text="Add Customer", command=self.add_customer, **button_style)
        btn3.pack(pady=5)
        btn3.bind("<Enter>", self.on_enter)
        btn3.bind("<Leave>", self.on_leave)

        btn4 = tk.Button(button_frame, text="View Customers", command=self.view_customers, **button_style)
        btn4.pack(pady=5)
        btn4.bind("<Enter>", self.on_enter)
        btn4.bind("<Leave>", self.on_leave)

        self.root.mainloop()

    def on_enter(self, e):
        e.widget["bg"] = "#43a047"

    def on_leave(self, e):
        e.widget["bg"] = "#2e7d32"

    def add_book(self):

        window = tk.Toplevel(self.root)

        tk.Label(window,text="Title").pack()
        title = tk.Entry(window)
        title.pack()

        tk.Label(window,text="Author").pack()
        author = tk.Entry(window)
        author.pack()

        tk.Label(window,text="Total Copies").pack()
        copies = tk.Entry(window)
        copies.pack()

        def save():
            self.library.add_book(
                title.get(),
                author.get(),
                int(copies.get())
            )
            messagebox.showinfo("Success","Book Added")
            window.destroy()

        tk.Button(window,text="Save",command=save).pack()

    def view_books(self):

        books = self.library.get_all_books()

        window = tk.Toplevel(self.root)

        for book in books:
            text = f"ID:{book[0]} | {book[1]} | {book[2]} | Available:{book[4]}"
            tk.Label(window,text=text).pack()

    def add_customer(self):

        window = tk.Toplevel(self.root)

        tk.Label(window,text="First Name").pack()
        first = tk.Entry(window)
        first.pack()

        tk.Label(window,text="Last Name").pack()
        last = tk.Entry(window)
        last.pack()

        tk.Label(window,text="Phone").pack()
        phone = tk.Entry(window)
        phone.pack()

        def save():
            self.library.add_customer(
                first.get(),
                last.get(),
                phone.get()
            )
            messagebox.showinfo("Success","Customer Added")
            window.destroy()

        tk.Button(window,text="Save",command=save).pack()

    def view_customers(self):

        customers = self.library.get_all_customers()

        window = tk.Toplevel(self.root)

        for c in customers:
            text = f"ID:{c[0]} | {c[1]} {c[2]} | Phone:{c[3]}"
            tk.Label(window,text=text).pack()