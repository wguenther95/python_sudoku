from PyQt5.QtWidgets import QDockWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QComboBox, QLabel
from PyQt5.QtCore import Qt, QRectF


class DifficultySelect(QDockWidget):
    def __init__(self):
        super().__init__()

        diff_widget = QWidget()

        layout = QVBoxLayout()

        self.difficulty_cb = QComboBox()
        self.difficulty_cb.addItem("Easy")
        self.difficulty_cb.addItem("Medium")
        self.difficulty_cb.addItem("Hard")

        self.generate_bt = QPushButton("Generate Board")

        layout.addWidget(self.difficulty_cb)
        layout.addWidget(self.generate_bt)

        diff_widget.setLayout(layout)

        title_label = QLabel("Difficulty Select")

        self.setWidget(diff_widget)
        self.setTitleBarWidget(title_label)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        # self.setFloating(False)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFixedSize(150, 150)
