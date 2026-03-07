from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QScrollArea, QComboBox, QTabWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QFileDialog, QPushButton, QFormLayout, QCompleter
from PyQt5.QtCore import QUrl, QStringListModel, Qt
import sys
import re
import main
import requests
import sqlite3 as sq

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
            text = item[1]

            label1 = QLabel(text)
            label1.setAlignment(Qt.AlignCenter)
            label1.setWordWrap(True)
            label1.setMinimumSize(200, 100)

            row = i // columns
            col = i % columns

            grid.addWidget(label1, row, col)

        tab1.setLayout(grid)

        tab2 = QWidget()
        self.tabs.addTab(tab2, "Add Books")

        vbox = QVBoxLayout()
        form = QFormLayout()

        self.name = QLineEdit(placeholderText='Name')
        self.language = 'English'
        self.lang = QComboBox()
        self.lang.addItem('English')
        self.lang.addItem('Arabic')
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
        form.addWidget(self.name)
        form.addWidget(self.lang)
        form.addWidget(self.author)
        form.addWidget(self.cat)
        add = QPushButton()
        add.setText("Add")
        add.clicked.connect(self.appendData)
        form.addWidget(add)
        self.label = QLabel()
        self.label.setText("Press Enter to view suggestions!")
        form.addWidget(self.label)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(form)
        tab2.setLayout(hbox)

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
        main.add_book(title, author, category)
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
