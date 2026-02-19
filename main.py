from database import initialize_database, add_book, create_customer, log_checkout, log_return, get_book_by_id

# Initialize database tables
initialize_database()

# Sample workflow
print("=== Library System Demo ===")

# Add a book
add_book("1984", "George Orwell", 5)
add_book("To Kill a Mockingbird", "Harper Lee", 3)

# Add a customer
create_customer("John", "Doe", "555-1234")

# Checkout a book
log_checkout(1, 1, "2026-02-19", "2026-03-05")
print("Checked out book 1 to customer 1")

# Return a book
log_return(1, "2026-02-25")
print("Returned checkout 1")

# Query a book
book = get_book_by_id(1)
print("Book info:", book)
