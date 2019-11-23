import math
import random
import numpy as np
import matplotlib.pyplot as plt
import copy

from matplotlib import rcParams

rcParams['figure.figsize'] = (6, 6)
rcParams['figure.dpi'] = 150


class Piece:
    """
    A class that defines the functions associated
    with a shape.

    A subclass that inherits from Shape is expected to override methods like
    "ID", "size", and "points" to reflect the characteristics of that particular shape.
    """

    def __init__(self):
        self.ID = "None"
        self.size = 1

    def create(self, num, pt):
        self.set_points(0, 0)
        pm = self.points
        self.points_map = pm

        self.refpt = pt
        x = pt[0] - self.points_map[num][0]
        y = pt[1] - self.points_map[num][1]
        self.set_points(x, y)

    def set_points(self, x, y):
        self.points = []
        self.corners = []

    def rotate_x(x, y, refx, refy, deg):
        """
        Returns the new x value of a point (x, y)
        rotated about the point (refx, refy) by
        deg degrees clockwise.
        """
        return (math.cos(math.radians(deg)) * (x - refx)) + (math.sin(math.radians(deg)) * (y - refy)) + refx

    def rotate_y(x, y, refx, refy, deg):
        """
        Returns the new y value of a point (x, y)
        rotated about the point (refx, refy) by
        deg degrees clockwise.
        """
        return (- math.sin(math.radians(deg)) * (x - refx)) + (math.cos(math.radians(deg)) * (y - refy)) + refy

    def rotate_p(p, ref, d):
        """
        Returns the new point as an integer tuple
        of a point p (tuple) rotated about the point
        ref (tuple) by d degrees clockwise.
        """
        return int(round(rotate_x(p, ref, d))), int(round(rotate_y(p, ref, d)))


    def rotate(self, degrees):
        """
        Returns the points that would be covered by a
        shape that is rotated 0, 90, 180, of 270 degrees
        in a clockwise direction.
        """
        assert (self.points != "None")
        assert (degrees in [0, 90, 180, 270])

        def rotate_this(p):
            return rotate_p(p, self.refpt, degrees)

        self.points = map(rotate_this, self.points)
        self.corners = map(rotate_this, self.corners)

    def flip(self, orientation):
        """
        Returns the points that would be covered if the shape
        was flipped horizontally or vertically.
        """
        assert (orientation == "h" or orientation == "None")
        assert (self.points != "None")

        def flip_h(p):
            x1 = self.refpt[0]
            x2 = p[0]
            x1 = (x1 - (x2 - x1))
            return x1, p[1]

        def no_flip(p):
            return p

        # flip the piece horizontally
        if orientation == "h":
            self.points = map(flip_h, self.points)
            self.corners = map(flip_h, self.corners)
        # flip the piece vertically
        elif orientation == "None":
            self.points = map(no_flip, self.points)
            self.corners = map(no_flip, self.corners)
        else:
            raise Exception("Invalid orientation.")
