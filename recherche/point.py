from typing import Any
from numpy import zeros, cross, ndarray, add, array_equal
from math import isnan


class Point():
    def __init__(self, coordinates: ndarray):
        self.coordinates = coordinates
        self.faces = []
        self.normal = None

    def add_face(self, face):
        self.faces.append(face)

    # def __str__(self):
    #     return f"Point({self.coordinates}), {self.normal}"

    def calculate_normal(self):
        """Calcul de sa normale par rapport à ses faces.
        On considère que toute les faces sont triangulaires."""
        if self.normal == None:
            normal = zeros(3)
            for face in self.faces:
                if array_equal(face.x[0].coordinates, self.coordinates):
                    p1, p2 = face.x[1], face.x[2]
                if array_equal(face.x[1].coordinates, self.coordinates):
                    p1, p2 = face.x[0], face.x[2]
                if array_equal(face.x[2].coordinates, self.coordinates):
                    p1, p2 = face.x[0], face.x[1]
                # On calcule le vecteur normal de la face
                a = self.coordinates - p1.coordinates
                b = self.coordinates - p2.coordinates
                normal += cross(a, b)
                # print("face", face)
                # print("a, b", a, b, "normal", cross(
                #     a, b), "point", self.coordinates, p1, p2)
            self.normal = normal
            # print(self.normal)
            # for i, e in enumerate(self.normal):
            #     self.normal[i] = e * 100
            for el in self.normal:
                if isnan(el):
                    self.normal = [0, 0, 0]
                    break

    def calculate_normal_moyenne(self):
        normal = zeros(3)
        for face in self.faces:
            if array_equal(face.x[0].coordinates, self.coordinates):
                p1, p2 = face.x[1], face.x[2]
            if array_equal(face.x[1].coordinates, self.coordinates):
                p1, p2 = face.x[0], face.x[2]
            if array_equal(face.x[2].coordinates, self.coordinates):
                p1, p2 = face.x[0], face.x[1]
            normal = add(normal, add(p1.normal, p2.normal))
        self.normal = normal
        for i, e in enumerate(self.normal):
            self.normal[i] = e * 100
        # print(self.normal)

    def verify_normal(self):
        # print(self.normal)
        if self.normal.all() == zeros(3).all():
            print("Normal nulle")
            self.calculate_normal_moyenne()

    def __str__(self):
        return f"{self.coordinates}"
