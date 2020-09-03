from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsGridLayout, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsObject
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor, QColor, QFont
from PyQt5.QtCore import Qt, QLineF, QRectF, QPropertyAnimation, QAbstractAnimation, QPointF, QTimer

from time import time

from test_performance_timer import PerformanceTimer
from test_generator import SudokuGenerator


class SudokuItem(QGraphicsObject):
    def __init__(self, parent=None):
        super(QGraphicsObject, self).__init__(parent=parent)

        self.setParent(parent)
        self.parent = parent

class Board(SudokuItem):

    height = 540.0
    width = 540.0

    def __init__(self):
        super().__init__()

        # Create the sudoku generator object and generate a board.
        self.game = SudokuGenerator()
        # self.game.print()

        # Add a grid to populate with the Sudoku board.
        self.grid = Grid(self)

    def paint(self, painter, option, widget):
        painter.fillRect(self.boundingRect(), Qt.white)

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
        self.update()

    def update(self):
        self.number_items = []
        self.rects = []

        for i in range(9):
            ni_row = []
            rect_row = []
            for j in range(9):
                disabled = False
                x = (self.parent.width / 9) * j
                y = (self.parent.height / 9) * i
                width = self.parent.width / 9
                height = self.parent.height / 9
                rect = QRectF(x, y, width, height)
                num = self.parent.game.board[i][j]
                if num != 0:
                    disabled = True
                rect_row.append(rect)
                ni_row.append(NumberItem(self, i, j, num, rect, disabled))
            self.number_items.append(ni_row)
            self.rects.append(rect_row)

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)

        for i in range(9):
            for j in range(9):
                painter.drawRect(self.rects[i][j])

    def boundingRect(self):
        return QRectF(0, 0, self.parent.width, self.parent.height)

class NumberItem(SudokuItem):

    adj = 5
    hover = False

    def __init__(self, parent, row, col, num, rect: QRectF, disabled=False):
        super().__init__(parent=parent)
        self.rect = rect.adjusted(self.adj, self.adj, -self.adj, -self.adj)
        self.disabled = disabled
        self.row = row
        self.col = col

        if num == 0:
            self.num = ''
        else:
            self.num = num

        self.animations()

        if not self.disabled:
            self.setFlags(QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setTransformOriginPoint(self.rect.center())

    def paint(self, painter, option, widget):
        pen = QPen(Qt.black, 1)
        brush = QBrush(Qt.NoBrush)
        if self.disabled:
            brush = QBrush(QColor(200, 200, 200), Qt.SolidPattern)
        if self.hover:
            brush = QBrush(QColor(140, 190, 220), Qt.SolidPattern)
        if self.isSelected():
            width = self.rect.width() * 1.1
            height = self.rect.height() * 1.1
            x = self.rect.x() - ((width - self.rect.width()) / 2)
            y = self.rect.y() - ((height - self.rect.height()) / 2)
            rect = QRectF(x, y, width, height)
            brush = QBrush(QColor(30, 150, 215), Qt.SolidPattern)
        else:
            rect = self.rect
        # Fill in the background, so items don't remain painted in the case of a new game initialization.
        painter.fillRect(rect, Qt.white)

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setFont(QFont('Helvetica', 14, 50))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, f'{self.num}')

    def boundingRect(self):
        return self.rect.adjusted(-self.adj, -self.adj, self.adj, self.adj)

    def hoverEnterEvent(self, e):
        if not self.disabled:
            self.hover = True
            self.setCursor(Qt.IBeamCursor)
            self.start_animations(QAbstractAnimation.Forward)

    def hoverMoveEvent(self, e):
        pass

    def hoverLeaveEvent(self, e):
        if not self.disabled:
            self.hover = False
            self.setCursor(Qt.ArrowCursor)
            self.start_animations(QAbstractAnimation.Backward)

    def mousePressEvent(self, e):
        # Clear any item that may be selected that belongs to the same parent.
        # Also, remove the focus from that item.
        for item in self.parent.childItems():
            item.setSelected(False)
            item.setFocus(False)
        # Set the current item as selected, and give it focus.
        self.setSelected(True)
        self.setFocus(True)

    def keyPressEvent(self, e):
        if self.hasFocus():
            if e.key() == 16777219 or e.key() == 16777223:
                self.num = ''
            elif e.key() >= 49 and e.key() <= 57:
                self.num = str(e.key() - 48)
            self.update()

    def animations(self):
        scale_value = 1.1
        self.scale_anim = QPropertyAnimation(self, b'scale')
        self.scale_anim.setDuration(100)
        self.scale_anim.setStartValue(1)
        self.scale_anim.setEndValue(scale_value)

    def start_animations(self, direction: QAbstractAnimation):
        self.scale_anim.setDirection(direction)
        self.scale_anim.start()
