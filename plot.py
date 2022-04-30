from matplotlib import pyplot as plt
import numpy as np


class Plot:

    def __init__(self, eq=None):
        self.equation = eq
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        x = np.arange(0, 10, 0.01)
        self.line, = self.ax.plot(self.equation.start()) \
            if self.equation else self.ax.plot(x, np.sin(x))

    def animate(self, i):
        x = np.linspace(0, 2, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        self.line.set_data(x, y)
        return self.line
