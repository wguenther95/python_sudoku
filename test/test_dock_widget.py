from PyQt5.QtWidgets import (QDockWidget, QWidget, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QComboBox, QLabel, QSpacerItem,
                             QSizePolicy, QCheckBox, QToolButton)
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QIcon
from pathlib import Path
from test_digital_timer import DigitalTimer

RESOURCES_PATH = Path(__file__).parent.parent / "resources"


class GameControl(QDockWidget):

    start_new_game = pyqtSignal()
    solve = pyqtSignal()
    hint = pyqtSignal()
    show_errors = pyqtSignal()
    width = 150
    solve_icon = RESOURCES_PATH / 'solve.png'
    new_game_icon = RESOURCES_PATH / 'new_game.png'
    hint_icon = RESOURCES_PATH / 'hint.png'
    down_arrow_icon = str(RESOURCES_PATH / 'down_arrow.png')

    def __init__(self):
        super().__init__()

        diff_widget = QWidget()

        layout = QVBoxLayout()

        self.difficulty_cb = QComboBox()
        self.difficulty_cb.addItem("Easy")
        self.difficulty_cb.addItem("Medium")
        self.difficulty_cb.addItem("Hard")

        self.new_game = QToolButton()
        self.new_game.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.new_game.setText("New Game")
        self.new_game.setIcon(QIcon(str(self.new_game_icon)))
        self.new_game.clicked.connect(self.new_game_clicked)

        self.solve_puzzle = QToolButton()
        self.solve_puzzle.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.solve_puzzle.setText("Solve")
        self.solve_puzzle.setIcon(QIcon(str(self.solve_icon)))
        self.solve_puzzle.clicked.connect(self.solve_clicked)

        self.hint_button = QToolButton()
        self.hint_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.hint_button.setText("Hint")
        self.hint_button.setIcon(QIcon(str(self.hint_icon)))
        self.hint_button.clicked.connect(self.hint_clicked)

        self.check_chb = QCheckBox("Show errors")
        self.check_chb.setChecked(True)
        self.check_chb.clicked.connect(self.check_box_clicked)

        self.timer = DigitalTimer()

        spacer = QSpacerItem(self.width, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.difficulty_cb)
        layout.addWidget(self.new_game)
        layout.addWidget(self.solve_puzzle)
        layout.addWidget(self.hint_button)
        layout.addWidget(self.check_chb)
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

    def check_box_clicked(self):
        self.show_errors.emit()
