from matplotlib import pyplot as plt
from equation import Equation
import matplotlib as mpl
from cycler import cycler


class Plot:

    def __init__(self, eq=None):
        mpl.rcParams['axes.prop_cycle'] = cycler(color=['b', 'm', 'r'])
        self.equation = eq if eq is not None else Equation()
        self.fig = plt.Figure(figsize=(8.5, 6.))
        self.ax = self.fig.add_subplot(111)
        self.prepare_plot()

    def prepare_plot(self):
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot([], [], 'o-')
        self.trace, = self.ax.plot([], [], '-', lw=1, ms=2)
        self.ax.set_title(self.equation.__str__())
        self.ax.set_ylabel('y')
        self.ax.set_xlabel('x')

    def animate(self, i):
        x, y, z = self.equation.update(i)
        if self.equation.axes == 0:
            self.line.set_data(x, y)
            self.trace.set_data(self.equation.x, self.equation.y)
        elif self.equation.axes == 1:
            self.line.set_data(y, z)
            self.trace.set_data(self.equation.y, self.equation.z)
        else:
            self.line.set_data(x, z)
            self.trace.set_data(self.equation.x, self.equation.z)
        return self.line,

    def new_equation(self, eq):
        self.ax.clear()
        self.equation = eq
        self.prepare_plot()
