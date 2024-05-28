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
        """fonction qui permet de définir les indices des points du triangle dans la liste des points de l'objet
        """
        self.ids = l

    def set_u(self, vecteurs):
        """fonction qui permet de définir les vecteurs normaux aux côtés du triangle
        """
        self.u = vecteurs

    def set_adjacent_faces(self):
        """fonction qui permet de définir les faces adjacentes à la face
        """
        possible_faces = []
        for p in self.x:
            possible_faces.extend([f for f in p.faces if (
                f != self and f not in possible_faces)])
        self.adjacent_faces = possible_faces

    def __str__(self):
        return f"Triangle({self.x[0].coordinates}, {self.x[1].coordinates}, {self.x[2].coordinates})"
