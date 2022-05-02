import numpy as np
import itertools
from scipy.integrate import solve_ivp


# parent equation class
class Equation:
    def __init__(self):
        self.x = []
        self.y = []
        self.xlim = (0, 10)
        self.ylim = (-10, 10)
        self.params = dict()

    def set_initial_conditions(self, x=None, y=None):
        self.x = [x] if x else []
        self.y = [y] if y else []

    def data_gen(self):
        yield 0, 0

    def update(self, data):
        x, y = data
        self.x.append(x)
        self.y.append(y)
        return x, y

    def __str__(self):
        return "Equation"

    @staticmethod
    def text_equation():
        return ""


# example equation
class TripleSine(Equation):
    def __init__(self):
        super().__init__()
        self.xlim = (0, 4*np.pi)
        self.ylim = (-4, 4)
        self.params = {"a": 2.,
                       "b": 2.}

    def data_gen(self):
        for cnt in itertools.count():
            x = cnt / 20
            y = np.sin(2 * np.pi * (x - 0.01 * x)) + \
                np.sin(2 * np.pi * (x + self.params["a"] - 0.01 * x)) + \
                np.sin(2 * np.pi * (x / self.params["b"] - 0.01 * x))
            yield x, y

    def __str__(self):
        return "Triple sine wave"

    @staticmethod
    def text_equation():
        return "Triple sine wave (example)\n" \
               "sin(x) + sin(x+a) + sin(x/b)"


class LorenzSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [1.]
        self.y = [1.]
        self.z = [1.]

        self.xlim = (-22, 22)
        self.ylim = (-30, 30)

        self.params = {"rho": 28.0,         # 28.0
                       "sigma": 10.0,       # 10.0
                       "beta": 8.0 / 5.0}   # 8.0 / 3.0

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [1.]
        self.y = [y] if y else [1.]
        self.z = [z] if z else [1.]

    def derivatives(self, t, state):
        x, y, z = state
        return self.params["sigma"] * (y - x), \
            x * (self.params["rho"] - z) - y, \
            x * y - self.params["beta"] * z

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i/40, (i+1)/40], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def update(self, data):
        x, y, z = data
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        return x, y

    def __str__(self):
        return "Lorenz system"

    @staticmethod
    def text_equation():
        return "Lorenz system:\n" \
               "dx/dt = sigma * (y-x)\n" \
               "dy/dt = x * (rho - z) - y\n" \
               "dz/dt = xy - beta * z"


class RosslerSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [0.0]
        self.y = [0.0]
        self.z = [0.0]

        self.xlim = (-15, 15)
        self.ylim = (-20, 10)

        self.params = {"a": 0.2,  # 0.2
                       "b": 0.2,  # 0.2
                       "c": 5.7}  # 5.7

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [0.]
        self.y = [y] if y else [0.]
        self.z = [z] if z else [0.]

    def derivatives(self, t, state):
        x, y, z = state
        return -y - z, x + self.params["a"] * y, self.params["b"] + z * (x - self.params["c"])

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i/5, (i+1)/5], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def update(self, data):
        x, y, z = data
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        return x, y

    def __str__(self):
        return "Rössler system"

    @staticmethod
    def text_equation():
        return "Rössler system:\n" \
               "dx/dt = -y - z\n" \
               "dy/dt = x + ay\n" \
               "dz/dt = b + z(x - c)"


class ChenSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [-0.1]
        self.y = [0.5]
        self.z = [-0.6]

        self.xlim = (-25, 30)
        self.ylim = (-30, 35)

        self.params = {"a": 40.,  # 40.
                       "b": 3.,   # 3.
                       "c": 28.}  # 28.

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [-0.1]
        self.y = [y] if y else [0.5]
        self.z = [z] if z else [-0.6]

    def derivatives(self, t, state):
        x, y, z = state
        return self.params["a"] * (y - x), \
            (self.params["c"]-self.params["a"])*x - x*z + self.params["c"]*y,\
            x * y - self.params["b"] * z

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i/50, (i+1)/50], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def update(self, data):
        x, y, z = data
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        return x, y

    def __str__(self):
        return "Chen system"

    @staticmethod
    def text_equation():
        return "Chen system:\n" \
               "dx/dt = a(y - x)\n" \
               "dy/dt = (c-a)x - xz + cy\n" \
               "dz/dt = xy - bz"


class LotkaVolterra(Equation):
    def __init__(self):
        super().__init__()
        self.x = [10.]
        self.y = [10.]

        self.xlim = (-1., 40.)
        self.ylim = (-1., 20.)

        self.params = {"a": 1.1,  # 1.1
                       "b": 0.4,  # 0.4
                       "c": 0.1,  # 0.1
                       "d": 0.4}  # 0.4

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [10.]
        self.y = [y] if y else [10.]

    def derivatives(self, t, state):
        x, y = state
        return (self.params["a"] - self.params["b"] * y) * x, (self.params["c"] * x - self.params["d"]) * y

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1]]
            sol = solve_ivp(self.derivatives, [i/10, (i+1)/10], state)
            yield sol.y[0, 1], sol.y[1, 1]

    def __str__(self):
        return "Lotka-Volterra equations"

    @staticmethod
    def text_equation():
        return "Lotka-Volterra equations:\n" \
               "dx/dt = (a - by)x\n" \
               "dy/dt = (cx - d)y\n\n" \
               "x - prey population size\n" \
               "y - predator population size"
