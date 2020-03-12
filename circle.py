import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QLineEdit, QGraphicsView, \
    QMenu, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenu, QGraphicsEllipseItem, QGraphicsLineItem, QAction, \
    QToolButton, QButtonGroup
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor, QCursor, QBrush, QIcon, QTransform
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QPointF, QLineF

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from connectingline import ConnectingLine


class Circle(QGraphicsEllipseItem):
    MoveItem, InsertLine = 1, 2
    myMode = MoveItem

    def __init__(self, radius, parent=None):
        position = QtCore.QPoint(*random.choices(range(800), k=2))
        x_coordinate, y_coordinate = position.x(), position.y()
        QGraphicsEllipseItem.__init__(self, QRectF(x_coordinate, y_coordinate, 2 * radius, 2 * radius), parent=parent)
        self.setZValue(1)
        # self.scene.moveCircle.connect(self.mouseMoveEvent)
        self.line = None
        self.color = QColor(*random.choices(range(256), k=3))
        self.setPen(QPen(self.color, 4, Qt.SolidLine))

        self.setFlags(QGraphicsItem.ItemIsMovable)

        self.connectlines = {}

    def setMode(self, mode):
        Circle.myMode = mode

    def contextMenuEvent(self, event):
        contextMenu = QMenu()
        deleteAction = contextMenu.addAction("Delete")
        quitAction = contextMenu.addAction("Exit")
        # connectAction = contextMenu.addAction("Connect With")
        action = contextMenu.exec_(event.screenPos())
        if action == deleteAction:

            self.scene().removeItem(self)
        if action == quitAction:
            self.window().close()
        # if action == connectAction:
        #     self.connect()

    def addOnCanvas(self, scene):
        scene.addItem(self)
        textLabel = scene.addWidget(QLineEdit('cirA'))
        textLabel.setParentItem(self)
        textLabel.setGeometry(
            QRectF(self.rect().x() + self.rect().width() / 4, self.rect().y() - self.pen().width() - 10, 50, 10))

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != Qt.LeftButton:
            return

        if Circle.myMode == Circle.InsertLine:
            item = self
            if type(item) == Circle:
                startPoint = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                     item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
                endPoint = mouseEvent.scenePos()
                self.line = ConnectingLine(startPoint, endPoint)
                self.scene().addItem(self.line)
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if Circle.myMode == Circle.InsertLine and self.line:
            self.line.updateLine(mouseEvent.scenePos())
        if Circle.myMode == Circle.MoveItem:
            super().mouseMoveEvent(mouseEvent)
            for line in self.connectlines.values() :
                line.updateLine(mouseEvent.scenePos())

    def mouseReleaseEvent(self, mouseEvent):
        if Circle.myMode == Circle.InsertLine and self.line:
            item = self.scene().itemAt(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), self.transform())

            if type(item) == Circle and item != self and not item in self.connectlines:
                point = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
                self.line.updateLine(point)
                self.connectlines[item]=self.line
                item.connectlines[self]=self.line
                self.line.setStartCircle(self)
                self.line.setEndCircle(item)
            else:
                self.scene().removeItem(self.line)

        self.line = None
        super(Circle, self).mouseReleaseEvent(mouseEvent)
