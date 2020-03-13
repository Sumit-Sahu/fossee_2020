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
        self.title = "Create Circles"
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)

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
        self.addAction = QAction(QIcon('images/bringtofront.png'),
                                 "Add", self, shortcut="Ctrl+N")
        self.addAction.triggered.connect(self.drawCircle)

        self.generateReportAction = QAction(QIcon('images/bringtofront.png'),
                                            "Generate Report", self, shortcut="Ctrl+G")
        self.generateReportAction.triggered.connect(self.drawCircle)

        self.saveAction = QAction(QIcon('images/bringtofront.png'),
                                  "Save", self, shortcut="Ctrl+G")
        self.saveAction.triggered.connect(self.saveAsPng)

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.addAction)
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
        circle = Circle()
        circle.addOnCanvas(self.scene)
        # self.scene.addItem(circle)
        # circle.textLabel = self.scene.addWidget(QLineEdit('cirA'))
        # circle.textLabel.setParentItem(circle)
        # circle.textLabel.setGeometry(QRectF(circle.rect().x() + circle.rect().width() / 4,
        #                                     circle.rect().y() - circle.pen().width() - 20,
        #                                     50, 20))


    def saveAsPng(self):
        fileName,_ = QFileDialog.getSaveFileName(self, 'Save file', "image.png", '*.png')
        pixmap = QPixmap()
        pixmap = self.view.grab()
        pixmap.save(fileName, 'PNG')


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
