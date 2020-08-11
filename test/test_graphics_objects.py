from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsGridLayout, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsObject
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor
from PyQt5.QtCore import Qt, QLineF, QRectF


class SudokuItem(QGraphicsObject):
    def __init__(self, parent=None):
        super(QGraphicsObject, self).__init__(parent=parent)

        self.setParent(parent)
        self.parent = parent

class Board(SudokuItem):

    height = 270.0
    width = 270.0

    def __init__(self):
        super().__init__()

        self.grid = Grid(self)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(0, 0, self.width, self.height)

        lines = [QLineF(self.width * (1 / 3), 0, self.width * (1 / 3), self.height),
                 QLineF(self.width * (2 / 3), 0, self.width * (2 / 3), self.height),
                 QLineF(0, self.height * (1 / 3), self.width, self.height * (1 / 3)),
                 QLineF(0, self.height * (2 / 3), self.width, self.height * (2 / 3))]

        for line in lines:
            painter.drawLine(line)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)


class Grid(SudokuItem):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.number_items = []

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        for i in range(9):
            row = []
            for j in range(9):
                x = (self.parent.width / 9) * i
                y = (self.parent.height / 9) * j
                width = self.parent.width / 9
                height = self.parent.height / 9
                rect = QRectF(x, y, width, height)
                painter.drawRect(rect)
                row.append(NumberItem(self, i, j, i, rect))
            self.number_items.append(row)

    def boundingRect(self):
        return QRectF(0, 0, self.parent.width, self.parent.height)

class NumberItem(SudokuItem):

    adj = 5

    def __init__(self, parent, row, col, num, rect: QRectF):
        super().__init__(parent=parent)
        self.rect = rect.adjusted(self.adj, self.adj, -self.adj, -self.adj)
        self.row = row
        self.col = col
        self.num = num

        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemIsFocusable)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 1)
        if self.hasFocus():
            brush = QBrush(Qt.gray, Qt.SolidPattern)
        else:
            brush = QBrush(Qt.NoBrush)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(self.rect)
        painter.drawText(self.rect, Qt.AlignCenter, f'{self.num}')

    def boundingRect(self):
        return self.rect.adjusted(-self.adj, -self.adj, self.adj, self.adj)

    def hoverEnterEvent(self, e):
        self.setFocus(Qt.MouseFocusReason)
        self.setCursor(Qt.IBeamCursor)
        e.accept()

    def hoverMoveEvent(self, e):
        pass

    def hoverLeaveEvent(self, e):
        self.clearFocus()
        self.setCursor(Qt.ArrowCursor)
        e.accept()
