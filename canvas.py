from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QMenu, QGraphicsView

from connectingline import ConnectingLine
from circle import Circle


class Canvas(QGraphicsScene):
    MoveItem, InsertLine = 1, 2
    myMode = MoveItem

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.lines = []
        self.circles = []

    def setMode(self, mode):
        Canvas.myMode = mode

    def contextMenuEvent(self, event):
        contextMenu = QMenu()
        deleteCircleAction = contextMenu.addAction("Delete All Circle")
        clearConnectionAction = contextMenu.addAction("Delete All Connection")
        quitAction = contextMenu.addAction("Exit Application")
        clearConnectionAction.triggered.connect(self.clearAllConnection)
        action = contextMenu.exec_(event.screenPos())
        if action == deleteCircleAction:
            circle = self.items()
            for item in circle:
                self.removeItem(item)
        if action == quitAction:
            self.window().close()

    def clearAllConnection(self):
        items = self.items()
        for item in items:
            if type(item) == ConnectingLine:
                item.removeFromCanvas()

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != Qt.LeftButton:
            return

        if Canvas.myMode == Canvas.InsertLine:
            circles = self.selectedItems()
            for circle in circles:
                if type(circle) == Circle:
                    startPoint = circle.getCenter()
                    endPoint = mouseEvent.scenePos()
                    line = ConnectingLine(startPoint, endPoint)
                    line.addOnCanvas(self)
                    self.circles.append(circle)
                    self.lines.append(line)

        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if Canvas.myMode == Canvas.InsertLine and self.lines:
            for line in self.lines:
                line.updateLine(mouseEvent.scenePos())

        if Canvas.myMode == Canvas.MoveItem:
            circles = self.selectedItems()
            for circle in circles:
                circle.mouseMoveEvent(mouseEvent)
                if type(circle) == Circle:
                    for line in circle.getLines():
                        line.updateLine(mouseEvent.scenePos())
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if Canvas.myMode == Canvas.InsertLine and self.lines:
            item = self.itemAt(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), Circle().transform())
            lines = self.lines
            circles = self.circles
            if type(item) == Circle:
                point = item.getCenter()
                for circle, line in zip(circles, lines):
                    if item != circle and item not in circle.connectedCircle:
                        line.updateLine(point)
                        circle.addConnection(item, line)
                        item.addConnection(circle, line)
                        line.setStartCircle(circle)
                        line.setEndCircle(item)
                    else:
                        line.removeFromCanvas()
            else:
                for line in lines:
                    line.removeFromCanvas()
            item.clearFocus()

        self.lines.clear()
        self.circles.clear()
        super(Canvas, self).mouseReleaseEvent(mouseEvent)
