

class Book:
    def __init__(self, title, author, book_id, total_copies):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.total_copies = total_copies
        self.available_copies = total_copies

    def borrow(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []


class Library:
    def __init__(self):
        self.books = {}
        self.borrow_records = {}

    def add_book(self, book):
        self.books[book.book_id] = book

    def search_by_title(self, title):
        return [
            book for book in self.books.values()
            if title.lower() in book.title.lower()
        ]

    def search_by_author(self, author):
        return [
            book for book in self.books.values()
            if author.lower() in book.author.lower()
        ]

    def borrow_book(self, book_id, user_name):
        book = self.books.get(book_id)
        if not book:
            return "Book not found."

        if book.borrow():
            user = self.borrow_records.get(user_name, User(user_name))
            user.borrowed_books.append(book_id)
            self.borrow_records[user_name] = user
            return "Book borrowed successfully."
        return "No copies available."

    def return_book(self, book_id, user_name):
        book = self.books.get(book_id)
        user = self.borrow_records.get(user_name)

        if not book or not user:
            return "Invalid book or user."

        if book_id in user.borrowed_books:
            book.return_book()
            user.borrowed_books.remove(book_id)
            return "Book returned successfully."
        return "This book was not borrowed by the user."