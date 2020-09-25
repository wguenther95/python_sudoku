from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsGridLayout, QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsObject
from PyQt5.QtGui import QPainter, QBrush, QPen, QCursor, QColor, QFont, QPainterPath
from PyQt5.QtCore import Qt, QLineF, QRectF, QPropertyAnimation, QAbstractAnimation, QPointF, QTimer, pyqtSignal

from time import time
from copy import deepcopy

from test_generator import SudokuGenerator

BOARD_HEIGHT = 540.0
BOARD_WIDTH = 540.0


class SudokuItem(QGraphicsObject):
    def __init__(self, parent=None):
        super(QGraphicsObject, self).__init__(parent=parent)

        self.setParent(parent)
        self.parent = parent

class Board(SudokuItem):

    height = BOARD_HEIGHT
    width = BOARD_WIDTH
    game_over = pyqtSignal()
    show_errors = True

    def __init__(self):
        super().__init__()

        # Create the sudoku generator object and generate a board.
        self.game = SudokuGenerator()
        # self.game.print()

        # Add a grid to populate with the Sudoku board.
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
        self.update()

    def update(self):
        # Clear the board so items aren't stacked on top of each other.
        self.clear_board()

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
                if num != 0 and num == self.parent.game.initial_board[i][j]:
                    disabled = True
                rect_row.append(rect)
                ni_row.append(NumberItem(self, i, j, num, rect, disabled))
            self.number_items.append(ni_row)
            self.rects.append(rect_row)

    def show_solution(self, solved_board, initial_board):
        # Clear the board so items aren't stacked on top of each other.
        self.clear_board()

        self.number_items = []
        self.rects = []

        for i in range(9):
            ni_row = []
            rect_row = []
            for j in range(9):
                disabled = True
                if (initial_board[i][j] == 0):
                    disabled = False
                x = (self.parent.width / 9) * j
                y = (self.parent.height / 9) * i
                width = self.parent.width / 9
                height = self.parent.height / 9
                rect = QRectF(x, y, width, height)
                num = solved_board[i][j]
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

    def clear_board(self):
        for item in self.childItems():
            self.scene().removeItem(item)

class NumberItem(SudokuItem):

    adj = 5
    valid_input = True

    def __init__(self, parent, row, col, num, rect: QRectF, disabled=False):
        super().__init__(parent=parent)
        self.rect = rect.adjusted(self.adj, self.adj, -self.adj, -self.adj)
        self.disabled = disabled
        self.row = row
        self.col = col

        # Create a link to the sudoku game instance.
        self.game = self.parent.parent.game

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
        # Change font color when user input is false.
        # Default pen color is set to black.
        black_pen = QPen(Qt.black, 1)
        red_pen = QPen(Qt.red, 1)

        painter.setPen(black_pen)

        brush = QBrush(Qt.NoBrush)
        if self.disabled:
            brush = QBrush(QColor(200, 200, 200), Qt.SolidPattern)
        if self.isSelected():
            width = self.rect.width() * 1.1
            height = self.rect.height() * 1.1
            x = self.rect.x() - ((width - self.rect.width()) / 2)
            y = self.rect.y() - ((height - self.rect.height()) / 2)
            rect = QRectF(x, y, width, height)
            brush = QBrush(QColor(160, 200, 255), Qt.SolidPattern)
        else:
            rect = self.rect

        painter.setBrush(brush)
        painter.setFont(QFont('Helvetica', 14, 50))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(rect)

        if self.parent.parent.show_errors and not self.valid_input:
            painter.setPen(red_pen)

        painter.drawText(rect, Qt.AlignCenter, f'{self.num}')

    def boundingRect(self):
        return self.rect.adjusted(-self.adj, -self.adj, self.adj, self.adj)

    def hoverEnterEvent(self, e):
        if not self.disabled:
            self.setCursor(Qt.IBeamCursor)
            self.start_animations(QAbstractAnimation.Forward)

    def hoverMoveEvent(self, e):
        pass

    def hoverLeaveEvent(self, e):
        if not self.disabled:
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
        print()
        # Only act on the item that currently has keyboard focus.
        if self.hasFocus():
            # On backspace or delete, remove the current number from spot.
            if e.key() == 16777219 or e.key() == 16777223:
                self.num = ''
                self.game.board[self.row][self.col] = 0
            elif e.key() >= 49 and e.key() <= 57:
                # If the number already exists in spot, do nothing.
                if str(e.key() - 48) == self.num:
                    return

                # Otherwise, set the number to the key that was pressed.
                self.num = str(e.key() - 48)

                board_copy = deepcopy(self.game.board)
                board_copy[self.row][self.col] = int(self.num)

                # Check to make sure that there are no overlaps in columns, and rows, and the board is solveable.
                if self.game.check_input(int(self.num), self.row, self.col, self.game.board):
                    self.valid_input = True
                else:
                    self.valid_input = False

                self.game.board[self.row][self.col] = int(self.num)

            self.update()

            if self.parent.parent.game.check_game_over():
                self.parent.parent.game_over.emit()

    def animations(self):
        scale_value = 1.1
        self.scale_anim = QPropertyAnimation(self, b'scale')
        self.scale_anim.setDuration(100)
        self.scale_anim.setStartValue(1)
        self.scale_anim.setEndValue(scale_value)

    def start_animations(self, direction: QAbstractAnimation):
        self.scale_anim.setDirection(direction)
        self.scale_anim.start()


class GameOverOverlay(SudokuItem):

    width = BOARD_WIDTH * 2 / 3
    height = BOARD_HEIGHT * 1 / 4

    def __init__(self, board):
        super().__init__(parent=board)

        self.x = (BOARD_WIDTH - self.width) / 2
        self.y = (BOARD_HEIGHT / 2) + (BOARD_HEIGHT / 6)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        pen = QPen(QColor('#455A64'), 5)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)

        time = self.parent.scene().views()[0].parent().game_control.timer.time.toString('mm:ss')

        rect = QRectF(self.x, self.y, self.width, self.height)
        string = f'Congratulations, you have found a solution in {time}! Use the New Game button to start over.'

        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        painter.drawPath(path)

        fill_color = QColor('#CFD8DC')
        fill_color.setAlphaF(0.9)
        fill_brush = QBrush(fill_color, Qt.SolidPattern)

        painter.fillPath(path, fill_brush)

        font_pen = QPen(Qt.black, 1)
        painter.setPen(font_pen)
        font = (QFont('Helvetica', 14, 50))
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter | Qt.TextWordWrap, string)
