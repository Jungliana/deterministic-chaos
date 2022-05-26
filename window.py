import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import equation


class Window:
    """
    Basic window containing GUI elements and animated plot.
    """
    def __init__(self, plot):
        self.plot = plot
        self.root = ThemedTk(theme='breeze')
        self.label = ttk.Label(self.root, text="Deterministic chaos")
        self.canvas = FigureCanvasTkAgg(plot.fig, master=self.root)

        self.combobox = ttk.Combobox(self.root, width=34)
        self.equation_label = ttk.Label(self.root, text="")
        self.initial_cond_label = ttk.Label(self.root, text="Change initial conditions:")
        self.x_slider = tk.Scale(self.root, length=250, sliderlength=20, from_=-2., to=2.,
                                 resolution=0.05, tickinterval=1., orient="horizontal")
        self.y_slider = tk.Scale(self.root, length=250, sliderlength=20, from_=-2., to=2.,
                                 resolution=0.05, tickinterval=1., orient="horizontal")
        self.z_slider = tk.Scale(self.root, length=250, sliderlength=20, from_=-2., to=2.,
                                 resolution=0.05, tickinterval=1., orient="horizontal")

        self.param_label = ttk.Label(self.root, text="Choose a parameter to change:")
        self.param_combo = ttk.Combobox(self.root, width=8)
        self.param_value = ttk.Entry(self.root, width=10)
        self.apply = ttk.Button(self.root, text=" apply ", width=8)

        self.left = ttk.Button(self.root, text=" < ", width=7)
        self.right = ttk.Button(self.root, text=" > ", width=7)
        self.reset = ttk.Button(self.root, text=" reset ", width=7)
        self.pause = ttk.Button(self.root, text=" pause ", width=7)
        self.paused = False

        self.set_window_geometry()
        self.add_options_to_list()
        self.place_components()
        self.bind_gui_elements()
        self.beautify()

        self.ani = animation.FuncAnimation(self.plot.fig, self.plot.animate,
                                           frames=self.plot.equation.data_gen,
                                           interval=20, blit=False, cache_frame_data=False)

    def set_window_geometry(self):
        width = 1250
        height = 650
        self.root.geometry("%dx%d" % (width, height))
        self.root.title("Deterministic chaos")

    def beautify(self):
        unified_font = ("Consolas", 14)

        self.root['padx'] = 10
        self.root['background'] = 'white'
        self.label['background'] = 'white'
        self.label['font'] = unified_font
        self.initial_cond_label['background'] = 'white'
        self.initial_cond_label['font'] = unified_font
        self.equation_label['background'] = 'white'
        self.equation_label['font'] = unified_font
        self.param_label['background'] = 'white'
        self.param_label['font'] = unified_font
        self.x_slider['background'] = 'white'
        self.y_slider['background'] = 'white'
        self.z_slider['background'] = 'white'

    def place_components(self):
        self.label.grid(column=0, row=0)
        self.canvas.get_tk_widget().grid(column=0, row=1, rowspan=10)
        self.combobox.grid(column=1, columnspan=4, row=1)
        self.equation_label.grid(column=1, columnspan=4, row=2)
        self.initial_cond_label.grid(column=1, columnspan=4, row=3, sticky='S')
        self.x_slider.grid(column=1, columnspan=4, row=4)
        self.y_slider.grid(column=1, columnspan=4, row=5)
        self.z_slider.grid(column=1, columnspan=4, row=6)
        self.param_label.grid(column=1, columnspan=4, row=7, sticky='S')
        self.param_combo.grid(column=1, row=8, sticky='E')
        self.param_value.grid(column=2, row=8, columnspan=2)
        self.apply.grid(column=4, row=8)
        self.left.grid(column=2, row=9)
        self.right.grid(column=3, row=9)
        self.reset.grid(column=4, row=9)
        self.pause.grid(column=1, row=9)

    def add_options_to_list(self):
        self.combobox['values'] = ("Lorenz system",
                                   "Rössler system",
                                   "Chua's circuit",
                                   "Chen system",
                                   "Thomas system",
                                   "Aizawa system")

    def bind_gui_elements(self):
        self.combobox.bind('<<ComboboxSelected>>', self.update_equation)
        self.param_combo.bind('<<ComboboxSelected>>', self.update_entry_param)
        self.x_slider.bind("<ButtonRelease-1>", self.apply_changes)
        self.y_slider.bind("<ButtonRelease-1>", self.apply_changes)
        self.z_slider.bind("<ButtonRelease-1>", self.apply_changes)
        self.apply.bind('<Button>', self.apply_param_value)
        self.reset.bind('<Button>', self.update_equation)
        self.pause.bind('<Button>', self.pause_simulation)
        self.right.bind('<Button>', self.next_axes)
        self.left.bind('<Button>', self.prev_axes)

    def set_sliders(self):
        self.x_slider.set(self.plot.equation.x[0])
        self.y_slider.set(self.plot.equation.y[0])
        self.z_slider.set(self.plot.equation.z[0])

    def load_param_dict(self):
        params = list(self.plot.equation.params.keys())
        self.param_combo['values'] = params
        self.param_combo.set('')
        self.param_value.delete(0, len(self.param_value.get()))

    def update_entry_param(self, _):
        self.param_value.delete(0, len(self.param_value.get()))
        self.param_value.insert(0, str(self.plot.equation.params[self.param_combo.get()]))

    def apply_param_value(self, _):
        if self.param_combo.get() in self.plot.equation.params.keys():
            try:
                new_param = float(self.param_value.get())
            except ValueError:
                return
            self.plot.equation.params[self.param_combo.get()] = new_param
            self.apply_changes()

    def apply_changes(self, event=None):
        self.plot.last_x = self.plot.equation.x
        self.plot.last_y = self.plot.equation.y
        self.plot.last_z = self.plot.equation.z
        self.plot_shadow()
        self.plot.equation.set_initial_conditions(self.x_slider.get(),
                                                  self.y_slider.get(),
                                                  self.z_slider.get())
        self.ani.frame_seq = self.plot.equation.data_gen()

    def plot_shadow(self):
        line = self.plot.shadow.pop(0)
        line.remove()
        axes_to_draw = self.plot.equation.axes
        if axes_to_draw == 0:
            self.plot.shadow = self.plot.ax.plot(self.plot.last_x, self.plot.last_y, 'k-', alpha=0.15)
        elif axes_to_draw == 1:
            self.plot.shadow = self.plot.ax.plot(self.plot.last_y, self.plot.last_z, 'k-', alpha=0.15)
        else:
            self.plot.shadow = self.plot.ax.plot(self.plot.last_x, self.plot.last_z, 'k-', alpha=0.15)

    def update_equation(self, event=None):
        if self.combobox.get() == "Lorenz system":
            self.plot.new_equation(equation.LorenzSystem())
        elif self.combobox.get() == "Rössler system":
            self.plot.new_equation(equation.RosslerSystem())
        elif self.combobox.get() == "Chua's circuit":
            self.plot.new_equation(equation.ChuaCircuit())
        elif self.combobox.get() == "Chen system":
            self.plot.new_equation(equation.ChenSystem())
        elif self.combobox.get() == "Thomas system":
            self.plot.new_equation(equation.ThomasSystem())
        elif self.combobox.get() == "Aizawa system":
            self.plot.new_equation(equation.AizawaSystem())
        else:
            self.plot.new_equation(equation.Equation())
        self.ani.frame_seq = self.plot.equation.data_gen()
        self.set_sliders()
        self.load_param_dict()
        self.equation_label.config(text=self.plot.equation.text_equation())

    def next_axes(self, _):
        next_a = (self.plot.equation.axes + 1) % 3
        self.plot.equation.axes = next_a
        self.plot.change_axes(next_a)
        self.plot_shadow()

    def prev_axes(self, _):
        prev_a = (self.plot.equation.axes - 1) % 3
        self.plot.equation.axes = prev_a
        self.plot.change_axes(prev_a)
        self.plot_shadow()

    def pause_simulation(self, _):
        if not self.paused:
            self.ani.pause()
            self.paused = True
        else:
            self.ani.resume()
            self.paused = False
