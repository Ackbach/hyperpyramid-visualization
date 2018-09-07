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

# 25.4 mm = 1 in
width_in = root.winfo_screenmmwidth() / 25.4
height_in = root.winfo_screenmmheight() / 25.4

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
my_font = tkf.Font(font='monospace', size=20)
pixel_width_per_char = my_font.measure("w")
pixel_height_per_char = my_font.metrics("linespace")

print('Pixel width per character: %f px, Pixel height per character: %f px'
      % (pixel_width_per_char, pixel_height_per_char))

# Figure size in inches
figure_size = (10, 6)


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


""" -------------------------- Node class -------------------------- """


class PascalTriangleNode:


    # Data members.
    row = 1
    row_position = 1
    binomial_coefficient = 1
    number_of_digits = 1
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


    def __str__(self) -> str:
        """
        How to pretty-print this node. Our goal here is to center-
        justify based on the maximum width number in this row. This will
        have to be done outside the class, though, because it depends
        on the max width of the max row.
        :return:
        """

        # Old code.
        """
        if self.number_of_digits // 2 == self.max_number_of_digits // 2:
            # Same parity. We can center exactly.
            # number_of_spaces is divisible by 2.
            number_of_spaces = self.max_number_of_digits - \
                               self.number_of_digits
            spaces = " " * (number_of_spaces // 2)
            return spaces + str(self.binomial_coefficient) + spaces

        else:
            # Different parity. We can center almost exactly. We'll put
            # the extra space on the right.
            number_of_spaces = self.max_number_of_digits - \
                               self.number_of_digits
            left_spaces = " " * (number_of_spaces // 2)
            right_spaces = " " * ((number_of_spaces // 2) + 1)
            return left_spaces + str(self.binomial_coefficient) + \
                right_spaces
        """

        return str(self.binomial_coefficient)


    def compute_width(self) -> list:
        """
        This function computes the width of the
        current coefficient in pixels, and the width of the maximum
        coefficient (near the middle) in pixels.
        :return: list containing this node's width, and the max node's
        width (in that order).
        """

        global pixel_width_per_char

        return [self.number_of_digits * pixel_width_per_char,
                self.max_number_of_digits * pixel_width_per_char]


    def compute_coordinates(self) -> None:
        """
        This function computes the x and y coordinates based on
        pixel width and pixel height of characters, and the level of
        the row.
        :return:
        """

        self.x_coordinate = 1
        self.y_coordinate = 1


row_number = 10
max_width_chars = len(str(n_choose_k(row_number, row_number // 2)))
max_row_width_chars = (row_number + 1) * max_width_chars

# A list comprehension is more Pythonic.
nodes = [PascalTriangleNode(row_number, i)
         for i in range(row_number + 1)]

# for node in nodes:
#     print(str(node))
