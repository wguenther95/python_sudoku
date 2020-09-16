from PyQt5.QtWidgets import (QDockWidget, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QGroupBox, QComboBox, QLabel, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

from test_digital_timer import DigitalTimer

class GameControl(QDockWidget):

    start_new_game = pyqtSignal()
    solve = pyqtSignal()
    hint = pyqtSignal()
    width = 150

    def __init__(self):
        super().__init__()

        diff_widget = QWidget()

        layout = QVBoxLayout()

        self.difficulty_cb = QComboBox()
        self.difficulty_cb.addItem("Easy")
        self.difficulty_cb.addItem("Medium")
        self.difficulty_cb.addItem("Hard")

        self.new_game = QPushButton("New Game")
        self.new_game.clicked.connect(self.new_game_clicked)

        self.solve_puzzle = QPushButton("Solve")
        self.solve_puzzle.clicked.connect(self.solve_clicked)

        self.hint_button = QPushButton("Hint")
        self.hint_button.clicked.connect(self.hint_clicked)

        self.timer = DigitalTimer()

        spacer = QSpacerItem(self.width, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.difficulty_cb)
        layout.addWidget(self.new_game)
        layout.addWidget(self.solve_puzzle)
        layout.addWidget(self.hint_button)
        layout.addSpacerItem(spacer)
        layout.addWidget(self.timer)

        diff_widget.setLayout(layout)

        title_label = QLabel("Game Options")

        self.setWidget(diff_widget)
        self.setTitleBarWidget(title_label)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFixedWidth(self.width)

    def new_game_clicked(self):
        self.start_new_game.emit()
        self.timer.restart()

    def solve_clicked(self):
        self.solve.emit()

    def hint_clicked(self):
        self.hint.emit()
