"""Contrôles du carré formel, de la lecture classique et des modèles finis. Python 3.8+."""
from itertools import product

FORMULES = {(0,0): 'T', (0,1): 'P', (1,0): 'E', (1,1): 'N'}
DEPLACEMENTS = {'f': (1,0), 'q': (0,1), 'f+q': (1,1)}


def somme(x, y):
    return x[0]^y[0], x[1]^y[1]


def verifier_klein():
    for a in DEPLACEMENTS.values():
        assert somme(a,a) == (0,0)
        for b in DEPLACEMENTS.values():
            assert somme(a,b) == somme(b,a)
            if a != b:
                assert somme(a,b) in set(DEPLACEMENTS.values()) - {a,b}
    for nom, d in DEPLACEMENTS.items():
        paires = [(FORMULES[x], FORMULES[somme(x,d)]) for x in FORMULES if x < somme(x,d)]
        fixe = {k for k in ('f','q','v') if {'f':d[0],'q':d[1],'v':d[0]^d[1]}[k] == 0}
        assert len(fixe)==1
        print('Geste',nom,'|',paires,'| marque conservée',fixe.pop())


def verifier_classique():
    motifs = set()
    for n in (1,2,3,4):
        for valeurs in product((False, True),repeat=n):
            t = all(valeurs)
            e = any(not a for a in valeurs)
            etat = {'T':t,'P':not t,'E':e,'N':not e}
            for x, s in FORMULES.items():
                for nom, geste in DEPLACEMENTS.items():
                    arrivee = FORMULES[somme(x, geste)]
                    assert etat[arrivee] == (etat[s] if nom == 'f+q' else not etat[s])
            motifs.add(''.join(s for s in 'TPEN' if etat[s]))
    print('Classique | groupes vrais :',sorted(motifs),'| f et q complémentent, f+q conserve la valeur.')


def profil_kripke(futurs, predicats):
    mondes = set(futurs)
    for pred in predicats:
        assert all(futurs[w] <= pred for w in pred)
    def neg(ouvert):
        return {w for w in mondes if futurs[w].isdisjoint(ouvert)}
    t = mondes.intersection(*predicats)
    e = set().union(*(neg(ouvert) for ouvert in predicats))
    p, n = neg(t), neg(e)
    assert t <= n and e <= p and not t & e
    assert n == mondes.intersection(*(neg(neg(a)) for a in predicats))
    return dict(zip('TPEN',(t,p,e,n)))


def verifier_kripke():
    tous = {'racine','gauche','droite'}
    fourche = {'racine':tous,'gauche':{'gauche'},'droite':{'droite'}}
    r = profil_kripke(fourche,[{'gauche'},{'droite'}])
    assert r == {'T':set(),'P':tous,'E':{'gauche','droite'},'N':set()}
    print('Fourche, domaine fixe {a,b} | la racine force P ; aucun témoin de E à la racine.')
    chaine = {'avant':{'avant','après'},'après':{'après'}}
    r = profil_kripke(chaine,[{'après'}])
    assert 'avant' in r['N'] and 'avant' not in r['T']
    print('Chaîne à deux mondes, singleton | la racine force N et ne force pas T.')
    un_monde = {'unique':{'unique'}}
    r = profil_kripke(un_monde,[{'unique'}])
    assert r['P'] == set() and r['N'] == {'unique'}
    print('Modèle classique à un monde, prédicat toujours vrai | P est faux, indépendamment du cardinal du domaine non vide.')


def verifier_heyting():
    # Code des trois éléments 0, h, 1 par 0, 1, 2 dans cet ordre.
    def non(a):
        return 2 if a == 0 else 0
    profils = set()
    for drapeaux in product((False,True),repeat=3):
        ensemble = [a for a,pris in enumerate(drapeaux) if pris]
        if ensemble:
            t = min(ensemble)
            e = max(map(non,ensemble))
            profils.add((t,non(t),e,non(e)))
    assert all(p==e for t,p,e,n in profils)
    assert (1,0,0,2) in profils and max(1,non(1))==1
    print('H3 | P=E pour les 7 images non vides du prédicat ; h ou non-h vaut h, distinct du sommet.')


def verifier_paraconsistance():
    # Paire de preuves positive, négative ; une première composante vraie est désignée.
    preuve_double = (True,True)
    negation = preuve_double[::-1]
    assert preuve_double[0] and negation[0]
    print('Contre-exemple à « aucune logique » | une valeur à la fois vraie et fausse et sa négation sont désignées.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Exécuter sans -O pour conserver les assertions.')
    verifier_klein()
    verifier_classique()
    verifier_kripke()
    verifier_heyting()
    verifier_paraconsistance()
    print('Le modèle à domaine infini est démontré au n° 9 du rapport. Aucun segment fini ne le remplace.')
