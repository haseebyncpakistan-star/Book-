

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
        return "This book was not borrowed by the user.".py

import streamlit as st
from book import Book, Library

st.set_page_config(page_title="Digital Library System", layout="centered")

st.title("Digital Library System")

# Keep library persistent
if "library" not in st.session_state:
    st.session_state.library = Library()

library = st.session_state.library

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Book",
        "Search by Title",
        "Search by Author",
        "Borrow Book",
        "Return Book",
        "View All Books"
    ]
)

if menu == "Add Book":
    st.header("Add New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    book_id = st.text_input("Book ID")
    copies = st.number_input("Total Copies", min_value=1, step=1)

    if st.button("Add Book"):
        if book_id in library.books:
            st.error("Book ID already exists.")
        else:
            library.add_book(Book(title, author, book_id, copies))
            st.success("Book added successfully.")

elif menu == "Search by Title":
    st.header("Search by Title")
    title = st.text_input("Enter title")

    if st.button("Search"):
        results = library.search_by_title(title)
        if results:
            for book in results:
                st.write(
                    f"**{book.title}** | {book.author} | "
                    f"{book.available_copies}/{book.total_copies} available"
                )
        else:
            st.warning("No books found.")

elif menu == "Search by Author":
    st.header("Search by Author")
    author = st.text_input("Enter author")

    if st.button("Search"):
        results = library.search_by_author(author)
        if results:
            for book in results:
                st.write(
                    f"**{book.title}** | {book.author} | "
                    f"{book.available_copies}/{book.total_copies} available"
                )
        else:
            st.warning("No books found.")

elif menu == "Borrow Book":
    st.header("Borrow Book")

    book_id = st.text_input("Book ID")
    user_name = st.text_input("Your Name")

    if st.button("Borrow"):
        message = library.borrow_book(book_id, user_name)
        if "successfully" in message:
            st.success(message)
        else:
            st.error(message)

elif menu == "Return Book":
    st.header("Return Book")

    book_id = st.text_input("Book ID")
    user_name = st.text_input("Your Name")

    if st.button("Return"):
        message = library.return_book(book_id, user_name)
        if "successfully" in message:
            st.success(message)
        else:
            st.error(message)

elif menu == "View All Books":
    st.header("Library Books")

    if not library.books:
        st.info("No books available.")
    else:
        for book in library.books.values():
            st.write(
                f"**ID:** {book.book_id} | "
                f"**Title:** {book.title} | "
                f"**Author:** {book.author} | "
                f"**Available:** {book.available_copies}/{book.total_copies}"
            )