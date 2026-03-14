from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QScrollArea, QComboBox, QMenu, QTabWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QFileDialog, QPushButton, QFormLayout, QCompleter
from PyQt5.QtCore import QUrl, QStringListModel, Qt
from PyQt5.QtGui import QIcon
import sys
import re
import main
import requests
import sqlite3 as sq
import cv2
import os
import random

if not os.path.exists("images"):
    os.makedirs("images")

db = sq.connect("database.db")
cu = db.cursor()
cu.execute("""CREATE TABLE IF NOT EXISTS covers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                path VARCHAR(256),
                FOREIGN KEY(book_id) REFERENCES book(id))""")
db.commit()
cu.execute("""SELECT * FROM covers""")
print(cu.fetchall())


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle("ReadSet")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(1000, 600)
        self.initUI()
        

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #1e1e2e;
            }
        """)

        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)
        cen_widget.setStyleSheet("""
            background-color: #181825;
            color: #eff1f5;
        """)

        main_layout = QVBoxLayout(cen_widget)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.tabs.setTabShape(QTabWidget.Rounded)
        self.tabs.tabBar().setDocumentMode(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px transparent;
                top: -1;
                background-color: #1e1e2e;
            }
            QTabBar::tab {
				font-family: "JetBrains Mono", monospace;
                font-size: 15px;
                font-weight: 600; 
				background: #1e1e2e;
                padding: 8px;
                min-height: 20px;
                border-radius: 7px;
                margin-right: 3px;
                margin-left: 3px;
            }
            QTabBar::tab:hover {
				background: #313244;
            }         
        """)

        tab1 = QWidget()
        self.tabs.addTab(tab1, "My Books")

        tab1_layout = QVBoxLayout(tab1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tab1_layout.addWidget(scroll)
        scroll.setStyleSheet("""
			border: 1px transparent;
		""")

        content = QWidget()
        scroll.setWidget(content)

        grid = QGridLayout(content)
        grid.setSpacing(10)
        columns = 3

        for i, item in enumerate(main.fetch_books()):
            id = item[0]
            text1 = item[1]
            text2 = item[2]
            list1 = ["Reading", "Planning to read", "Completed"]
            text3 = list1[int(item[4])]

            book_widget = QWidget()
            book_layout = QVBoxLayout(book_widget)
            book_widget.setMinimumHeight(400)

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
            
            for label in [label1, label2, label3]:
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(12)
                shadow.setOffset(2, 2)
                shadow.setColor(Qt.black)
                label.setGraphicsEffect(shadow)
                label.setStyleSheet("""
                    background: transparent;
                    font-size: 20px;
                    font-weight: 800;
                    font-family: "JetBrains Mono", monospace;
                """)

            cu.execute("SELECT path FROM covers WHERE book_id = ?", (id,))
            result = cu.fetchone()
            path = result[0] if result and result[0] else ""
            save_path = f"images/{text1.replace(' ', '')}.jpg"
            if path:
                clean_path = path.replace("\\", "/")
                if not os.path.exists(save_path):
                    img = cv2.imread(clean_path, 1)
                    img = cv2.resize(img, (300, 400))
                    img_name = f"{text1.replace(' ', '')}.jpg"
                    img_path = f"images/{img_name}"
                    cv2.imwrite(img_path, img)
                book_widget.setStyleSheet(f"""
                    QWidget {{
                        background-image: url({save_path});
                        background-repeat: no-repeat;
                        background-position: center;
                        border-radius: 5px;
                    }}
                    QLabel {{
                        font-size: 20px;
                        font-weight: 800;
                        font-family: "JetBrains Mono", monospace;
                        margin: 2px;
                    }}
                """)

            book_layout.addWidget(label2)
            book_layout.addWidget(label1)
            book_layout.addWidget(label3)

            if os.path.exists(save_path):
                book_layout.removeWidget(label1)

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
        self.completion.addItems(["Reading", "Planning to read", "Completed"])
        form.addWidget(self.name)
        form.addWidget(self.lang)
        form.addWidget(self.author)
        form.addWidget(self.cat)
        form.addWidget(self.completion)
        button_container = QHBoxLayout()
        add = QPushButton()
        add.setText("Add")
        add.clicked.connect(self.appendData)
        button_container.addStretch()
        button_container.addWidget(add)
        button_container.addStretch()
        form.addRow(button_container)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(form)
        tab2.setLayout(hbox)
        
        for i in [self.name, self.lang, self.author, self.cat, self.completion]:
            i.setStyleSheet("""border: 0.5px solid #7f849c; padding: 2px; font-size: 15px; font-weight: 100; font-family: "JetBrains Mono", monospace;""")
        add.setStyleSheet("""
            QPushButton {
				border: 0.5px solid #6c7086;
                padding: 4px 10px 4px 10px;
                font-size: 20px;
                font-weight: 600;
                font-family: "JetBrains Mono", monospace;
                border-radius: 7px;
            }
            QPushButton:hover {
                background: #313244;
			}"""
		)
        self.completion.setStyleSheet("""
            border: 0.5px solid #6c7086;
            padding: 2px 2px 2px 4px;
            font-size: 15px;
            font-weight: 100;
            font-family: "JetBrains Mono", monospace;
        """)
        self.lang.setStyleSheet("""
            border: 0.5px solid #6c7086;
            padding: 2px 2px 2px 4px;
            font-size: 15px;
            font-weight: 100;
            font-family: "JetBrains Mono", monospace;
        """)

    def show_context_menu(self, pos, widget):
            book_id = widget.property("book_id")
            menu = QMenu()

            addcover = menu.addAction("Edit Cover")
            del_book = menu.addAction("Delete Book")

            action = menu.exec_(widget.mapToGlobal(pos))

            if action == addcover:
                cu.execute("SELECT * FROM covers WHERE book_id = ?", (book_id,))
                dialog = QFileDialog.getOpenFileName(
                        caption = "Select Book Cover",
                        directory = "./",
                        filter="Images (*.png *.jpg *.jpeg)"
                    )
                if not cu.fetchone():
                    cu.execute("INSERT INTO covers (book_id, path) values (?, ?)", (book_id, dialog[0]))
                else:
                    cu.execute("SELECT title FROM book WHERE id = ?", (book_id,))
                    text1 = cu.fetchone()[0]
                    save_path = f"images/{text1.replace(' ', '')}.jpg"
                    os.remove(save_path)
                    cu.execute("UPDATE covers SET path = ?", (dialog[0],))
                db.commit()
                self.initUI()
            elif action == del_book:
                cu.execute("DELETE FROM book WHERE id = ?", (book_id,))
                cu.execute("DELETE FROM covers WHERE book_id = ?", (book_id,))
                db.commit()
                self.initUI()


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
