

import sys, random
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.top = 900
        self.left = 100
        self.width = 1000
        self.height = 800
        self.title = "Create Circles"
        self.InitWindow()

        mainMenu = self.menuBar()
        Add = mainMenu.addMenu("Add")
        Generate_Report = mainMenu.addMenu("Generate_Report")
        Save = mainMenu.addMenu("Save")

        self.shapes = []

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for shape in self.shapes:
            shape.paint(painter)


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)




class Circle():
    def __init__(self):
        self.color = QtGui.QColor(*random.choices(range(256), k=3))
        self.position = QtCore.QPoint(*random.choices(range(800), k=2))
        self.length = random.randrange(200)
        self.textlable=QLabel()

    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  4 , Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawEllipse(x, y, self.length, self.length)
        painter.restore()




if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    for _ in range(20):
        window.shapes.append(Circle())
    window.show()
    sys.exit(App.exec())