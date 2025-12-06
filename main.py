import mysql.connector as msq
from pdf2image import convert_from_path

db = msq.connect(
    host="localhost",
    user="root",
    password="55362146",
)
cu = db.cursor()

def setup():
    cu.execute("CREATE DATABASE IF NOT EXISTS books")
    cu.execute("USE books")
    cu.execute("""CREATE TABLE IF NOT EXISTS book (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(100),
                author VARCHAR(100),
                category VARCHAR(100))""")
    db.commit()
def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    category = input("Enter book category: ")
    cu.execute("INSERT INTO book (title, author, category) VALUES (%s, %s, %s)", (title, author, category))
    db.commit()
def view_books():
    cu.execute("SELECT * FROM book")
    books = cu.fetchall()
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}")
def delete_book():
    letters = input("Enter the first few letters of the book to delete: ")
    cu.execute("DELETE FROM book WHERE title LIKE %s", (f"{letters}%",))
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