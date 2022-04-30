import numpy as np


# parent equation class
class Equation:
    def __init__(self):
        self.x = np.arange(0, 10, 0.01)
        self.y = self.x/2
        self.xlim = (0, 10)
        self.ylim = (-10, 10)

    def update(self, i):
        self.y = -self.y
        return self.x, self.y


# example equation 1
class Sine(Equation):
    def __init__(self):
        super().__init__()
        self.x = np.arange(0, 2*np.pi, 0.01)
        self.y = np.sin(self.x)
        self.xlim = (0, 2*np.pi)
        self.ylim = (-1, 1)

    def update(self, i):
        self.y = np.sin(2 * np.pi * (self.x - 0.01 * i))
        return self.x, self.y


# example equation 2
class TripleSine(Equation):
    def __init__(self):
        super().__init__()
        self.x = np.arange(0, 2*np.pi, 0.01)
        self.y = np.sin(self.x) + np.sin(self.x+2) + np.sin(self.x/2)
        self.xlim = (0, 2*np.pi)
        self.ylim = (-4, 4)

    def update(self, i):
        self.y = np.sin(2 * np.pi * (self.x - 0.01 * i)) + \
                 np.sin(2 * np.pi * (self.x+2 - 0.01 * i)) + \
                 np.sin(2 * np.pi * (self.x/2 - 0.01 * i))
        return self.x, self.y
