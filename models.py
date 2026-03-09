import database
class Book:
    def  __init__(self, book_id, title, author, total_copies, available_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies
    
    def is_available(self):
        if self.available_copies > 0:
            return True
        else:
            return False
        
    def get_info(self):
        return self.book_id, self.title, self.author, self.available_copies, self.total_copies
    
class Customer:
    def __init__(self, customer_id, first_name, last_name, phone_number):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def get_info(self):
        return self.customer_id, self.first_name, self.last_name, self.phone_number
    
    def get_overdue_books(self):
        return database.get_overdue_books_by_customer(self.customer_id)
    
class Library:
    def __init__(self):
        self.books = []
        self.books_by_id = {}
        self.customers = []
        self.book_fields = ("book_id", "title", "author", "total_copies", "available_copies")
        self.customer_fields = ("customer_id", "first_name", "last_name", "phone")

    def add_book(self,title,author,total_copies):
        database.add_book(title, author, total_copies,)
        data = database.search_book(title=title)[0]
        book = Book(data[0], data[1], data[2], data[3], data[4])
        self.books.append(book)
        self.books_by_id[book.book_id] = book
       
    def remove_book(self, book_id):
        database.delete_book(book_id)
        self.books.remove(self.books_by_id[book_id])
        del self.books_by_id[book_id]

    def update_book(self, book_id, title, author, total_copies):
        database.update_book(title, author, total_copies, book_id)
        existing_book = self.books_by_id[book_id]
        existing_book.title = title
        existing_book.author = author
        existing_book.total_copies = total_copies



    #Add Customer
    def add_customer (self, first_name, last_name, phone):
        database.create_customer(first_name, last_name, phone)

    #Remove Customer
    def remove_customer (self, customer_id):
        database.delete_customer(customer_id)

    #Update Customer
    def update_customer (self, first_name, last_name, phone, customer_id):
        database.update_customer(first_name, last_name, phone, customer_id)



    #Search Book
    def search_book(self, title=None, book_id=None, author=None):
        return database.search_book(title=title, book_id=book_id, author=author)

    # Get all books
    def get_all_books(self):
        return database.get_all_books()

    #Get all Customers
    def get_all_customers(self):
        return database.get_all_customers()

    #checkout book
    def checkout_book (self, book_id, customer_id, checkout_date, due_date):
        database.log_checkout(book_id, customer_id, checkout_date, due_date)
        existing_book = self.books_by_id[book_id]
        existing_book.available_copies = existing_book.available_copies - 1


    #Return Book
    def return_book (self, checkout_id, return_date, book_id):
        database.log_return(checkout_id, return_date)
        existing_book = self.books_by_id[book_id]
        existing_book.available_copies = existing_book.available_copies + 1


    #Get active cehckouts
    def get_active_checkouts (self):
        return database.get_active_checkouts()

    #Get overdue Books
    def get_overdue_books (self):
        return database.get_overdue_books()
    
    # Load Books
    def load_books(self):
        all_books = database.get_all_books()
        for data in all_books:
            book = Book(data[0], data[1], data[2], data[3], data[4])
            self.books.append(book)
            self.books_by_id[book.book_id] = book
        self.load_books