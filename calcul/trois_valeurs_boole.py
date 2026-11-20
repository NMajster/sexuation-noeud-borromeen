# Logique a trois valeurs dans l'algebre que Lacan ecrit le 14 mai 1974 (p. 194-197) :
#   x(1-x) = 0  (Boole, x = x^2)   puis   x(1-x)(1+x) = 0  (x = x^3), le troisieme facteur s'ecrivant aussi -(1+x) = (-1-x).
# x = x^3 est vrai de tout element du corps a trois elements {0, 1, -1}. On calcule donc dans ce corps.
# Trois involutions sur les valeurs, chacune fixant une valeur :
#   n1(x) = 1 - x   echange 0 et 1, fixe -1   : le "pas exclusif" de Boole
#   n2(x) = -1 - x  echange 0 et -1, fixe 1   : le terme que Boole ecarte, ecrit par Lacan p. 197
#   n3(x) = -x      echange 1 et -1, fixe 0   : non ecrit par Lacan
# AUCUNE convention n'est choisie : on enumere les 27 facons d'ecrire les quatre formules avec ces negations.
#   tous            T = produit des Phi(x)                      (Boole : l'intersection est le produit)
#   exception       E = m( produit des m(nf(Phi(x))) )          (Boole : "il existe" par dualite, avec la negation m)
#   pas-tout        P = nq(T)        pas d'exception  N = nq(E)
#   nf = barre sur la fonction, nq = barre sur le quanteur, m = negation de la dualite.
# Une formule "tient" quand elle vaut 1. On cherche, sur tous les domaines de 1 a 5 elements, quelles formules tiennent ensemble.
import itertools
def mod(x): return ((x + 1) % 3) - 1
NEG = {"1-x": lambda x: mod(1 - x), "-1-x": lambda x: mod(-1 - x), "-x": lambda x: mod(-x)}
def prod(v):
    p = 1
    for a in v: p = mod(p * a)
    return p
def mondes(nf, nq, m, valeurs, nmax=5):
    out = set()
    for n in range(1, nmax + 1):
        for phi in itertools.combinations_with_replacement(valeurs, n):
            T = prod(phi); E = NEG[m](prod([NEG[m](NEG[nf](a)) for a in phi]))
            P = NEG[nq](T); N = NEG[nq](E)
            out.add("".join(k for k, v in zip("TEPN", (T, E, P, N)) if v == 1))
    return out
def paires(ms):
    d = {}
    for a, b in [("T", "E"), ("P", "N"), ("T", "N"), ("E", "P"), ("T", "P"), ("E", "N")]:
        d[a + b] = any(a in w and b in w for w in ms)
    return d

print("Temoin : Boole a deux valeurs {0,1}, les trois negations egales a 1-x")
print("   mondes :", sorted(mondes("1-x", "1-x", "1-x", (0, 1))))
print()
print("Les 27 ecritures, a trois valeurs. Colonnes : cote homme (T et E ensemble), cote femme (P et N ensemble),")
print("couples d'Aristote (T et N ; E et P), contradictoires (T et P ; E et N). o = possible, . = impossible")
print(f"{'barre fonction':15}{'barre quanteur':15}{'dualite':9}| TE PN | TN EP | TP EN | mondes")
bons = []
for nf, nq, m in itertools.product(NEG, repeat=3):
    ms = mondes(nf, nq, m, (0, 1, -1)); p = paires(ms)
    s = lambda k: "o " if p[k] else ". "
    print(f"{nf:15}{nq:15}{m:9}| {s('TE')}{s('PN')} | {s('TN')}{s('EP')} | {s('TP')}{s('EN')} | {' '.join(sorted(w or '-' for w in ms))}")
    # Ce que Lacan demande : les deux cotes tiennent ; une formule et sa barree ne tiennent jamais ensemble ;
    # le pas-tout peut tenir sans l'exception (10 avril 1973 ; 11 mars 1975).
    pas_tout_sans_exception = any("P" in w and "E" not in w for w in ms)
    if p["TE"] and p["PN"] and not p["TP"] and not p["EN"] and pas_tout_sans_exception:
        bons.append((nf, nq, m, sorted(ms)))
print()
print("Ecritures ou : les deux cotes tiennent, une formule et sa barree ne tiennent jamais ensemble,")
print("et le pas-tout peut tenir sans l'exception :", len(bons), "sur 27")
for b in bons: print("   barre fonction", b[0], "| barre quanteur", b[1], "| dualite", b[2], "| mondes", " ".join(w or "-" for w in b[3]))
print()
print("Meme recherche sans exiger le cote homme (T et E ensemble) :")
for nf, nq, m in itertools.product(NEG, repeat=3):
    ms = mondes(nf, nq, m, (0, 1, -1)); p = paires(ms)
    if p["PN"] and not p["TP"] and not p["EN"] and any("P" in w and "E" not in w for w in ms):
        print("   barre fonction", nf, "| barre quanteur", nq, "| dualite", m, "| cote homme :", "oui" if p["TE"] else "non", "| mondes", " ".join(sorted(w or "-" for w in ms)))
