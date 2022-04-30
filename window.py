import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from equation import Sine, TripleSine


class Window:
    def __init__(self, plot):
        self.plot = plot
        self.root = tk.Tk()
        self.root.title("Chaos")
        self.label = tk.Label(self.root, text="not really a chaos for now")
        self.canvas = FigureCanvasTkAgg(plot.fig, master=self.root)
        self.combobox = ttk.Combobox(self.root, width=30)
        self.add_options_to_list()
        self.equation = tk.Label(self.root, text="Choose something")
        self.button = tk.Button(self.root, text="Plot")
        self.place_components()
        self.bind_gui_elements()

        self.ani = animation.FuncAnimation(self.plot.fig, self.plot.animate, frames=200, interval=25, blit=False)

    def place_components(self):
        self.label.grid(column=0, row=0)
        self.canvas.get_tk_widget().grid(column=0, row=1, rowspan=4)
        self.combobox.grid(column=1, row=2)
        self.equation.grid(column=1, row=3)
        self.button.grid(column=1, row=4)

    def add_options_to_list(self):
        self.combobox['values'] = ("sin(x)", "triple sine")

    def bind_gui_elements(self):
        self.combobox.bind('<<ComboboxSelected>>', self.update_equation)

    def update_equation(self, event):
        if self.combobox.get() == "sin(x)":
            self.plot.new_equation(Sine())
        else:
            self.plot.new_equation(TripleSine())
        self.equation.config(text=self.plot.equation.text_equation())
