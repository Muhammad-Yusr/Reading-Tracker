from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QScrollArea, QComboBox, QMenu, QTabWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QFileDialog, QPushButton, QFormLayout, QCompleter
from PyQt5.QtCore import QUrl, QStringListModel, Qt
import sys
import re
import main
import requests
import sqlite3 as sq

db = sq.connect("database.db")
cu = db.cursor()
cu.execute("""CREATE TABLE IF NOT EXISTS covers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id FOREIGN KEY """)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(300, 200, 1000, 600)
        self.setWindowTitle("Reading Progress")
        self.initUI()

    def initUI(self):
        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)

        main_layout = QVBoxLayout(cen_widget)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        tab1 = QWidget()
        self.tabs.addTab(tab1, "My Books")

        tab1_layout = QVBoxLayout(tab1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tab1_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        grid = QGridLayout(content)
        grid.setSpacing(10)
        columns = 3

        for i, item in enumerate(main.fetch_books()):
            id = item[0]
            text1 = item[1]
            text2 = item[2]
            list1 = ["Planning to read", "Reading", "Completed"]
            text3 = list1[int(item[4])]

            book_widget = QWidget()
            book_layout = QVBoxLayout(book_widget)

            label1 = QLabel(text1)
            label1.setAlignment(Qt.AlignCenter)
            label1.setWordWrap(True)
            label1.setMinimumSize(200, 100)

            label2 = QLabel(text2)
            label2.setAlignment(Qt.AlignTop)
            label2.setWordWrap(True)
            label2.setMinimumSize(200, 100)

            label3 = QLabel(text3)
            label3.setAlignment(Qt.AlignBottom)
            label3.setWordWrap(True)
            label3.setMinimumSize(200, 100)

            book_layout.addWidget(label2)
            book_layout.addWidget(label1)
            book_layout.addWidget(label3)

            book_widget.setProperty("book_id", id)
            book_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            book_widget.customContextMenuRequested.connect(
                lambda pos, w=book_widget: self.show_context_menu(pos, w)
            )

            row = i // columns
            col = i % columns
            grid.addWidget(book_widget, row, col)

        tab2 = QWidget()
        self.tabs.addTab(tab2, "Add Books")

        vbox = QVBoxLayout()
        form = QFormLayout()

        self.name = QLineEdit(placeholderText='Name')
        self.language = 'English'
        self.lang = QComboBox()
        self.lang.addItems(['English', 'Arabic'])
        self.lang.activated.connect(self.setLang) 
        self.cat = QLineEdit(placeholderText='Category')
        self.author = QLineEdit(placeholderText='Author')
        self.suggestion_list = []
        self.model = QStringListModel(self.suggestion_list)
        self.suggestions = QCompleter()
        self.suggestions.setModel(self.model)
        self.suggestions.setCompletionMode(QCompleter.PopupCompletion)
        self.suggestions.setCaseSensitivity(Qt.CaseInsensitive)
        self.name.setCompleter(self.suggestions)
        self.name.returnPressed.connect(self.search)
        self.completion = QComboBox()
        self.completion.addItems(["Planning to read", "Reading", "Completed"])
        form.addWidget(self.name)
        form.addWidget(self.lang)
        form.addWidget(self.author)
        form.addWidget(self.cat)
        form.addWidget(self.completion)
        add = QPushButton()
        add.setText("Add")
        add.clicked.connect(self.appendData)
        form.addWidget(add)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(form)
        tab2.setLayout(hbox)

    def show_context_menu(self, pos, widget):
            book_id = widget.property("book_id")
            menu = QMenu()

            addcover = menu.addAction("Edit Cover")
            del_book = menu.addAction("Delete Book")

            action = menu.exec_(widget.mapToGlobal(pos))

            if action == addcover:
                pass
            elif action == del_book:
                pass


    def setLang(self, _):
        self.language = self.lang.currentText()

    def search(self):
        url = "https://openlibrary.org/search.json"
        text = self.name.text().replace(" ", "+")
        lang = 'en'
        if self.language == 'English':
            lang = 'en'
        elif self.language == 'Arabic':
            lang = 'ar'
        req = f"{url}?q={text}&lang={lang}"
        response = requests.get(req)
        if response.status_code == 200:
            for i in range(5):
                title = response.json()["docs"][i]["title"]
                if not title:
                    break
                self.suggestion_list.append(title)
            self.model.setStringList(self.suggestion_list)
            self.suggestions.complete()

    def appendData(self):
        title = self.name.text()
        author = self.author.text()
        category = self.cat.text()
        completion = self.completion.currentIndex()
        main.add_book(title, author, category, completion)
        self.initUI()

    def changeText(self):
        self.label.setText("Label2")
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

window()
