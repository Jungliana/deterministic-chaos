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

        self.combobox = ttk.Combobox(self.root, width=34)
        self.param_combo = ttk.Combobox(self.root, width=8)
        self.param_value = tk.Entry(self.root, width=10)
        self.apply = tk.Button(self.root, text="apply")

        self.equation = tk.Label(self.root, text="Choose something")
        self.pause = tk.Button(self.root, text="pause")
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
        self.combobox.grid(column=1, columnspan=3, row=1)
        self.param_combo.grid(column=1, row=2)
        self.param_value.grid(column=2, row=2)
        self.apply.grid(column=3, row=2)
        self.equation.grid(column=1, columnspan=3, row=3)
        self.pause.grid(column=1, row=4)

    def add_options_to_list(self):
        self.combobox['values'] = ("sin(x)",
                                   "triple sine",
                                   "Lorenz system",
                                   "Rössler system",
                                   "Lotka-Volterra equations")

    def bind_gui_elements(self):
        self.combobox.bind('<<ComboboxSelected>>', self.update_equation)
        self.param_combo.bind('<<ComboboxSelected>>', self.update_entry_param)
        self.apply.bind('<Button>', self.apply_param_value)
        self.pause.bind('<Button>', self.pause_simulation)

    def load_param_dict(self):
        params = list(self.plot.equation.params.keys())
        self.param_combo['values'] = params
        self.param_combo.set('')
        self.param_value.delete(0, len(self.param_value.get()))

    def update_entry_param(self, event):
        self.param_value.delete(0, len(self.param_value.get()))
        self.param_value.insert(0, str(self.plot.equation.params[self.param_combo.get()]))

    def apply_param_value(self, event):
        if self.param_combo.get() in self.plot.equation.params.keys():
            try:
                new_param = float(self.param_value.get())
            except ValueError as e:
                return
            self.plot.equation.params[self.param_combo.get()] = new_param
            self.plot.equation.set_initial_conditions()
            self.ani.frame_seq = self.plot.equation.data_gen()
            print(f'new param: {new_param}')

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
        self.load_param_dict()
        self.equation.config(text=self.plot.equation.text_equation())

    def pause_simulation(self, event):
        if not self.paused:
            self.ani.pause()
            self.paused = True
        else:
            self.ani.resume()
            self.paused = False
