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
        self.beta = 7.0 / 3.0   # 8.0 / 3.0

    def lorenz(self, t, state):
        x, y, z = state
        return self.sigma * (y - x), x * (self.rho - z) - y, x * y - self.beta * z  # Derivatives

    def data_gen(self):
        for cnt in itertools.count():
            i = cnt
            state = [self.x[-1], self.y[-1], self.z[-1]]
            sol = solve_ivp(self.lorenz, [i/50, (i+1)/50], state)
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
