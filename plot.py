import matplotlib as mpl
from matplotlib import pyplot as plt
from cycler import cycler
from equation import Equation


class Plot:
    """
    Animated Matplotlib plot.
    """
    def __init__(self, eq=None):
        mpl.rcParams['axes.prop_cycle'] = cycler(color=['b', 'm', 'k'])
        self.equation = eq if eq is not None else Equation()
        self.fig = plt.Figure(figsize=(8.5, 6.))
        self.ax = self.fig.add_subplot(111)
        self.shadow = self.ax.plot([], [], '.-')
        self.prepare_plot()

    def prepare_plot(self):
        self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
        self.line, = self.ax.plot([], [], 'o-')
        self.trace, = self.ax.plot([], [], '-', lw=1, ms=2)
        self.ax.set_title(self.equation.__str__())
        self.ax.set_ylabel('y')
        self.ax.set_xlabel('x')

        self.last_x = self.equation.x
        self.last_y = self.equation.y
        self.last_z = self.equation.z

    def change_axes(self, next_a=0):
        if next_a == 0:
            self.ax.set(xlim=self.equation.xlim, ylim=self.equation.ylim)
            self.ax.set_ylabel('y')
            self.ax.set_xlabel('x')
        elif next_a == 1:
            self.ax.set(xlim=self.equation.ylim, ylim=self.equation.zlim)
            self.ax.set_ylabel('z')
            self.ax.set_xlabel('y')
        else:
            self.ax.set(xlim=self.equation.xlim, ylim=self.equation.zlim)
            self.ax.set_ylabel('z')
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
