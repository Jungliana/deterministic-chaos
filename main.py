import tkinter as tk
from plot import Plot
from window import Window


if __name__ == "__main__":
    window = Window(Plot())
    tk.mainloop()

# dodac "cien" przy zmianie warunkow (bardzo blado pod spodem jest widoczny poprzedni przebieg)