from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel
import sys
import main

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
        category = 

        grid = QGridLayout()   
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(grid)
        cen_widget.setLayout(hbox)

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