from numpy import mean, float64, zeros, array, int32

from recherche.triangle import Triangle
from recherche.point import Point
from recherche.calculs import corrected_gaussian_curvature, corrected_gaussian_curvature_somme, prepare_triangle


class Objet():
    def __init__(self, object):
        self.points = object.only_coordinates()
        self.faces = object.only_faces()
        self.usables_points = [Point(point) for point in self.points]
        self.new_points = []
        # print("nb faces", len(self.faces))
        # print("nb_points", len(self.points))
        self.boundary_edges = object.numpy_boundary_edges()
        self.boundary_vertices = object.boundary_vertices()
        self.set_faces()
        # print(self.faces, "\n\n\n\n\n")
        # print(self.points)
        self.set_points()

        self.prepare_faces()

        # print("nb faces", len(self.faces))
        # print("nb_points", len(self.usables_points))

        self.list_curvature = zeros(len(self.faces))
        self.list_curvature_somme = zeros(len(self.faces))
        self.list_gaussian = zeros(len(self.faces))
        self.list_area = zeros(len(self.faces))
        for i, face in enumerate(self.faces):
            # print("for face ", face, "we know: ")
            self.list_curvature[i] = corrected_gaussian_curvature(face)
            self.list_curvature_somme[i] = corrected_gaussian_curvature_somme(
                face)
            self.list_gaussian[i] = face.gaussian_density
            self.list_area[i] = face.area_density
        # print("couleurs: ", self.list_curvature)

        self.only_coordinates()
        self.only_faces()

    def set_faces(self):
        new_faces = []
        for face in self.faces:
            if len(face) == 3:
                p1, p2, p3 = self.usables_points[face[0]
                                                 ], self.usables_points[face[1]], self.usables_points[face[2]]
                t = Triangle([p1, p2, p3])
                t.set_ids([face[0], face[1], face[2]])
                new_faces.append(t)
            else:
                id_new_point = len(self.usables_points)
                values = mean([self.points[point]
                               for point in face], axis=0)
                new_point = array(values)
                new_point = Point(new_point)
                self.usables_points.append(new_point)
                self.new_points.append(new_point)
                for i in range(len(face)):
                    t = Triangle(
                        [self.usables_points[face[i]], self.usables_points[face[(i+1) % len(face)]], new_point])
                    # print("t", t.x[0].coordinates,
                    #       t.x[1].coordinates, t.x[2].coordinates)
                    t.set_ids([face[i], face[(i+1) % len(face)], id_new_point])
                    new_faces.append(t)
        self.faces = new_faces

    def only_coordinates(self):
        V = zeros((len(self.usables_points), 3), float64)
        for i in range(len(self.usables_points)):
            V[i][0] = self.usables_points[i].coordinates[0]
            V[i][1] = self.usables_points[i].coordinates[1]
            V[i][2] = self.usables_points[i].coordinates[2]
        # print(V)
        return V

    def only_faces(self):
        all_faces = []
        for f in self.faces:
            face = []
            for i in f.ids:
                face.append(i)
            all_faces.append(face)
        return all_faces

    def boundary_edges(self):
        bdry_e = set()
        darts = {}
        faces = self.only_faces()
        for f in faces:
            for i in range(len(f)):
                if (f[i] in darts):
                    darts[f[i]].append(f[(i+1) % len(f)])
                else:
                    darts[f[i]] = [f[(i+1) % len(f)]]
        for i, i_list in darts.items():
            for j in i_list:
                j_list = darts[j]
                if (not i in j_list):
                    bdry_e.add((j, i))
        return bdry_e

    def numpy_boundary_edges(self):
        edges = self.boundary_edges()
        np_edges = zeros((len(edges), 2), int32)
        k = 0
        for e in edges:
            np_edges[k][0] = e[0]
            np_edges[k][1] = e[1]
            k = k+1
        return np_edges

    def set_points(self):
        for face in self.faces:
            for id in face.ids:
                self.usables_points[id].add_face(face)
        self.set_normals()

    def set_normals(self):
        for point in self.usables_points:
            point.calculate_normal()
        for point in self.new_points:
            point.verify_normal()
        for f in self.faces:
            # print([self.usables_points[f.ids[0]].normal,
            #        self.usables_points[f.ids[1]].normal,
            #        self.usables_points[f.ids[2]].normal])
            f.set_u([self.usables_points[f.ids[0]].normal,
                     self.usables_points[f.ids[1]].normal,
                     self.usables_points[f.ids[2]].normal])
            # print(f.u)

    def prepare_faces(self):
        for f in self.faces:
            prepare_triangle(f)
            f.set_adjacent_faces()
