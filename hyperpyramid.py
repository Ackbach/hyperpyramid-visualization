# -*- coding: utf-8 -*-

# Some important numerical libraries we'll need. Might need scipy, we'll
# see. Just use courier 10 pitch
import numpy as np
import matplotlib.pyplot as plt
import math
import tkinter as tk
import tkinter.font as tkf


""" ---------------------------- Globals --------------------------- """


font = tkf.Font(font='courier', size=12)
pixels_per_char = font.measure("w")


""" -------------------------- Node class -------------------------- """


class PascalTriangleNode:

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

        global binomial_coefficient
        global number_of_digits

        # Clean inputs:
        n = int(n)
        k = int(k)

        # Take care of special cases to save compute time. Default:
        binomial_coefficient = 1

        # There are n ways to choose 1 or n-1 objects.
        if 1 == k or (n-1) == k:
            binomial_coefficient = n

        # These are impossible, so let the coefficient be zero.
        elif k > n or 0 > n or 0 > k:
            binomial_coefficient = 0

        # The main case: we have n!/(k!(n-k)!).
        else:
            a = math.factorial(n)
            b = math.factorial(k)
            c = math.factorial(n-k)
            binomial_coefficient = a // (b * c)

        number_of_digits = len(str(abs(binomial_coefficient)))

    def __str__(self) -> str:
        """
        How to pretty-print this node.
        :return:
        """

        global binomial_coefficient

        return str(self.binomial_coefficient)

    def compute_width(self) -> int:
        """
        This function computes the width of the coefficient in pixels.
        :return: Width of binomial coefficient in pixels.
        """

        global pixels_per_char
        global number_of_digits

        return number_of_digits * pixels_per_char
