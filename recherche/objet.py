from numpy import mean, float64, zeros

from recherche.triangle import Triangle
from recherche.point import Point
from recherche.calculs import corrected_gaussian_curvature

class Objet():
    def __init__(self, object):
        self.points = object.only_coordinates()
        self.faces = object.only_faces()
        self.usables_points = [Point(point) for point in self.points]
        print("nb faces", len(self.faces))
        print("nb_points", len(self.points))
        self.boundary_edges = object.numpy_boundary_edges()
        self.boundary_vertices = object.boundary_vertices()
        self.set_faces()
        print(self.faces, "\n\n\n\n\n")
        print(self.points)
        self.set_points()

        print("nb faces", len(self.faces))
        print("nb_points", len(self.usables_points))

        for t in self.faces:
            print(corrected_gaussian_curvature(t))

    def set_faces(self):
        new_faces = []
        for face in self.faces:
            if len(face) == 3:
                p1, p2, p3 = self.usables_points[face[0]], self.usables_points[face[1]], self.usables_points[face[2]]
                t = Triangle([p1, p2, p3])
                t.set_ids([face[0], face[1], face[2]])
                new_faces.append(t)
            else:
                id_new_point = len(self.points)
                new_point = zeros((3, 1), float64)
                values = mean([self.points[point]
                                    for point in face], axis=0)
                for i in range (len(values)):
                    new_point[i] = values[i]
                new_point = Point(new_point)
                self.usables_points.append(new_point)
                for i in range(len(face)):
                    t = Triangle(
                        [self.usables_points[face[i]], self.usables_points[face[(i+1) % len(face)]], new_point])
                    t.set_ids([face[i], face[(i+1) % len(face)], id_new_point])
                    new_faces.append(t)
        self.faces = new_faces

    def set_points(self):
        for face in self.faces:
            for id in face.ids:
                self.usables_points[id].add_face(face)
        self.set_normals()

    def set_normals(self):
        for point in self.usables_points:
            point.calculate_normal()
        for f in self.faces:
            f.set_u([ self.usables_points[f.ids[0]].normal,
                self.usables_points[f.ids[1]].normal,
                self.usables_points[f.ids[2]].normal])
            print(f.u)
