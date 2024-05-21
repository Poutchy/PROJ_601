from typing import Any
from numpy.linalg import norm
from numpy import zeros, cross, ndarray
from math import isnan

class Point():
    def __init__(self, coordinates: ndarray):
        self.coordinates = coordinates
        self.faces = []
        self.normal = 0

    def add_face(self, face):
        self.faces.append(face)

    def __str__(self):
        return f"Point({self.coordinates}), {self.normal}"

    def calculate_normal(self):
        """Calcul de sa normale par rapport à ses faces.
        On considère que toute les faces sont triangulaires."""
        normal = zeros(3)
        for face in self.faces:
            if face.x[0].coordinates.all() == self.coordinates.all():
                p1, p2 = face.x[1], face.x[2]
            if face.x[1].coordinates.all() == self.coordinates.all():
                p1, p2 = face.x[0], face.x[2]
            if face.x[2].coordinates.all() == self.coordinates.all():
                p1, p2 = face.x[0], face.x[1]
            # On calcule le vecteur normal de la face
            a = self.coordinates - p1.coordinates
            b = self.coordinates - p2.coordinates
            normal += cross(a, b)
        self.normal = normal / norm(normal)
        for el in self.normal:
            if isnan(el):
                self.normal = [0, 0, 0]
                break
