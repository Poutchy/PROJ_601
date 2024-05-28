import polyscope as ps

from recherche.wavefront import load_obj
from recherche.objet import Objet

name = 'Mesh/bunnyhead'
obj_name = name + '.obj'

obj = load_obj(obj_name)

n_obj = Objet(obj)


ps.init()
ps_mesh = ps.register_surface_mesh(
    name, n_obj.only_coordinates(), n_obj.only_faces())
ps_mesh.add_scalar_quantity(
    "curvature", n_obj.list_curvature, defined_on='faces')
ps_mesh.add_scalar_quantity(
    "curvature somme", n_obj.list_curvature_somme, defined_on='faces')
ps_mesh.add_scalar_quantity(
    "gaussian", n_obj.list_gaussian, defined_on='faces')
ps_mesh.add_scalar_quantity(
    "area", n_obj.list_area, defined_on='faces')
bdry = obj.numpy_boundary_edges()
ps_net = ps.register_curve_network("boundary", n_obj.only_coordinates(), bdry)
ps.show()
