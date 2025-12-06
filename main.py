import sqlite3 as sq3
import pdf2image

db = sq3.connect("database.db")
cu = db.cursor()

def setup():
    cu.execute("""CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100),
                author VARCHAR(100),
                category VARCHAR(100))""")
    db.commit()
def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    category = input("Enter book category: ")
    cu.execute("INSERT INTO book (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    db.commit()
def view_books():
    cu.execute("SELECT * FROM book")
    books = cu.fetchall()
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}")
def delete_book():
    letters = input("Enter the first few letters of the book to delete: ")
    cu.execute("DELETE FROM book WHERE title LIKE ?", (f"{letters}%",))
    db.commit()
    
setup()

while True:
    print("1. Add Book")
    print("2. View Books")
    print("3. Delete Book")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        add_book()
    elif choice == '2':
        view_books()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")