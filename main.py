import tkinter as tk
from plot import Plot
from window import Window


if __name__ == "__main__":
    window = Window(Plot())
    tk.mainloop()
