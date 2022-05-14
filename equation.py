import itertools
import numpy as np
from scipy.integrate import solve_ivp


class Equation:
    def __init__(self):
        self.x = [0]
        self.y = [0]
        self.z = [0]
        self.axes = 0
        self.xlim = (-10, 10)
        self.ylim = (-10, 10)
        self.zlim = (-10, 10)
        self.params = dict()

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [0]
        self.y = [y] if y else [0]
        self.z = [z] if z else [0]

    def data_gen(self):
        yield 0, 0, 0

    def update(self, data):
        x, y, z = data
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        return x, y, z

    def __str__(self):
        return "Equation"

    @staticmethod
    def text_equation():
        return ""


class LorenzSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [1.]
        self.y = [1.]
        self.z = [1.]

        self.xlim = (-22, 22)
        self.ylim = (-30, 30)
        self.zlim = (-5, 55)

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
        self.zlim = (-3, 25)

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
        self.zlim = (-10, 45)

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

    def __str__(self):
        return "Chen system"

    @staticmethod
    def text_equation():
        return "Chen system:\n" \
               "dx/dt = a(y - x)\n" \
               "dy/dt = (c-a)x - xz + cy\n" \
               "dz/dt = xy - bz"


class ThomasSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [1.1]
        self.y = [1.1]
        self.z = [-0.01]

        self.xlim = (-3, 5)
        self.ylim = (-3, 5)
        self.zlim = (-3, 5)

        self.params = {"b": 0.208186}

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [1.1]
        self.y = [y] if y else [1.1]
        self.z = [z] if z else [-0.01]

    def derivatives(self, t, state):
        x, y, z = state
        return np.sin(y) - self.params["b"] * x, \
            np.sin(z) - self.params["b"] * y,\
            np.sin(x) - self.params["b"] * z

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i, (i+1)], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def __str__(self):
        return "Thomas system"

    @staticmethod
    def text_equation():
        return "Thomas system:\n" \
               "dx/dt = sin(y) - bx\n" \
               "dy/dt = sin(z) - by\n" \
               "dz/dt = sin(x) - bz"
