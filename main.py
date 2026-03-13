import sqlite3 as sq3

db = sq3.connect("database.db")
cu = db.cursor()

def setup():
    cu.execute("""CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100),
                author VARCHAR(100),
                category VARCHAR(100),
                completion INTEGER)""")
    db.commit()
def add_book(title, author, category, completion):
    cu.execute("INSERT INTO book (title, author, category, completion) VALUES (?, ?, ?, ?)", (title, author, category, completion))
    db.commit()
def view_books():
    cu.execute("SELECT * FROM book")
    books = cu.fetchall()
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}, Completion: {book[4]}")
def fetch_books():
    cu.execute("SELECT * FROM book ORDER BY completion")
    books = cu.fetchall()
    return books
def delete_book():
    letters = input("Enter the first few letters of the book to delete: ")
    cu.execute("DELETE FROM book WHERE title LIKE ?", (f"{letters}%",))
    db.commit()

setup()