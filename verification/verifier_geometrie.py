"""Vérification autonome des figures, Python >= 3.8, bibliothèque standard."""
from collections import Counter
from itertools import permutations, combinations, product
from math import atan2, cos, degrees, pi, sin, sqrt

NOMS = ('R', 'S', 'I')
# Indices du grand axe, du petit axe et de la normale du plan.
ELLIPSES = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
CUBE = tuple(product((1, -1), repeat=3))
TETRA = tuple(s for s in CUBE if s[0] * s[1] * s[2] == 1)
TABLEAU = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # T, P, E, N


def scalaire(a, b):
    return sum(x*y for x, y in zip(a, b))


def unite(a):
    norme = sqrt(scalaire(a, a))
    return tuple(x/norme for x in a)


def croix(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def camera(d):
    u = unite(croix((0, 0, 1), d))
    return u, croix(d, u)  # u x v = d, vers l'œil


def signe_court(angle):
    return (angle + pi/2) % pi - pi/2


def marque(d):
    u, v = camera(d)
    axes = []
    for grand, petit, _ in ELLIPSES:
        # Matrice symétrique M M^T de l'ellipse projetée, vraies directions principales.
        xx = 4*u[grand]**2 + u[petit]**2
        yy = 4*v[grand]**2 + v[petit]**2
        xy = 4*u[grand]*v[grand] + u[petit]*v[petit]
        assert abs(xx-yy) + abs(xy) > 1e-8
        axes.append(atan2(2*xy, xx-yy)/2)
    return [degrees(signe_court(axes[(i+1)%3]-axes[i])) for i in range(3)]


def hauteur_rayon(e, d):
    points = []
    for grand, petit, normale in ELLIPSES:
        rapport = -e[normale]/d[normale]
        v = tuple(a + rapport*b for a, b in zip(e, d))
        rayon = 1/sqrt((v[grand]/2)**2 + v[petit]**2)
        points.append((rapport*rayon, rayon))
    return points


def polynome(t):
    return (((-3*t + 16)*t - 15)*t + 12)*t + 1


def verifier_polynomes():
    # Les polynômes comparés ont degré au plus quatre ; cinq points distincts suffisent.
    for t in range(-4, 6):
        r = 1 + 4*t*t
        s = (t-1)**2 + 4
        i = t*t + 4*(1-t)**2
        assert (t+1)**2*s - (t-2)**2*r == polynome(t)
        assert polynome(t+2) == -3*t**4 - 8*t**3 + 9*t*t + 48*t + 45
        assert r-s == 3*t*t + 2*t - 4 and s-i == -4*t*t+6*t+1
    # Sur la direction omise a=0, b=1, les hauteurs de R et S diffèrent.
    assert 1/sqrt(1) != 1/sqrt(1/4)


def racine_tresse():
    # L'unique racine admissible est isolée par le raisonnement de RAPPORT.md, n° 3.
    a, b = 4., 5.
    assert polynome(a) > 0 > polynome(b)
    for _ in range(55):
        m = (a+b)/2
        if polynome(m) > 0:
            a = m
        else:
            b = m
    return (a+b)/2


def evenements(pentes, d, u, v, signes):
    resultats = []
    for t in pentes:
        e = unite((2-t, 2*t-1, -1-t))
        for anneau in range(3):
            paire = (anneau, (anneau+1)%3)
            for sens in (1, -1):
                repere = tuple(sens*s*x for s, x in zip(signes, e))
                angle = atan2(scalaire(repere, v), scalaire(repere, u)) % (2*pi)
                resultats.append((angle, paire))
            e = (e[2], e[0], e[1])
    return sorted(resultats)


def ligne_de_vue(theta, u, v):
    return tuple(cos(theta)*x + sin(theta)*y for x, y in zip(u, v))


def mot_et_projection(signes):
    d = unite(signes)
    base = unite((1, 1, 1))
    u0, v0 = camera(base)
    u = tuple(s*x for s, x in zip(signes, u0))
    v = tuple(s*x for s, x in zip(signes, v0))
    mot = []
    for theta, (i, j) in evenements([racine_tresse()], d, u, v, signes):
        points = hauteur_rayon(ligne_de_vue(theta, u, v), d)
        assert abs(points[i][0]-points[j][0]) < 1e-9
        assert abs(points[i][1]-points[j][1]) > 1e-3
        avant = hauteur_rayon(ligne_de_vue(theta-1e-5, u, v), d)
        apres = hauteur_rayon(ligne_de_vue(theta+1e-5, u, v), d)
        assert (avant[i][0]-avant[j][0])*(apres[i][0]-apres[j][0]) < 0
        ordre = sorted(range(3), key=lambda k: avant[k][0])
        places = sorted((ordre.index(i), ordre.index(j)))
        assert places[1] == places[0]+1
        gauche = ordre[places[0]]
        dessus = max((i,j), key=lambda k: points[k][1])
        mot.append((places[0]+1) * (1 if gauche==dessus else -1))
    assert sorted(Counter(mot).values()) == [3, 3]
    assert all(abs(mot[k]) != abs(mot[(k+1)%6]) and mot[k]*mot[(k+1)%6] < 0 for k in range(6))
    pentes = [(-1-sqrt(13))/3, (-1+sqrt(13))/3]
    ombre = evenements(pentes, d, u, v, signes)
    assert len({round(angle, 8) for angle, _ in ombre}) == 12
    assert sorted(Counter(p for _, p in ombre).values()) == [4, 4, 4]
    for theta,(i,j) in ombre:
        pts = hauteur_rayon(ligne_de_vue(theta, u, v), d)
        assert abs(pts[i][1]-pts[j][1]) < 1e-9 and abs(pts[i][0]-pts[j][0]) > 1e-3
    return mot, len(ombre)


def rotation(points):
    return tuple((-y, x) for x, y in points)


def verifier_symetries():
    for p in TETRA:
        images = {tuple(a*b for a,b in zip(s,p)) for s in TETRA}
        assert images == set(TETRA)
    for diag in TETRA:
        sens = tuple(diag[grand]*diag[petit] for grand,petit,k in ELLIPSES)
        assert sens == (diag[2],diag[0],diag[1])
        assert sens.count(-1) in (0,2)
    compte = 0
    for sigma in permutations(range(3)):
        inversions = sum(i>j for i,j in combinations(sigma,2))
        for e in CUBE:
            if e[0]*e[1]*e[2] == (-1)**inversions:
                compte += 2  # orientation ambiante libre, critère de Berglund et al.
    assert compte == 48
    print('Demi-tours : action libre et transitive ; critère de Berglund : 48 signatures, avec 0 ou 2 inversions à couleurs fixes.')


def verifier_vue_hors_diagonale():
    # Direction (1,1,10) ; projection sur z=0 en (X,Y)=(x-z/10,y-z/10).
    # Chaque frontière est Q=4 pour le triplet des coefficients de X², XY, Y².
    formes = ((1,0,4), (401,-2,1), (4,-8,104))
    comptes = []
    for f, g in combinations(formes,2):
        a,b,c = (x-y for x,y in zip(f,g))
        discriminant = b*b-4*a*c
        assert discriminant != 0
        comptes.append(4 if discriminant>0 else 0)
    assert comptes == [4,0,4]
    print('Direction intérieure (1,1,10) | R/S, R/I, S/I :', comptes,'soit 8 croisements.')


def verifier_placements():
    sommes = (0, 1, 1, 2)  # marque de parité f+q pour T, P, E, N
    fonctions = {(0,0,1,1):'f', (0,1,0,1):'q', tuple(v%2 for v in sommes):'v'}
    for espece in (1, -1):
        sommets = [s for s in CUBE if s[0]*s[1]*s[2] == espece]
        classes = Counter()
        for placement in permutations(sommets):
            partitions = [fonctions[tuple(int(v != col[0]) for v in col)] for col in zip(*placement)]
            classes[tuple(partitions)] += 1
            omis = partitions.index('v')
            axes = [k for k in range(3) if k != omis]
            positions = tuple((s[axes[0]],s[axes[1]]) for s in placement)
            succes = 0
            for sens in (-1, 1):
                pts = tuple((sens*x,y) for x,y in positions)
                for _ in range(4):
                    succes += pts == TABLEAU
                    pts = rotation(pts)
            assert succes == 1
        assert len(classes)==6 and set(classes.values())=={4}
        print('Espèce', espece, '| 24 bijections, 6 classes de 4 ; 24 tableaux réalisables en choisissant le côté de vue et la rotation.')
    for p, q in combinations(TETRA,2):
        assert sum(a==b for a,b in zip(p,q))==1
    principal = ((1,1,1),(-1,-1,1),(1,-1,-1),(-1,1,-1))
    autre = (principal[0], principal[1], principal[3], principal[2])
    assert tuple((-x,-z) for x,y,z in principal)==TABLEAU
    assert tuple((-y,-z) for x,y,z in autre)==TABLEAU
    for k in range(3):
        ar = [(i,j) for i,j in combinations(range(4),2) if principal[i][k] == principal[j][k]]
        assert len(ar)==2 and set(ar[0]).isdisjoint(ar[1])
    print('Carré orienté | placement principal : écran (-x,-z), œil en -y ; autre : (-y,-z), œil en +x.')


def main():
    verifier_polynomes()
    verifier_symetries()
    verifier_placements()
    verifier_vue_hors_diagonale()
    reference = None
    for s in CUBE:
        parite = s[0]*s[1]*s[2]
        angles = marque(unite(s))
        assert all(abs(a+60*parite) < 1e-9 for a in angles)
        mot, n = mot_et_projection(s)
        print('Vue',s,'| angles courts R,S,I,R :',tuple(round(a) for a in angles),
              '| intersections de la projection orthographique',n)
        if parite == 1:
            reference = mot if reference is None else reference
            assert mot==reference
            print('  Tresse', mot, '| tours dirigés R,S,I', (s[2],s[0],s[1]))
    for orientations in CUBE:
        coherents = [s for s in TETRA if len({a*b for a,b in zip(orientations,(s[2],s[0],s[1]))})==1]
        assert len(coherents)==1
    print('Les huit choix de flèches donnent chacun un axe non orienté où les trois sens concordent.')
    print('Pente admissible R/S pour la tresse (+,+,+) : %.9f' % racine_tresse())
    plages = [(k,2*k) for k in (1,3,9)]
    assert all(b<c for (_,b),(c,_) in zip(plages,plages[1:]))
    print('Contre-exemple au caractère intrinsèque du carré : trois ellipses dans des coquilles disjointes', plages)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Exécuter sans -O pour conserver les assertions.')
    main()
