import tkinter as tk
import tkinter.font as tkf
root = tk.Tk()
my_font = tkf.Font(font='courier', size=12)
pixels_per_char = my_font.measure("w")