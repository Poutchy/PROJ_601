from wavefront import WavefrontOBJ
import numpy as np


class Point():
    def __init__(self, coordinates: np.ndarray):
        self.coordinates = coordinates
        self.faces = []
        self.normal = 0

    def add_face(self, face):
        self.faces.append(face)

    def __str__(self):
        return f"Point({self.coordinates})"

    def calculate_normal(self):
        """Calcul de sa normale par rapport à ses faces.
        On considère que toute les faces sont triangulaires."""
        normal = np.zeros(3)
        for face in self.faces:
            # On calcule le vecteur normal de la face
            a = self.coordinates - face[0]
            b = self.coordinates - face[1]
            normal += np.cross(a, b)
        self.normal = normal / np.linalg.norm(normal)


class Triangle():
    def __init__(self, points: list):
        self.x = {"i": points[0], "j": points[1], "k": points[2]}
        self.u = {}

    def set_u(self, points):
        self.u = {"i": points[0].normal,
                  "j": points[1].normal, "k": points[2].normal}


class Objet():
    def __init__(self, object: WavefrontOBJ):
        self.points = object.only_coordinates()
        self.faces = object.only_faces()
        self.boundary_edges = object.numpy_boundary_edges()
        self.boundary_vertices = object.boundary_vertices()
        self.set_faces()
        self.set_points()

    def set_faces(self):
        """Pour chaque face
        Si une face n'est pas une triangle, on créer un nouveau point au centre de la face.
        Nous utilisons ensuite ce point pour créer autant de triangles que nécessaire pour remplacer la face."""
        new_faces = []
        for face in self.faces:
            if len(face) == 3:
                new_faces.append(
                    Triangle([self.points[face[0]], self.points[face[1]], self.points[face[2]]]))
            else:
                new_point = np.mean([self.points[point]
                                    for point in face], axis=0)
                for i in range(len(face)):
                    new_faces.append(Triangle(
                        [self.points[face[i]], self.points[face[(i+1) % len(face)]], new_point]))
        self.faces = new_faces

    def set_points(self):
        """Pour chaque point, on le transform en un objet Point, qui possède toutes les faces qu'il partage.
        Une fois que tous les points sont transformés, on peut les utiliser pour calculer les normales de chaque point."""
        self.points = [Point(point) for point in self.points]
        for face in self.faces:
            for point in face:
                self.points[point].add_face(face)
        self.set_normals()

    def set_normals(self):
        for point in self.points:
            point.calculate_normal()
