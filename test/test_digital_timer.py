from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber
from PyQt5.QtCore import QTimer, QTime

import sys


class DigitalTimer(QLCDNumber):
    def __init__(self):
        super().__init__()
        self.setSegmentStyle(QLCDNumber.Filled)

        self.timer = QTimer()
        self.timer.start(1000)

        self.timer.timeout.connect(self.show_time)

        self.restart()

    def show_time(self):
        self.time = self.time.addSecs(1)
        self.string = self.time.toString('mm:ss')
        self.display(self.string)

    def restart(self):
        self.time = QTime(0, 0, 0, 0)
        self.string = self.time.toString('mm:ss')
        self.display(self.string)
