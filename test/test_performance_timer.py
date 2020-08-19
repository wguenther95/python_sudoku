import time


class PerformanceTimer:
    def __init__(self):
        pass

    def start(self):
        self.st = time.perf_counter()

    def end(self):
        self.e = time.perf_counter()
        print(f'Time elapsed: {self.e - self.st}')
