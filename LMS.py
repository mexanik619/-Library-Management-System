from datetime import datetime, timedelta
from enum import Enum
import uuid

class BookStatus(Enum):
    AVAILABLE = "Available"
    ISSUED = "Issued"
    RESERVED = "Reserved"
    LOST = "Lost"
    DAMAGED = "Damaged"

class Book:
    def __init__(self, title, author, isbn, publication_year, category):
        self.book_id = str(uuid.uuid4())[:8]
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.category = category
        self.status = BookStatus.AVAILABLE
        self.issued_to = None
        self.issue_date = None
        self.return_date = None
    
    def __str__(self):
        return f"{self.title} by {self.author} [{self.isbn}] - {self.status.value}"

class Member:
    def __init__(self, name, email, address, phone):
        self.member_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        self.date_joined = datetime.now()
        self.books_issued = []
        self.fine_amount = 0
    
    def issue_book(self, book):
        if book.status == BookStatus.AVAILABLE:
            book.status = BookStatus.ISSUED
            book.issued_to = self.member_id
            book.issue_date = datetime.now()
            book.return_date = datetime.now() + timedelta(days=14)  # 2 weeks loan period
            self.books_issued.append(book.book_id)
            return True
        return False
    
    def return_book(self, book, library):
        if book.book_id in self.books_issued and book.status == BookStatus.ISSUED:
            self.books_issued.remove(book.book_id)
            book.status = BookStatus.AVAILABLE
            book.issued_to = None
            
            # Calculate fine if returned late
            if datetime.now() > book.return_date:
                days_late = (datetime.now() - book.return_date).days
                fine = days_late * library.fine_per_day
                self.fine_amount += fine
                book.issue_date = None
                book.return_date = None
                return fine
            
            book.issue_date = None
            book.return_date = None
            return 0
        return None
    
    def pay_fine(self, amount):
        if amount <= self.fine_amount:
            self.fine_amount -= amount
            return True
        return False
    
    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - Books issued: {len(self.books_issued)}, Fine: ${self.fine_amount}"

class Librarian:
    def __init__(self, name, employee_id, email):
        self.name = name
        self.employee_id = employee_id
        self.email = email
        self.date_joined = datetime.now()
    
    def add_book(self, library, title, author, isbn, publication_year, category):
        book = Book(title, author, isbn, publication_year, category)
        return library.add_book(book)
    
    def remove_book(self, library, book_id):
        return library.remove_book(book_id)
    
    def register_member(self, library, name, email, address, phone):
        member = Member(name, email, address, phone)
        return library.add_member(member)
    
    def remove_member(self, library, member_id):
        return library.remove_member(member_id)
    
    def issue_book_to_member(self, library, book_id, member_id):
        book = library.find_book(book_id)
        member = library.find_member(member_id)
        
        if book and member:
            if member.issue_book(book):
                return True
        return False
    
    def return_book_from_member(self, library, book_id, member_id):
        book = library.find_book(book_id)
        member = library.find_member(member_id)
        
        if book and member:
            fine = member.return_book(book, library)
            if fine is not None:
                return fine
        return None
    
    def collect_fine(self, library, member_id, amount):
        member = library.find_member(member_id)
        if member:
            return member.pay_fine(amount)
        return False
    
    def __str__(self):
        return f"Librarian: {self.name} (ID: {self.employee_id})"

class Library:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = {}
        self.members = {}
        self.librarians = {}
        self.fine_per_day = 1.0  # $1 per day for late returns
    
    def add_book(self, book):
        self.books[book.book_id] = book
        return book.book_id
    
    def remove_book(self, book_id):
        if book_id in self.books:
            book = self.books[book_id]
            if book.status == BookStatus.AVAILABLE:
                del self.books[book_id]
                return True
        return False
    
    def find_book(self, book_id):
        return self.books.get(book_id)
    
    def search_books(self, keyword):
        results = []
        for book in self.books.values():
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword.lower() in book.isbn.lower() or
                keyword.lower() in book.category.lower()):
                results.append(book)
        return results
    
    def add_member(self, member):
        self.members[member.member_id] = member
        return member.member_id
    
    def remove_member(self, member_id):
        if member_id in self.members:
            member = self.members[member_id]
            if not member.books_issued:
                del self.members[member_id]
                return True
        return False
    
    def find_member(self, member_id):
        return self.members.get(member_id)
    
    def add_librarian(self, librarian):
        self.librarians[librarian.employee_id] = librarian
        return librarian.employee_id
    
    def generate_report_overdue_books(self):
        overdue_books = []
        today = datetime.now()
        
        for book in self.books.values():
            if book.status == BookStatus.ISSUED and book.return_date < today:
                member = self.members.get(book.issued_to)
                days_late = (today - book.return_date).days
                fine = days_late * self.fine_per_day
                overdue_books.append({
                    'book': book,
                    'member': member,
                    'days_late': days_late,
                    'fine': fine
                })
        
        return overdue_books
    
    def generate_report_popular_books(self):
        # This would require tracking book issue history
        # For now, we'll just return a placeholder
        return "Report functionality would track most frequently issued books"
    
    def __str__(self):
        return f"{self.name} Library - Books: {len(self.books)}, Members: {len(self.members)}"


# Demo usage
if __name__ == "__main__":
    # Create a library
    city_library = Library("City Central Library", "123 Main St, Cityville")
    
    # Create a librarian
    head_librarian = Librarian("John Smith", "EMP001", "john@library.com")
    city_library.add_librarian(head_librarian)
    
    # Add books
    book1_id = head_librarian.add_book(city_library, "Python Programming", "Palak Chauhan", "978-1234567890", 2020, "Programming")
    book2_id = head_librarian.add_book(city_library, "Data Structures", "Jane Smith", "978-0987654321", 2019, "Computer Science")
    book3_id = head_librarian.add_book(city_library, "Machine Learning Basics", "Alice Johnson", "978-5678901234", 2021, "AI")
    
    # Register members
    member1_id = head_librarian.register_member(city_library, "Bob Wilson", "bob@example.com", "456 Park Ave", "555-1234")
    member2_id = head_librarian.register_member(city_library, "Sarah Brown", "sarah@example.com", "789 Oak St", "555-5678")
    
    # Issue books
    head_librarian.issue_book_to_member(city_library, book1_id, member1_id)
    head_librarian.issue_book_to_member(city_library, book2_id, member2_id)
    
    # Print status
    print(city_library)
    print(city_library.find_book(book1_id))
    print(city_library.find_book(book2_id))
    print(city_library.find_member(member1_id))
    
    # Return a book
    fine = head_librarian.return_book_from_member(city_library, book1_id, member1_id)
    print(f"Fine for returned book: ${fine}")
    
    # Search for books
    results = city_library.search_books("Programming")
    print(f"Search results for 'Programming': {len(results)} books found")
    for book in results:
        print(f"- {book}")