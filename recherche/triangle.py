import numpy as np


class Triangle():
    def __init__(self, points: list):
        self.x = points
        self.u = {}
        self.ids = []

    def set_ids(self, l):
        self.ids = l

    def set_u(self, vecteurs):
        self.u = vecteurs
