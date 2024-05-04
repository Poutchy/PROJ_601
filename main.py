# import polyscope as ps

# from recherche.wavefront import load_obj

# obj = load_obj( 'Mesh/spot.obj')
# ps.init()
# ps_mesh = ps.register_surface_mesh("spot", obj.only_coordinates(), obj.only_faces() )
# ps.show()


import polyscope as ps
import numpy as np

from recherche.wavefront import load_obj

name='Mesh/dodecahedron_poly'
obj_name=name+'.obj'
obj = load_obj( obj_name )
ps.init()
ps_mesh = ps.register_surface_mesh(name, obj.only_coordinates(), obj.only_faces() )
bdry  = obj.numpy_boundary_edges()
ps_net= ps.register_curve_network("boundary", obj.only_coordinates(), bdry )
ps.show()
