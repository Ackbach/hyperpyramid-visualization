import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as tk

# matplotlib.figure.Figure.text is a method for adding text to a Figure
# object.

root = tk.Tk()
root.wm_title("Embedding in TK")

f = Figure()
f.set_dpi(96)
f.set_size_inches(13, 6)

# f.text could add text to the figure.
a = f.add_subplot(111)
frame1 = f.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)
a.text(x=1, y=1, s='1,1', family='monospace', size=10)
a.text(x=0, y=0, s='0,0', family='monospace', size=10)
a.text(x=0, y=1, s='0,1', family='monospace', size=10)
a.text(x=1, y=0, s='1,0', family='monospace', size=10)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL
                    # tstate


button = tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=tk.BOTTOM)

tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
