import numpy as np
import itertools


# parent equation class
class Equation:
    def __init__(self):
        self.x = []
        self.y = []
        self.xlim = (0, 10)
        self.ylim = (-10, 10)

    def data_gen(self):
        yield 0, 0

    def update(self, data):
        x, y = data
        self.x.append(x)
        self.y.append(y)
        return x, y

    @staticmethod
    def text_equation():
        return ""


# example equation 1
class Sine(Equation):
    def __init__(self):
        super().__init__()
        self.xlim = (0, 2*np.pi)
        self.ylim = (-np.pi, np.pi)

    def data_gen(self):
        for cnt in itertools.count():
            x = cnt / 20
            y = np.sin(2 * np.pi * (x - 0.01 * x))
            yield x, y

    @staticmethod
    def text_equation():
        return "sin(X)"


# example equation 2
class TripleSine(Equation):
    def __init__(self):
        super().__init__()
        self.xlim = (0, 2*np.pi)
        self.ylim = (-4, 4)

    def data_gen(self):
        for cnt in itertools.count():
            x = cnt / 20
            y = np.sin(2 * np.pi * (x - 0.01 * x)) + \
                np.sin(2 * np.pi * (x+2 - 0.01 * x)) + \
                np.sin(2 * np.pi * (x/2 - 0.01 * x))
            yield x, y

    @staticmethod
    def text_equation():
        return "sin(x) + sin(x+2) + sin(x/2)"
