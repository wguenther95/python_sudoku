from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QHBoxLayout, QStyleFactory
from PyQt5.QtCore import Qt, QRectF
import sys
import os
from copy import deepcopy

from test_graphics_objects import Board, GameOverOverlay
from test_dock_widget import GameControl
from test_generator import Difficulty

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.view = View()

        self.setCentralWidget(self.view)

        # Main game control Dock Widget
        self.game_control = GameControl()
        self.game_control.start_new_game.connect(self.new_game)
        self.game_control.solve.connect(self.solve_game)
        self.game_control.hint.connect(self.hint)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.game_control)

        # Overlay to display when a solution has been found.
        # Initialize it as not visible, to be toggled later.
        self.game_over = GameOverOverlay(self.view.scene.board)
        self.game_over.setVisible(False)

        self.resize(1200, 1200)
        self.setWindowTitle("Sudoku Puzzle")
        self.show()

    def new_game(self):
        # Current board being used for game
        board = self.view.scene.board

        # Set the difficulty for the current game.
        diff = self.game_control.difficulty_cb.currentText()

        if diff == 'Easy':
            board.game.difficulty = Difficulty.EASY
        elif diff == 'Medium':
            board.game.difficulty = Difficulty.MEDIUM
        else:
            board.game.difficulty = Difficulty.HARD

        # Generate a new game board and update the grid with this board.
        # Make sure the board is enabled for events and the game over overlay is not visible.
        board.game.new_board()
        board.grid.update()
        self.view.scene.board.setEnabled(True)
        self.game_over.setVisible(False)

        # Enable the solve button to show the user the solution.
        self.game_control.solve_puzzle.setEnabled(True)

    def solve_game(self):
        # Current game being used by the player.
        game = self.view.scene.board.game

        # Make a copy to use in the solve algorithm.
        solved_board = deepcopy(game.initial_board)

        # If a solution is found, update the board display.
        # Pause the timer, set the solve button to disabled.
        # Disable the board and set the game over overlay as visible.
        if game.solve(solved_board):
            self.view.scene.board.grid.show_solution(solved_board, game.initial_board)
            self.game_control.timer.pause()
            self.game_control.solve_puzzle.setEnabled(False)
            self.view.scene.board.setEnabled(False)
            self.game_over.setVisible(True)

    def hint(self):
        game = self.view.scene.board.game
        if game.hint(game.board):
            self.view.scene.board.grid.update()

        if game.check_game_over():
            self.view.scene.board.setEnabled(False)
            self.game_over.setVisible(True)
            self.game_control.timer.pause()


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
