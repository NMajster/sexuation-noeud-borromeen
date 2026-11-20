# Les quatre formules sur les quatre ronds du noeud a quatre de Lacan (R, S, I et le quatrieme, note Sg).
# Donnee prise a l'etude sur les noeuds a quatre de 1975 (fiche technique, entrees 4 a 6, statut "demontre") :
#   le noeud a quatre ronds se decoupe par un tore en deux morceaux, ce qui range les ronds en deux couples,
#   (Sg, S) et (I, R) ; ses transformations en lui-meme permutent les ronds de huit facons, engendrees par
#   l'echange de Sg et S, l'echange de I et R, et l'echange des deux couples. Toute transformation respecte les couples.
# Question : combien de facons de mettre une formule par rond, a ces transformations pres ?
import itertools
RONDS = ("Sg", "S", "I", "R")
gens = [{"Sg": "S", "S": "Sg", "I": "I", "R": "R"}, {"Sg": "Sg", "S": "S", "I": "R", "R": "I"}, {"Sg": "I", "S": "R", "I": "Sg", "R": "S"}]
def compose(a, b): return {r: a[b[r]] for r in RONDS}
G = [{r: r for r in RONDS}]
while True:
    n = len(G)
    for g in list(G):
        for s in gens:
            h = compose(s, g)
            if h not in G: G.append(h)
    if len(G) == n: break
print("transformations du noeud (permutations des ronds) :", len(G))
couples_ronds = {frozenset(("Sg", "S")), frozenset(("I", "R"))}
assert all({frozenset(g[x] for x in c) for c in couples_ronds} == couples_ronds for g in G)

F = {"T": (0, 0), "P": (0, 1), "E": (1, 0), "N": (1, 1)}
NOM = {"T": "tous", "P": "pas-tout", "E": "exception", "N": "pas d'exception"}
def rangement(a, b):
    (f1, q1), (f2, q2) = F[a], F[b]
    return "lignes" if f1 == f2 else ("cotes" if q1 == q2 else "diagonales")
placements = [dict(zip(RONDS, p)) for p in itertools.permutations("TPEN")]
def cle(pl): return tuple(pl[r] for r in RONDS)
vus, orbites = set(), []
for pl in placements:
    if cle(pl) in vus: continue
    orb = {cle({g[r]: pl[r] for r in RONDS}) for g in G}
    vus |= orb; orbites.append((pl, len(orb)))
print("placements : 24 ; classes a transformation pres :", len(orbites))
for pl, n in orbites:
    print("  classe de", n, "placements | le couple (Sg, S) porte", NOM[pl["Sg"]], "et", NOM[pl["S"]], "| le couple (I, R) porte", NOM[pl["I"]], "et", NOM[pl["R"]],
          "| les couples du noeud sont les", rangement(pl["Sg"], pl["S"]), "du tableau")
print()
print("Rappel pour trois ronds : 24 placements sur les quatre quadrants, 6 classes.")
print("A quatre ronds : 3 classes, une par rangement des formules en couples (lignes, cotes, diagonales).")
print()
print("Si les couples du noeud sont les cotes du tableau, les 8 placements de la classe, avec les noms des ronds :")
for pl in placements:
    if rangement(pl["Sg"], pl["S"]) == "cotes":
        print("   Sg :", NOM[pl["Sg"]], "| S :", NOM[pl["S"]], "| I :", NOM[pl["I"]], "| R :", NOM[pl["R"]])
