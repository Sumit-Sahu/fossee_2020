import sys, random

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtPrintSupport import QPrinter
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

    def pointerGroupClicked(self, i):
        Circle.myMode = self.connectionTypeGroup.checkedId()

    def createActions(self):
        self.addAction = QAction(QIcon('images/bringtofront.png'),
                                 "Add", self, shortcut="Ctrl+N")
        self.addAction.triggered.connect(self.drawCircle)

        self.generateReportAction = QAction(QIcon('images/bringtofront.png'),
                                            "Generate Report", self, shortcut="Ctrl+G")
        self.generateReportAction.triggered.connect(self.saveAsPdf)

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

    def saveAsPng(self):
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save file', "image.png", '*.png')
            if not fileName:
                return
            if QFileInfo(fileName).suffix() != '.png':  # check if user type other extension with name
                fileName += '.png'
            pixmap = self.view.grab()
            pixmap.save(fileName, 'PNG')
        except:
            QMessageBox.information(self,'Error','Image not saved')

    def saveAsPdf(self):
        try:
            from reportlab.pdfgen.canvas import Canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.lib.colors import red, blue

        except:
            QMessageBox.information(self, 'Alert', 'Process Declined \n import reportlab')



        items = self.scene.items()
        fileName, _ = QFileDialog.getSaveFileName(self, directory='file.pdf',
                                                  filter='PDF Files *.pdf(*.pdf);;All Files *(*)')
        if not fileName:
            return
        print(QFileInfo(fileName).suffix())
        if QFileInfo(fileName).suffix() != 'pdf':                                            # check if user type other extension with name
            fileName += '.pdf'

        canvas = Canvas(fileName, pagesize=A4)
        canvas.setFont("Times-Roman", 30)
        canvas.setFillColor(red)
        canvas.drawCentredString(4 * inch, 11 * inch, "Connection Report")
        canvas.setFillColor(blue)
        size = 20
        y = 10 * inch
        x = 2 * inch
        line = 1
        for item in items:
            if type(item) == ConnectingLine:
                connectionLine = item.textLabel.text()
                startCircle = item.getStartCircle().textLabel.text()
                endCircle = item.getEndCircle().textLabel.text()
                str = "{}:({},{})".format(connectionLine, startCircle, endCircle)

                if line > 20:
                    canvas.showPage()
                    line = 4
                    size = 7
                    y = 10 * inch
                    x = 2 * inch

                canvas.setFont("Helvetica", size)
                canvas.drawString(x, y, str)
                line += 1
                y = y - size * 2

        try:
            canvas.save()
        except:
            QMessageBox.information(self, 'Error', 'Error Generating Report \n'
                                                   'first close file {}'.format(fileName))


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
