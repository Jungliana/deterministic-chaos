import itertools
import numpy as np
from scipy.integrate import solve_ivp


class Equation:
    """
    Base class for a system of equations.

    x, y, z - history of calculated points;
    axes - currently visible axes (0 - x&y, 1 - y&z, 2 - x&z);
    xlim, ylim, zlim - limits of the visible coordinate system;
    params - dictionary containing all parameters of the system of equations;
    """
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

    def derivatives(self, _, state):
        x, y, z = state
        dx = self.params["sigma"] * (y - x)
        dy = x * (self.params["rho"] - z) - y
        dz = x * y - self.params["beta"] * z
        return dx, dy, dz

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
        self.ylim = (-15, 10)
        self.zlim = (-3, 25)

        self.params = {"a": 0.2,  # 0.2
                       "b": 0.2,  # 0.2
                       "c": 5.7}  # 5.7

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [0.]
        self.y = [y] if y else [0.]
        self.z = [z] if z else [0.]

    def derivatives(self, _, state):
        x, y, z = state
        dx = -y - z
        dy = x + self.params["a"] * y
        dz = self.params["b"] + z * (x - self.params["c"])
        return dx, dy, dz

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i/10, (i+1)/10], state, method='DOP853')
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def __str__(self):
        return "Rössler system"

    @staticmethod
    def text_equation():
        return "Rössler system:\n" \
               "dx/dt = -y - z\n" \
               "dy/dt = x + ay\n" \
               "dz/dt = b + z(x - c)"


class ChuaCircuit(Equation):
    def __init__(self):
        super().__init__()
        self.x = [0.1]
        self.y = [0.1]
        self.z = [0.1]

        self.xlim = (-3, 3)
        self.ylim = (-2, 2)
        self.zlim = (-6, 6)

        self.params = {"alpha": 15.395,  # 15.395
                       "beta": 28.}      # 28.

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [0.1]
        self.y = [y] if y else [0.1]
        self.z = [z] if z else [0.1]

    @staticmethod
    def f(x):
        return -0.714*x - 0.2145*(abs(x+1) - abs(x-1))

    def derivatives(self, _, state):
        x, y, z = state
        dx = self.params["alpha"] * (y - x - self.f(x))
        dy = x - y + z
        dz = -self.params["beta"] * y
        return dx, dy, dz

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i, (i+1)], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def __str__(self):
        return "Chua's circuit"

    @staticmethod
    def text_equation():
        return "Chua's circuit:\n" \
               "dx/dt = alpha * (y - x - f(x))\n" \
               "dy/dt = x - y + z\n" \
               "dz/dt = -beta * y\n\n" \
               "f(x) = -0.714x-0.2145(|x+1|-|x-1|)"


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

    def derivatives(self, _, state):
        x, y, z = state
        dx = self.params["a"] * (y - x)
        dy = (self.params["c"] - self.params["a"]) * x - x*z + self.params["c"]*y
        dz = x * y - self.params["b"] * z
        return dx, dy, dz

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

        self.xlim = (-5, 5)
        self.ylim = (-5, 5)
        self.zlim = (-5, 5)

        self.params = {"b": 0.208186}

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [1.1]
        self.y = [y] if y else [1.1]
        self.z = [z] if z else [-0.01]

    def derivatives(self, _, state):
        x, y, z = state
        dx = np.sin(y) - self.params["b"] * x
        dy = np.sin(z) - self.params["b"] * y
        dz = np.sin(x) - self.params["b"] * z
        return dx, dy, dz

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i, (i+1)], state, method='DOP853')
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def __str__(self):
        return "Thomas system"

    @staticmethod
    def text_equation():
        return "Thomas system:\n" \
               "dx/dt = sin(y) - bx\n" \
               "dy/dt = sin(z) - by\n" \
               "dz/dt = sin(x) - bz"


class AizawaSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [0.1]
        self.y = [1.00]
        self.z = [0.01]

        self.xlim = (-2.5, 2.5)
        self.ylim = (-2.5, 2.5)
        self.zlim = (-2.5, 2.5)

        self.params = {"a": 0.95,
                       "b": 0.7,
                       "c": 0.6,
                       "d": 3.5,
                       "e": 0.25,
                       "f": 0.1}

    def set_initial_conditions(self, x=None, y=None, z=None):
        self.x = [x] if x else [0.1]
        self.y = [y] if y else [1.00]
        self.z = [z] if z else [0.01]

    def derivatives(self, _, state):
        x, y, z = state
        dx = (z - self.params["b"]) * x - self.params["d"] * y
        dy = self.params["d"] * x + (z - self.params["b"]) * y
        dz = self.params["c"] + self.params["a"]*z - z**3 / 3 \
            - (x*x + y*y) * (1 + self.params["e"]*z) + self.params["f"]*z * x**3
        return dx, dy, dz

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.derivatives, [i, (i+1)], state)
            yield sol.y[0, 1], sol.y[1, 1], sol.y[2, 1]

    def __str__(self):
        return "Aizawa system"

    @staticmethod
    def text_equation():
        return "Aizawa system:\n" \
               "dx/dt = (z-b)x - dy\n" \
               "dy/dt = dx + (z-b)y\n" \
               "dz/dt = c + az - (z^3)/3 -\n"\
               " -(x^2 + y^2)(1+ez) + fzx^3"
