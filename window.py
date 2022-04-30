import tkinter as tk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window:
    def __init__(self, plot):
        self.plot = plot
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text="not really a chaos for now")
        self.canvas = FigureCanvasTkAgg(plot.fig, master=self.root)
        self.listbox = tk.Listbox(self.root, width=30)
        self.add_options_to_list()
        self.equation = tk.Label(self.root, text="y = sin(x)")
        self.button = tk.Button(self.root, text="Plot")
        self.place_components()

        self.ani = animation.FuncAnimation(self.plot.fig, self.plot.animate, frames=200, interval=25, blit=False)

    def place_components(self):
        self.label.grid(column=0, row=0)
        self.canvas.get_tk_widget().grid(column=0, row=1, rowspan=4)
        self.listbox.grid(column=1, row=2)
        self.equation.grid(column=1, row=3)
        self.button.grid(column=1, row=4)

    def add_options_to_list(self):
        self.listbox.insert(1, "sin(x)")
        self.listbox.insert(2, "sin(x) + sin(x+2) + sin(x/2)")
        self.listbox.insert(3, "pendulum")
        self.listbox.insert(4, "bifurcation")
