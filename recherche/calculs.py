from numpy import cross, dot, add, array


def choix_calcul(*args, **kwargs):
    """fonction qui permet de choisir le calcul à effectuer

    Returns:
        voir les fonctions appelées
    """
    if (isinstance(kwargs["i"], int)):
        match kwargs["i"]:
            case 0:
                return corrected_area_density(kwargs["T"])
            case 1:
                return corrected_curvature_density(kwargs["T"])
            case 2:
                return corrected_gaussian_curvature_density(kwargs["T"])
    return corrected_second_fundamental_form(kwargs["T"], kwargs["X"], kwargs["Y"])


def corrected_mean_curvature(V):
    """fonction qui permet de calculer la courbure moyenne d'une face
    """
    return choix_calcul(i=1, T=V) / choix_calcul(i=0, T=V)


def corrected_gaussian_curvature(V):
    """fonction qui permet de calculer la courbure gaussienne d'une face
    """
    v3 = choix_calcul(i=2, T=V) / choix_calcul(i=0, T=V)
    return v3


def prepare_triangle(V):
    """fonction qui permet de préparer un triangle pour les calculs en lui attribuant les densités de courbure et d'aire
    """
    v1, v2 = choix_calcul(i=2, T=V), choix_calcul(i=0, T=V)
    V.gaussian_density, V.area_density = v1, v2


def corrected_gaussian_curvature_somme(V):
    """fonction qui permet de calculer la somme des courbures gaussiennes des faces adjacentes à la face en paramètre
    """
    gaussian = []
    area = []
    for f in V.adjacent_faces:
        gaussian.append(f.gaussian_density)
        area.append(f.area_density)
    gaussian.append(V.gaussian_density)
    area.append(V.area_density)
    return sum(gaussian) / sum(area)


def corrected_second_fundamental_form(T, X, Y):
    """fonction qui permet de calculer la seconde forme fondamentale corrigée d'une face
    """
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
    """fonction qui permet de calculer la densité de courbure corrigée d'une face
    """
    x = T.x
    u = T.u
    xi, xj, xk = x[0].coordinates, x[1].coordinates, x[2].coordinates
    ui, uj, uk = u[0], u[1], u[2]
    temp = cross((uk - ui), xi) + cross((ui - uk), xj) + cross((uj - ui), xk)
    return 1/2 * dot(u_(u), temp)


def detX(u, v, w):
    """fonction qui permet de calculer le déterminant de la matrice formée par les vecteurs u, v et w
    """
    c = cross(v, w)
    return dot(u, c)


def u_(u):
    """fonction qui permet de calculer u_ sur le vecteur normal u
    """
    u1, u2, u3 = array(u[0]), array(u[1]), array(u[2])
    temp = add(u1, add(u2, u3))
    return 1/3 * temp


def corrected_area_density(T):
    """fonction qui permet de calculer la densité d'aire corrigée d'une face
    """
    x = T.x
    u = T.u
    xi, xj, xk = x[0].coordinates, x[1].coordinates, x[2].coordinates
    return 1/2 * detX(u_(u), (xj - xk), (xk - xi))


def corrected_gaussian_curvature_density(T):
    """fonction qui permet de calculer la densité de courbure gaussienne corrigée d'une face
    """
    u = T.u
    ui, uj, uk = u[0], u[1], u[2]
    return 1/2 * dot(ui, cross(uj, uk))
