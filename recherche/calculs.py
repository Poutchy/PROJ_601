from numpy import cross, dot


class Calculs:
    @classmethod
    def detX(u, v, w):
        c = cross(v, w)
        return dot(u, c)


    @classmethod
    def u_(u):
        return 1/3 * (u.i + u.j + u.k)


    @classmethod
    def corrected_area_density(T):
        x = T.x()
        u = T.u()
        xi, xj, xk = x.i, x.j, x.k
        return Calculs.detX(Calculs.u_(u), (xj - xk), (xk - xi))


    @classmethod
    def corrected_curvature_density(T):
        x = T.x()
        u = T.u()
        xi, xj, xk = x.i, x.j, x.k
        ui, uj, uk = u.i, u.j, u.k
        temp = cross((uk - ui), xi) + cross((ui - uk), xj) + cross((uj - ui), xk)
        return dot(Calculs.u_(u), temp)


    @classmethod
    def corrected_gaussian_curvature_density(T):
        u = T.u()
        ui, uj, uk = u.i, u.j, u.k
        return dot(ui, cross(uj, uk))


    @classmethod
    def corrected_second_fundamental_form(T, X, Y):
        x = T.x()
        u = T.u()
        xi, xj, xk = x.i, x.j, x.k
        ui, uj, uk = u.i, u.j, u.k
        def calcul_temporaire(u1, u2):
            return dot(Y, (u1 - u2)) * X
        e1 = 1/2 * Calculs.detX(calcul_temporaire(uk, ui), (xj - xi))
        e2 = 1/2 * Calculs.detX(calcul_temporaire(uj, ui), (xk - xi))

        return e1/2 - e2/2


    @classmethod
    def w(*args):
        if (isinstance(args["i"], int)):
            match args["i"]:
                case 0:
                    return Calculs.corrected_area_density(args["T"])
                case 1:
                    return Calculs.corrected_curvature_density(args["T"])
                case 2:
                    return Calculs.corrected_gaussian_curvature_density(args["T"])
        return Calculs.corrected_second_fundamental_form(args["X"], args["Y"])


    @classmethod
    def corrected_mean_curvature(V):
        return Calculs.w(i = 1, T = V) / Calculs.w(i = 0, T = V)


    @classmethod
    def corrected_gaussian_curvature(V):
        return Calculs.w(i = 2, T = V) / Calculs.w(i = 0, T = V)
