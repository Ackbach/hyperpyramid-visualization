# For my wife, Susan Garrison Keister. You inspire me, you help me,
# and you help my walk with the Lord. I love you!

# -*- coding: utf-8 -*-

# Some important numerical libraries we'll need. Might need scipy, we'll
# see. Just use courier 10 pitch

import tkinter as tk
from tkinter import font as tkf

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.figure import Figure
import sys


""" -------------------------- Factorials -------------------------- """


def n_choose_k(n: int, k: int) -> int:
    """
    From
    https://stackoverflow.com/questions/26560726/python-binomial-
    coefficient,
    from alisianoi's answer.
    Compute the number of ways to choose k elements out of a pile of n.

    Use an iterative approach with the multiplicative formula:
    \frac{n!}{k!(n - k)!} =
    \frac{n(n - 1)\dots(n - k + 1)}{k(k-1)\dots(1)} =
    \prod{i = 1}{k}\frac{n + 1 - i}{i}

    Also rely on the symmetry: C_n^k = C_n^{n - k}, so the product can
    be calculated up to min(k, n - k)

    :param n: the size of the pile of elements
    :param k: the number of elements to take from the pile
    :return: the number of ways to choose k elements out of a pile of n
    """

    # When k out of sensible range, should probably throw an exception.
    # For compatibility with scipy.special.{comb, binom} returns 0
    # instead.

    # Special cases when there are NO ways to choose:
    if k < 0 or k > n:
        return 0

    # Only one way to choose all or none:
    if k == 0 or k == n:
        return 1

    # Initialize the multiplicative accumulator.
    total_ways = 1

    # Take the shorter route.
    for i in range(min(k, n - k)):
        total_ways = total_ways * (n - i) // (i + 1)

    return total_ways


""" ----------------- Globals and Units Conversion ----------------- """


root = tk.Tk()
root.wm_title("Embedding in TK")

# Debug flag
debug_flag = True
# debug_flag = False

# Force update idle tasks to run, to see if it fixes our geometry prob:
root.update_idletasks()

# Get screen characteristics. N.B. This assumes single monitor.
width_px = root.winfo_screenwidth()
height_px = root.winfo_screenheight()

# 25.4 mm = 1 in
width_in = root.winfo_screenmmwidth() / 25.4
height_in = root.winfo_screenmmheight() / 25.4

print('Uncorrected screen width (in):' + str(width_in))
print('Uncorrected screen height (in):' + str(height_in))

# If on Windows, scale by correction factors.
# These are, unfortunately, experimentally determined. I have not been
# able to figure out the winfo_screenmmwidth and winfo_screenmmheight
# functions are so incorrect in their reported values, but they are.
if sys.platform.startswith('win'):
    width_correction_factor = 1.481
    height_correction_factor = 1.58
    width_in = width_in / width_correction_factor
    height_in = height_in / height_correction_factor

# Calculate dpi's (ratios):
width_dpi = width_px/width_in
height_dpi = height_px/height_in

print('Screen width: %i px, Screen height: %i px' %
      (width_px, height_px))
print('Screen width: %f in, Screen height: %f in' %
      (width_in, height_in))
print('Screen ratio for width: %f dpi, Screen ratio for height: %f dpi'
      % (width_dpi, height_dpi))

# Pixel width and height of a character in the fixed-width font courier.
# Note that two chars gives you exactly twice what one char is.
my_font = tkf.Font(font='monospace', size=10)
pixel_width_per_char = my_font.measure("w")
pixel_height_per_char = my_font.metrics("linespace")

print('Pixel width per character: %f px, Pixel height per character: %f px'
      % (pixel_width_per_char, pixel_height_per_char))

# Figure size in inches
figure_size = (13, 6)

f = Figure()
f.set_dpi(width_dpi)
f.set_size_inches(figure_size[0], figure_size[1])

# a.text could add text to the figure.
a = f.add_subplot(111)
frame1 = f.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)

# This we would input from the user, generally.
row_number = 16


def x_chars_to_xu(x_chars: float) -> float:
    """
    This function takes in a number of characters, and returns the
    width of those characters in x data units of the graph. x_chars
    could be fractional, hence the float type.
    :param x_chars:
    :return:
    """

    # These are the conversion rates from outside, just calculated.
    global pixel_width_per_char
    global width_dpi
    global figure_size

    return ((x_chars*(pixel_width_per_char + 2))/width_dpi)/figure_size[0]


# Similarly to the above, find the vertical spacing between numbers.
# Assume baselines are 1.5 times character height.
# yu refers to y direction data units, needed for the .text function.
num_y_space_char = 1.5
num_y_space_yu = ((num_y_space_char * pixel_height_per_char) /
                  height_dpi) / figure_size[1]

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# canvas.bind("<1>", lambda event: canvas.focus_set())


