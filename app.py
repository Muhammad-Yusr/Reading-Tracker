from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QPushButton
from PyQt5.QtCore import QUrl
import sys
import re
import main
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

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
        button = QPushButton(self)
        button.setText("Open")
        button.clicked.connect(self.addFile)
        grid = QGridLayout()   
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        vbox.addWidget(button)
        hbox.addLayout(grid)
        cen_widget.setLayout(hbox)

    def addFile(self):
        dialog = QFileDialog.getOpenFileUrl(self, "Select PDF File", QUrl(), "PDF (*.pdf)")
        rawurl = str(dialog[0]).split("(")
        path = rawurl[1].replace("file:///", "")
        path = path.replace(")", "")
        path = path.replace("'", "")
        file = open(path, 'rb')
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        print(doc.info)

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