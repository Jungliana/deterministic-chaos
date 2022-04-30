from matplotlib import pyplot as plt
from equation import Equation


class Plot:

    def __init__(self, eq=None):
        self.equation = eq if eq is not None else Equation()
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot([], [], 'o-')
        self.trace, = self.ax.plot([], [], '.-', lw=1, ms=2)

    def animate(self, i):
        x, y = self.equation.update(i)
        self.line.set_data(x, y)
        self.trace.set_data(self.equation.x, self.equation.y)
        return self.line,

    def new_equation(self, eq):
        self.ax.clear()
        self.equation = eq
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot([], [], 'o-')
        self.trace, = self.ax.plot([], [], '.-', lw=1, ms=2)
