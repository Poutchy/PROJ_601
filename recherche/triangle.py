import numpy as np


class Triangle():
    def __init__(self, points: list):
        self.x = points
        self.u = {}
        self.ids = []
        self.gaussian_density = 0.0
        self.area_density = 0.0
        self.adjacent_faces = []

    def set_ids(self, l):
        self.ids = l

    def set_u(self, vecteurs):
        self.u = vecteurs

    def set_adjacent_faces(self, i=1):
        possible_faces = []
        for p in self.x:
            possible_faces.extend([f for f in p.faces if (
                f != self and f not in possible_faces)])
        self.adjacent_faces = possible_faces

    def __str__(self):
        return f"Triangle({self.x[0].coordinates}, {self.x[1].coordinates}, {self.x[2].coordinates})"
