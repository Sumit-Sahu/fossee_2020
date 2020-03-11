import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QLineEdit, QGraphicsView, \
    QMenu, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenu, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QStaticText, QColor, QCursor, QBrush, QIcon, QTransform
from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QPointF

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ConnectingLine(QGraphicsLineItem):
    def __init__(self, startPoint, endPoint,parent=None):
        QGraphicsLineItem.__init__(self,startPoint.x(), startPoint.y(), endPoint.x(), endPoint.y(),parent=parent)
        print('s')
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.startCircle = None
        self.endCircle = None

        self.setPen(QPen(Qt.black, 4, Qt.SolidLine))

    def getStartCircle(self):
        return self.startCircle

    def setStartCircle(self, startCircle):
        self.startCircle = startCircle

    def getEndCircle(self):
        return self.endCircle

    def setEndCircle(self, endCircle):
        self.endCircle = endCircle

    def adjust(self, point):
        if self.startCircle and self.endCircle:
            # line = QLineF(self.mapFromItem(self.startCircle, 0, 0),
            #               self.mapFromItem(self.endCircle, 0, 0))

            self.startPoint = self.mapFromItem(self.startCircle, 0, 0)
            self.endPoint = self.mapFromItem(self.endCircle, 0, 0)
        else:
            print('then',point)
            self.endPoint = point
        self.setLine(self.startPoint.x(), self.startPoint.y(),self.endPoint.x(),self.endPoint.y())
