from matplotlib import pyplot as plt
from equation import Equation


class Plot:

    def __init__(self, eq=None):
        self.equation = eq if eq is not None else Equation()
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot(self.equation.x, self.equation.y)

    def animate(self, i):
        x, y = self.equation.update(i)
        self.line.set_data(x, y)
        return self.line

    def new_equation(self, eq):
        self.ax.clear()
        self.equation = eq
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot(self.equation.x, self.equation.y)
