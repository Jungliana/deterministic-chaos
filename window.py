import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from equation import Sine, TripleSine, LorenzSystem, RosslerSystem, LotkaVolterra


class Window:
    def __init__(self, plot):
        self.plot = plot
        self.root = ThemedTk(theme='scidpurple')
        self.label = tk.Label(self.root, text="Deterministic chaos")
        self.canvas = FigureCanvasTkAgg(plot.fig, master=self.root)
        self.combobox = ttk.Combobox(self.root, width=30)
        self.equation = tk.Label(self.root, text="Choose something")
        self.pause = tk.Button(self.root, text="Pause")
        self.paused = False

        self.add_options_to_list()
        self.place_components()
        self.bind_gui_elements()
        self.beautify()

        self.ani = animation.FuncAnimation(self.plot.fig, self.plot.animate,
                                           frames=self.plot.equation.data_gen,
                                           interval=20, blit=False, cache_frame_data=False)

    def beautify(self):
        self.root['padx'] = 20
        self.root['background'] = 'white'
        self.label['background'] = 'white'
        self.equation['background'] = 'white'

    def place_components(self):
        self.label.grid(column=0, row=0)
        self.canvas.get_tk_widget().grid(column=0, row=1, rowspan=4)
        self.combobox.grid(column=1, row=2)
        self.equation.grid(column=1, row=3)
        self.pause.grid(column=1, row=4)

    def add_options_to_list(self):
        self.combobox['values'] = ("sin(x)",
                                   "triple sine",
                                   "Lorenz system",
                                   "Rössler system",
                                   "Lotka-Volterra equations")

    def bind_gui_elements(self):
        self.combobox.bind('<<ComboboxSelected>>', self.update_equation)
        self.pause.bind('<Button>', self.pause_simulation)

    def update_equation(self, event):
        if self.combobox.get() == "sin(x)":
            self.plot.new_equation(Sine())
        elif self.combobox.get() == "Lorenz system":
            self.plot.new_equation(LorenzSystem())
        elif self.combobox.get() == "Rössler system":
            self.plot.new_equation(RosslerSystem())
        elif self.combobox.get() == "Lotka-Volterra equations":
            self.plot.new_equation(LotkaVolterra())
        else:
            self.plot.new_equation(TripleSine())
        self.ani.frame_seq = self.plot.equation.data_gen()
        self.equation.config(text=self.plot.equation.text_equation())

    def pause_simulation(self, event):
        if not self.paused:
            self.ani.pause()
            self.paused = True
        else:
            self.ani.resume()
            self.paused = False
