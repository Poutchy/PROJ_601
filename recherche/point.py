from typing import Any
from numpy import zeros, cross, ndarray, add, array_equal
from math import isnan


class Point():
    def __init__(self, coordinates: ndarray):
        self.coordinates = coordinates
        self.faces = []
        self.normal = None

    def add_face(self, face):
        """fonction qui permet d'ajouter une face à la liste des faces du point"""
        self.faces.append(face)

    def calculate_normal(self):
        """Calcul de sa normale par rapport à ses faces.
        On considère que toute les faces sont triangulaires.
        """
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
            self.normal = normal
            for el in self.normal:
                if isnan(el):
                    self.normal = [0, 0, 0]
                    break

    def calculate_normal_moyenne(self):
        """Calcul de sa normale par rapport à ses faces.
        On considère que toute les faces sont triangulaires.
        """
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

    def verify_normal(self):
        """Vérifie si la normale du point est nulle
        Si elle l'est, on la recalcule par rapport aux moyennes des normales des points adjacents
        """
        if self.normal.all() == zeros(3).all():
            print("Normal nulle")
            self.calculate_normal_moyenne()

    def __str__(self):
        return f"{self.coordinates}"
