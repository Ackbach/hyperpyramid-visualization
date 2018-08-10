# -*- coding: utf-8 -*-

# Some important numerical libraries we'll need. Might need scipy, we'll
# see. Just use courier 10 pitch
import numpy as np
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import font as tkf


""" ---------------------------- Globals --------------------------- """


root = tk.Tk()

# Get screen characteristics. N.B. This assumes single monitor.
width_px = root.winfo_screenwidth()
height_px = root.winfo_screenheight()
width_in = root.winfo_screenmmwidth() / 25.4
height_in = root.winfo_screenmmheight() / 25.4
# 2.54 cm = in
width_dpi = width_px/width_in
height_dpi = height_px/height_in

print('Width: %i px, Height: %i px' % (width_px, height_px))
print('Width: %f in, Height: %f in' % (width_in, height_in))
print('Width: %f dpi, Height: %f dpi' % (width_dpi, height_dpi))
my_font = tkf.Font(font='monospace', size=12)

# Pixel width and height of a character in the fixed-width font courier.
# Note that two chars gives you exactly twice what one char is.
pixel_width_per_char = my_font.measure("w")
pixel_height_per_char = my_font.metrics("linespace")

# Figure size in inches
figure_size = (10, 6)


""" -------------------------- Node class -------------------------- """


class PascalTriangleNode:

    row = 1
    row_position = 1
    binomial_coefficient = 1
    number_of_digits = 1
    x_coordinate = 0
    y_coordinate = 0

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
        self.binomial_coefficient = 1

        # There are n ways to choose 1 or n-1 objects.
        if 1 == k or (n-1) == k:
            self.binomial_coefficient = n
            # print("Case 1: binomial coefficient = "
            #       + str(binomial_coefficient))

        # These are impossible, so let the coefficient be zero.
        elif k > n or 0 > n or 0 > k:
            self.binomial_coefficient = 0
            # print("Case 2: binomial coefficient = "
            #       + str(binomial_coefficient))

        # The main case: we have n!/(k!(n-k)!).
        else:
            a = math.factorial(n)
            b = math.factorial(k)
            c = math.factorial(n-k)
            self.binomial_coefficient = a // (b * c)
            # print("Case 3: binomial coefficient = "
            #       + str(binomial_coefficient))

        self.number_of_digits = len(str(self.binomial_coefficient))

    def __str__(self) -> str:
        """
        How to pretty-print this node.
        :return:
        """

        return str(self.binomial_coefficient)

    def compute_width(self) -> int:
        """
        This function computes the width of the coefficient in pixels.
        :return: Width of binomial coefficient in pixels.
        """

        global pixel_width_per_char

        return self.number_of_digits * pixel_width_per_char

    def compute_coordinates(self) -> None:
        """
        This function computes the x and y coordinates based on
        pixel width and pixel height of characters, and the level of
        the row.
        :return:
        """

        self.x_coordinate = 1
        self.y_coordinate = 1

nodes = []

for i in range(11):
    nodes.append(PascalTriangleNode(10, i))

for node in nodes:
    print(str(node))
