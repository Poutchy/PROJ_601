from numpy import cross, dot


class Calculs:
    @classmethod
    def w(*args, **kwargs):
        if (isinstance(kwargs["i"], int)):
            match kwargs["i"]:
                case 0:
                    return corrected_area_density(kwargs["T"])
                case 1:
                    return corrected_curvature_density(kwargs["T"])
                case 2:
                    return corrected_gaussian_curvature_density(kwargs["T"])
        return corrected_second_fundamental_form(kwargs["T"], kwargs["X"], kwargs["Y"])

    @classmethod
    def corrected_mean_curvature(V):
        return Calculs.w(i=1, T=V) / Calculs.w(i=0, T=V)


def corrected_gaussian_curvature(V):
    print("gaussian density", Calculs.w(i=2, T=V))
    print("area density", Calculs.w(i=0, T=V))
    return "corrected gaussian curvature", Calculs.w(i=2, T=V) / Calculs.w(i=0, T=V)


def corrected_second_fundamental_form(T, X, Y):
    x = T.x
    u = T.u
    xi, xj, xk = x[0].coordinates, x[1].coordinates, x[2].coordinates
    ui, uj, uk = u[0], u[1], u[2]

    def calcul_temporaire(u1, u2):
        return dot(Y, (u1 - u2)) * X
    e1 = 1/2 * detX(calcul_temporaire(uk, ui), (xj - xi))
    e2 = 1/2 * detX(calcul_temporaire(uj, ui), (xk - xi))

    return e1/2 - e2/2


def corrected_curvature_density(T):
    x = T.x
    u = T.u
    xi, xj, xk = x[0].coordinates, x[1].coordinates, x[2].coordinates
    ui, uj, uk = u[0], u[1], u[2]
    temp = cross((uk - ui), xi) + cross((ui - uk), xj) + cross((uj - ui), xk)
    return 1/2 * dot(u_(u), temp)


def detX(u, v, w):
    c = cross(v, w)
    return dot(u, c)


def u_(u):
    print("u", u)
    print("ui + uj", u[0] + u[1])
    temp = (u[0] + u[1] + u[2])
    return 1/3 * temp


def corrected_area_density(T):
    x = T.x
    u = T.u
    xi, xj, xk = x[0].coordinates, x[1].coordinates, x[2].coordinates
    return 1/2 * detX(u_(u), (xj - xk), (xk - xi))


def corrected_gaussian_curvature_density(T):
    u = T.u
    ui, uj, uk = u[0], u[1], u[2]
    return 1/2 * dot(ui, cross(uj, uk))
