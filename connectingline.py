import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsLineItem, QApplication, QGraphicsView, QGraphicsScene, \
    QLineEdit, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QLine, pyqtSignal, QPoint, QPointF, QRectF


class ConnectingLine(QGraphicsLineItem):
    # updateLine = pyqtSignal(QPointF)

    def __init__(self, startPoint, endPoint, parent=None):
        QGraphicsLineItem.__init__(self, startPoint.x(), startPoint.y(), endPoint.x(), endPoint.y(), parent=parent)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.startCircle = None
        self.endCircle = None
        self.textLabel = QGraphicsProxyWidget()
        self.textLabel.setWidget(QLineEdit('CON1'))
        self.textLabel.setParentItem(self)

        self.setPen(QPen(Qt.black, 4, Qt.SolidLine))

    def setStartCircle(self, startCircle):
        self.startCircle = startCircle

    def setEndCircle(self, endCircle):
        self.endCircle = endCircle

    def getStartCircle(self):
        return self.startCircle

    def getEndCircle(self):
        return self.endCircle

    def updateLine(self, point):
        if self.startCircle and self.endCircle:
            item = self.startCircle
            self.startPoint = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                      item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
            item = self.endCircle
            self.endPoint = QPointF(item.sceneBoundingRect().x() + item.sceneBoundingRect().width() / 2.0,
                                    item.sceneBoundingRect().y() + item.sceneBoundingRect().height() / 2.0)
        else:
            self.endPoint = point

        self.setLine(self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y())
        self.textLabel.setGeometry(QRectF(self.boundingRect().x() + self.boundingRect().width() / 2,
                                          self.boundingRect().y() + self.boundingRect().height() / 2,
                                          50, 20))

    def addOnCanvas(self, scene):
        scene.addItem(self)
        scene.addItem(self.textLabel)
