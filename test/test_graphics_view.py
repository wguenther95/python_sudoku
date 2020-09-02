from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QHBoxLayout
from PyQt5.QtCore import Qt, QRectF
import sys
import os

from test_graphics_objects import Board
from test_dock_widget import DifficultySelect

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)


class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        view = View()

        self.setCentralWidget(view)

        self.diff_select = DifficultySelect()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.diff_select)

        self.resize(1200, 1200)
        self.setWindowTitle("Sudoku Puzzle")
        self.show()


class View(QGraphicsView):
    def __init__(self):
        super(QGraphicsView, self).__init__()

        self.scene = Scene()

        self.setScene(self.scene)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

    def showEvent(self, e):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)


class Scene(QGraphicsScene):

    scene_rect_buffer = 1.1

    def __init__(self):
        super(QGraphicsScene, self).__init__()

        self.board = Board()

        self.addItem(self.board)

        self.setSceneRect(QRectF(0, 0, self.board.width * self.scene_rect_buffer, self.board.height * self.scene_rect_buffer))
        self.board.setPos(self.sceneRect().width() / 2 - self.board.width / 2, self.sceneRect().height() / 2 - self.board.height / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Window()

    sys.exit(app.exec_())
