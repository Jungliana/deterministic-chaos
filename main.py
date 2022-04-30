import tkinter as tk
from plot import Plot
from window import Window
from equation import Sine, TripleSine


if __name__ == "__main__":
    window = Window(Plot(TripleSine()))
    tk.mainloop()
