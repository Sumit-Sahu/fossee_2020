import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QLineEdit, QGraphicsView, \
    QMenu, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenu, QGraphicsEllipseItem, QGraphicsLineItem, QAction, \
    QToolButton, QButtonGroup
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor, QCursor, QBrush, QIcon, QTransform
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QPointF, QLineF

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from circle import Circle
from connectingline import ConnectingLine




class CanvasScene(QGraphicsScene):

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # self.top = 100
        # self.left = 900
        # self.width = 1000
        # self.height = 800
        self.title = "Create Circles"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.scene = CanvasScene()
        self.scene.setSceneRect(QRectF(0, 0, 1000, 1000))
        self.createActions()
        self.createToolbars()

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        # self.view.fitInView(self.scene.sceneRect())

    def pointerGroupClicked(self, i):
        Circle.myMode = self.connectionTypeGroup.checkedId()

    def createActions(self):
        self.adAction = QAction("Add", self, shortcut="Ctrl+N", statusTip="Add a new Circle")
        self.adAction.triggered.connect(lambda: self.drawCircle())
        self.generateReportAction = QAction("Generate Report", self, shortcut="Ctrl+G", statusTip="Pdf Report")
        self.saveAction = QAction(
            QIcon('images/bringtofront.png'), "Save",
            self, shortcut="Ctrl+S", statusTip="Save as Image")

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.adAction)
        self.editToolBar.addAction(self.generateReportAction)
        self.editToolBar.addAction(self.saveAction)

        pointerButton = QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QIcon('images/pointer.png'))
        linePointerButton = QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QIcon('images/linepointer.png'))

        self.connectionTypeGroup = QButtonGroup()
        self.connectionTypeGroup.addButton(pointerButton, Circle.MoveItem)
        self.connectionTypeGroup.addButton(linePointerButton, Circle.InsertLine)
        self.connectionTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        self.lineToolbar = self.addToolBar("Pointer type")
        self.lineToolbar.addWidget(linePointerButton)
        self.lineToolbar.addWidget(pointerButton)

    def drawCircle(self):
        radius = 50
        circle = Circle(radius)
        circle.addOnCanvas(self.scene)

    def save_image(self):
        fileName = QFileDialog.getSaveFileName(self, 'caption', "image.png", '*.png')
        pixmap = QPixmap()
        pixmap = self.view.grab(self.rect())
        pixmap.save(fileName[0], 'PNG')


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
