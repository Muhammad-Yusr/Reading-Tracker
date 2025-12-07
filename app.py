from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QFileDialog, QPushButton, QFormLayout, QCompleter
from PyQt5.QtCore import QUrl
import sys
import re
import main
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import requests

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(300, 200, 1000, 600)
        self.setWindowTitle("Reading Progress")
        self.initUI()

    def initUI(self):
        cen_widget = QWidget()
        self.setCentralWidget(cen_widget)

        vbox = QVBoxLayout()
        #button = QPushButton(self)
        #button.setText("Open")
        #button.clicked.connect(self.addFile)

        form = QFormLayout()
        name = QLineEdit(placeholderText='Name')
        cat = QLineEdit(placeholderText='Category')
        suggestion_list = []
        suggestions = QCompleter(suggestion_list)
        name.setCompleter(suggestions)
        name.textChanged.connect(self.search)
        form.addWidget(name)
        form.addWidget(cat)
        add = QPushButton()
        add.setText("Add")
        add.clicked.connect(self.appendData)
        form.addWidget(add)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(form)
        cen_widget.setLayout(hbox)
    def search(self, text):
        url = "https://openlibrary.org/search.json"
        text = text.replace(" ", "+")
        req = f"{url}?q={text}"
        response = requests.get(req)
        if response.status_code == 200:
            print(response.json()["docs"][0]["title"])

    def appendData(self):
        pass

    #def addFile(self):
    #    dialog = QFileDialog.getOpenFileUrl(self, "Select PDF File", QUrl(), "PDF (*.pdf)")
    #    rawurl = str(dialog[0]).split("(")
    #    path = rawurl[1].replace("file:///", "")
    #    path = path.replace(")", "")
    #    path = path.replace("'", "")
    #    file = open(path, 'rb')
    #    parser = PDFParser(file)
    #    doc = PDFDocument(parser)
    #    print(doc.info)

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