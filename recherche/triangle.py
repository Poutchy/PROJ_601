class Vector3:
        def __init__(self, vi, vj, vk) -> None:
            self.i = vi
            self.j = vj
            self.k = vk

class Triangle:
    def __init__(self) -> None:
        self.x = None
        self.u = None


    def make_x(self, xi, xj, xk):
        self.x = Vector3(xi, xj, xk)


    def make_u(self, ui, uj, uk):
        self.u = Vector3(ui, uj, uk)


    def x(self):
        return self.x


    def u(self):
        return self.u
