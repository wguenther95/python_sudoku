from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsGridLayout, QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QLineF


class Board(QGraphicsWidget):

    height = 270.0
    width = 270.0

    def __init__(self):
        super(QGraphicsWidget, self).__init__()

        self.resize(self.width, self.height)

        grid = QGraphicsGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        self.setLayout(grid)

        for i in range(9):
            for j in range(9):
                square = Square()
                grid.addItem(square, i, j)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width, self.height)

        lines = [QLineF(self.width * (1 / 3), 0, self.width * (1 / 3), self.height),
                 QLineF(self.width * (2 / 3), 0, self.width * (2 / 3), self.height),
                 QLineF(0, self.height * (1 / 3), self.width, self.height * (1 / 3)),
                 QLineF(0, self.height * (2 / 3), self.width, self.height * (2 / 3))]

        for line in lines:
            painter.drawLine(line)


class Square(QGraphicsWidget):

    width = 30.0
    height = 30.0

    def __init__(self):
        super(QGraphicsWidget, self).__init__()

        self.resize(self.width, self.height)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width, self.height)
