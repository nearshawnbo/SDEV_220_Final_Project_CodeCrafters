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



    #Remove Customer



    #Update Customer



    #Search Book



    # Get all books



    #Get all Customers



    #checkout book





    #Return Book




    #Get active cehckouts





    #Get overdue Books