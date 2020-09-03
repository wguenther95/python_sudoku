from PyQt5.QtWidgets import QDockWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QComboBox, QLabel
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

class DifficultySelect(QDockWidget):

    start_new_game = pyqtSignal()

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

        layout.addWidget(self.difficulty_cb)
        layout.addWidget(self.new_game)

        diff_widget.setLayout(layout)

        title_label = QLabel("Difficulty Select")

        self.setWidget(diff_widget)
        self.setTitleBarWidget(title_label)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        # self.setFloating(False)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFixedSize(150, 150)

    def new_game_clicked(self):
        self.start_new_game.emit()
