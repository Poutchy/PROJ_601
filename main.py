import polyscope as ps
import numpy as np

from recherche.wavefront import load_obj
from recherche.objet import Objet

name = 'Mesh/triple_vierbein'
obj_name = name + '.obj'

obj = load_obj(obj_name)

n_obj = Objet(obj)



ps.init()
ps_mesh = ps.register_surface_mesh(
    name, n_obj.only_coordinates(), n_obj.only_faces())
ps_mesh.add_color_quantity("curvature colors", n_obj.list_color, defined_on='faces')
bdry = obj.numpy_boundary_edges()
ps_net = ps.register_curve_network("boundary", n_obj.only_coordinates(), bdry)
ps.show()
