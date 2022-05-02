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


# example equation 1
class Sine(Equation):
    def __init__(self):
        super().__init__()
        self.xlim = (0, 4*np.pi)
        self.ylim = (-np.pi, np.pi)

    def data_gen(self):
        for cnt in itertools.count():
            x = cnt / 20
            y = np.sin(2 * np.pi * (x - 0.01 * x))
            yield x, y

    def __str__(self):
        return "Sine wave"

    @staticmethod
    def text_equation():
        return "sin(X)"


# example equation 2
class TripleSine(Equation):
    def __init__(self):
        super().__init__()
        self.xlim = (0, 4*np.pi)
        self.ylim = (-4, 4)

    def data_gen(self):
        for cnt in itertools.count():
            x = cnt / 20
            y = np.sin(2 * np.pi * (x - 0.01 * x)) + \
                np.sin(2 * np.pi * (x+2 - 0.01 * x)) + \
                np.sin(2 * np.pi * (x/2 - 0.01 * x))
            yield x, y

    def __str__(self):
        return "Triple sine wave"

    @staticmethod
    def text_equation():
        return "sin(x) + sin(x+2) + sin(x/2)"


class LorenzSystem(Equation):
    def __init__(self):
        super().__init__()
        self.x = [1.]
        self.y = [1.]
        self.z = [1.]

        self.xlim = (-22, 22)
        self.ylim = (-30, 30)

        self.rho = 28.0         # 28.0
        self.sigma = 10.0       # 10.0
        self.beta = 8.0 / 5.0   # 8.0 / 3.0

    def derivatives(self, t, state):
        x, y, z = state
        return self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z  # Derivatives

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
        self.x = [0.1]
        self.y = [0.2]
        self.z = [0.1]

        self.xlim = (-15, 15)
        self.ylim = (-20, 10)

        self.a = 0.2        # 0.2
        self.b = 0.2        # 0.2
        self.c = 5.7        # 5.7

    def derivatives(self, t, state):
        x, y, z = state
        return -y - z, x + self.a * y, self.b + z * (x - self.c)  # Derivatives

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


class LotkaVolterra(Equation):
    def __init__(self):
        super().__init__()
        self.x = [10.]
        self.y = [10.]

        self.xlim = (-1., 40.)
        self.ylim = (-1., 20.)

        self.a = 1.1       # 1.1
        self.b = 0.4       # 0.4
        self.c = 0.1       # 0.1
        self.d = 0.4       # 0.4

    def derivatives(self, t, state):
        x, y = state
        return (self.a - self.b * y) * x, (self.c * x - self.d) * y

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