def recompute_triangle():
    """
    This function redraws Pascal's Triangle on the basis of a new number
    of rows.
    :return:
    """
    global row_number
    global canvas
    global a
    global f

    # The following parameters determine the maximum width in x units
    # for the biggest number in the lowest row. xu refers to x direction
    # data units in the graph, needed for the .text function.
    max_width_chars = len(str(n_choose_k(row_number, row_number // 2)))

    # The following parameters assume one space between numbers
    # horizontally: take half from one number, half from the next, and
    # add one, to get the horizontal spacing between numbers.
    num_x_space_char = max_width_chars

    """ ------------------------ Node class ------------------------ """

    class PascalTriangleNode:

        # Data members.
        row = 1
        row_position = 1
        binomial_coefficient = 1
        number_of_digits = 1
        number_of_digits_xu = 0.01
        x_coordinate = 0
        y_coordinate = 0

        # Function members.
        def __init__(self, n: int=1, k: int=1):
            """
            This function initializes a node in Pascal's Triangle.
            :param n:
            :param k:
            """

            # Clean inputs:
            n = int(n)
            k = int(k)
            # print('n = ' + str(n))
            # print('k = ' + str(k))

            # Assign row number and row position.
            self.row = n
            self.row_position = k

            # Take care of special cases to save compute time. Default:
            self.binomial_coefficient = n_choose_k(n, k)
            self.number_of_digits = len(str(self.binomial_coefficient))

            # Intermediate calculations we don't care about.
            num_digits_px = self.number_of_digits * pixel_width_per_char
            num_digits_in = num_digits_px / width_dpi

            # This is important for calculating position in data units.
            self.number_of_digits_xu = num_digits_in / figure_size[0]

            # Auto-compute the coordinates.
            self.compute_coordinates()

        def __str__(self) -> str:
            """
            How to pretty-print this node. Our goal here is to center-
            justify based on the maximum width number in this row. This
            will
            have to be done outside the class, though, because it
            depends
            on the max width of the max row.
            :return:
            """

            return str(self.binomial_coefficient)

        def compute_coordinates(self) -> None:
            """
            This function computes the x and y coordinates based on
            pixel width and pixel height of characters, and the level of
            the row.
            :return:
            """

            nonlocal num_x_space_char
            global num_y_space_yu
            global debug_flag

            # Units are in chars.
            x_central_offset_chars = (self.row_position - self.row / 2) * \
                num_x_space_char
            # if debug_flag:
            #     print("x central offset in chars: " +
            #           str(x_central_offset_chars))

            # For the .text function, we need the lower left coordinate.
            # Subtract half the width of this number. Convert to x units.
            x_left_offset_chars = x_central_offset_chars + \
                self.number_of_digits / 2
            # if debug_flag:
            #     print(str(x_left_offset_chars))
            x_left_offset_xu = x_chars_to_xu(x_left_offset_chars)
            # if debug_flag:
            #     print(str(x_left_offset_xu))

            # Start at x = 0.5, and subtract the offset in xu.
            self.x_coordinate = 0.5 - x_left_offset_xu

            # The y coordinate is way easier.
            self.y_coordinate = 1 - (self.row + 1) * num_y_space_yu
    """
    if debug_flag:
        debug_number = 16
        debug_node = PascalTriangleNode(debug_number, debug_number // 2)
        print(str(debug_node.x_coordinate))
        print(str(debug_node))
    """

    # A list comprehension is more Pythonic.
    nodes = [[PascalTriangleNode(row, i)
             for i in range(row + 1)]
             for row in range(row_number + 1)]

    # for list_of_nodes in nodes:
    #     for node in list_of_nodes:
    #         print(str(node))

    # Clear the previous graph, if any.
    a.clear()

    colors = ['brown', 'green', 'blue', 'black']

    for list_of_nodes in nodes:
        for node in list_of_nodes:
            a.text(x=node.x_coordinate, y=node.y_coordinate,
                   s=str(node), family='monospace', size=10,
                   color=colors[node.row % len(colors)])

    """
    # Test Code:
    # a.text(x=1, y=1, s='1,1', family='monospace', size=10)
    # a.text(x=0, y=0, s='0,0', family='monospace', size=10)
    # a.text(x=0, y=1, s='0,1', family='monospace', size=10)
    # a.text(x=1, y=0, s='1,0', family='monospace', size=10)
    """

    # a tk.DrawingArea
    # a tk.DrawingArea
    canvas.draw()
    toolbar.update()


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent errors.


sv = tk.StringVar()


def _update_number_rows(event=None) -> bool:
    """
    This function updates the number of rows to display, and displays
    them.
    :return:
    """
    global row_number
    global sv
    global debug_flag
    global root
    global e1

    if debug_flag:
        print("Calling _update_number_rows.")

    try:
        text = sv.get()
        if debug_flag:
            print(text)
        int_value = int(text)
        if debug_flag:
            print(int_value)
        if int_value > 18:
            int_value = 18
            sv.set(str(int_value))
        if int_value < 0:
            int_value = 0
            sv.set(str(int_value))
        row_number = int_value
        recompute_triangle()

        # Validate command has to return True if it's a good value,
        if debug_flag:
            print(row_number)

        # Have to
        root.after_idle(lambda: e1.config(validate="focusout"))
        return True

    except ValueError:
        # and False if not.
        root.after_idle(lambda: e1.config(validate="focusout"))
        return False


e2 = tk.Label(root, text='Number of Rows (max 18):')
e2.pack()

e1 = tk.Entry(root, textvariable=sv, validate="focusout",
              validatecommand=_update_number_rows)
e1.pack()
e1.bind('<Return>', _update_number_rows)
e1.bind('<KP_Enter>', _update_number_rows)

button = tk.Button(master=root, text='Quit', command=_quit)
button.pack()

root.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
