# Le noeud borromeen colorie oriente (Soury, Chaines et noeuds, texte 3) :
#  - est-il invariant par les « inversions paires » (inverser l'orientation de deux ronds) ?
#  - l'est-il par les inversions impaires ? (Soury dit ne pas l'avoir demontre.)
# On liste toutes les isometries du complementaire donnees par SnapPy, leur action sur les ronds
# (permutation des couleurs), sur l'orientation de chaque rond, et sur l'orientation de l'espace.
import snappy, spherogram, collections, itertools
L = spherogram.Link(braid_closure=[1, -2, 1, -2, 1, -2])
M = L.exterior()
print("ronds :", len(L.link_components), "| volume :", round(float(M.volume()), 6), "|", M.identify()[:2])
G = M.symmetry_group()
print("groupe de symetries :", G, "| ordre", G.order(), "| declare complet :", G.is_full_group())
vus = collections.Counter()
for essai in range(6):
    N = L.exterior()
    for e in range(essai): N.randomize()
    for iso in N.is_isometric_to(N, return_isometries=True):
        if not iso.extends_to_link(): continue
        perm = tuple(iso.cusp_images()); mats = iso.cusp_maps()
        dets = [int(m.det()) for m in mats]
        assert len(set(dets)) == 1
        espace = "conserve" if dets[0] == 1 else "miroir"
        # orientation du rond : signe de l'image de la longitude sur la longitude
        sens = tuple(int(m[1, 1]) for m in mats)
        assert all(abs(s) == 1 and m[0, 1] == 0 and m[1, 0] == 0 for s, m in zip(sens, mats)), mats
        vus[(perm, sens, espace)] += 1
print("isometries distinctes (permutation, sens des ronds, espace) :", len(vus))
def parite(p): return sum(1 for i, j in itertools.combinations(range(3), 2) if p[i] > p[j]) % 2
tab = collections.defaultdict(set)
for (perm, sens, espace) in vus:
    nb_inv = sum(1 for s in sens if s == -1)
    tab[("couleurs fixes" if perm == (0, 1, 2) else ("permutation circulaire" if parite(perm) == 0 else "echange de deux couleurs"), espace)].add(nb_inv)
for k in sorted(tab): print("  ", k, ": nombre de ronds dont l'orientation est inversee :", sorted(tab[k]))
fix = sorted({(sens, espace) for (perm, sens, espace) in vus if perm == (0, 1, 2)})
print("couleurs fixes, detail :"); [print("   sens", s, "| espace", e) for s, e in fix]
