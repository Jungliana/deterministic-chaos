import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import equation


class Window:
    def __init__(self, plot):
        self.plot = plot
        self.root = ThemedTk(theme='scidpurple')
        self.label = tk.Label(self.root, text="Deterministic chaos")
        self.canvas = FigureCanvasTkAgg(plot.fig, master=self.root)

        self.combobox = ttk.Combobox(self.root, width=34)
        self.param_label = tk.Label(self.root, text="Choose a parameter to change:")
        self.param_combo = ttk.Combobox(self.root, width=8)
        self.param_value = tk.Entry(self.root, width=10)
        self.apply = tk.Button(self.root, text=" apply ")

        self.equation = tk.Label(self.root, text="")
        self.left = tk.Button(self.root, text=" < ")
        self.right = tk.Button(self.root, text=" > ")
        self.pause = tk.Button(self.root, text=" pause ")
        self.paused = False

        self.add_options_to_list()
        self.place_components()
        self.bind_gui_elements()
        self.beautify()

        self.ani = animation.FuncAnimation(self.plot.fig, self.plot.animate,
                                           frames=self.plot.equation.data_gen,
                                           interval=20, blit=False, cache_frame_data=False)

    def beautify(self):
        unified_font = ("Consolas", 14)
        button_font = ("Consolas", 12)

        self.root['padx'] = 20
        self.root['background'] = 'white'
        self.label['background'] = 'white'
        self.label['font'] = unified_font
        self.equation['background'] = 'white'
        self.equation['font'] = unified_font
        self.param_label['background'] = 'white'
        self.param_label['font'] = unified_font
        self.combobox['font'] = button_font
        self.pause['font'] = button_font
        self.apply['font'] = button_font

    def place_components(self):
        self.label.grid(column=0, row=0)
        self.canvas.get_tk_widget().grid(column=0, row=1, rowspan=5)
        self.combobox.grid(column=1, columnspan=3, row=1)
        self.param_label.grid(column=1, columnspan=3, row=2, sticky='S')
        self.param_combo.grid(column=1, row=3)
        self.param_value.grid(column=2, row=3)
        self.apply.grid(column=3, row=3)
        self.equation.grid(column=1, columnspan=3, row=4)
        self.left.grid(column=1, row=5, sticky='E')
        self.right.grid(column=2, row=5, sticky='W')
        self.pause.grid(column=3, row=5)

    def add_options_to_list(self):
        self.combobox['values'] = ("Lorenz system",
                                   "Rössler system",
                                   "Chen system")

    def bind_gui_elements(self):
        self.combobox.bind('<<ComboboxSelected>>', self.update_equation)
        self.param_combo.bind('<<ComboboxSelected>>', self.update_entry_param)
        self.apply.bind('<Button>', self.apply_param_value)
        self.pause.bind('<Button>', self.pause_simulation)
        self.right.bind('<Button>', self.next_axes)
        self.left.bind('<Button>', self.prev_axes)

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

    def update_equation(self, event):
        if self.combobox.get() == "Lorenz system":
            self.plot.new_equation(equation.LorenzSystem())
        elif self.combobox.get() == "Chen system":
            self.plot.new_equation(equation.ChenSystem())
        else:
            self.plot.new_equation(equation.RosslerSystem())
        self.ani.frame_seq = self.plot.equation.data_gen()
        self.load_param_dict()
        self.equation.config(text=self.plot.equation.text_equation())

    def next_axes(self, event):
        next_a = (self.plot.equation.axes + 1) % 3
        self.plot.equation.axes = next_a
        self.plot.change_axes(next_a)

    def prev_axes(self, event):
        prev_a = (self.plot.equation.axes - 1) % 3
        self.plot.equation.axes = prev_a
        self.plot.change_axes(prev_a)

    def pause_simulation(self, event):
        if not self.paused:
            self.ani.pause()
            self.paused = True
        else:
            self.ani.resume()
            self.paused = False
