# Exploration : le noeud borromeen enroule autour de chacun de ses quatre axes (les sommets du tetraedre).
# Autour d'un axe, on repere chaque point par son angle, sa distance a l'axe et sa hauteur le long de l'axe.
import itertools, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures'))
import figures as f

def cylindre(v, nom, n=2400):
    u, w, a = f.repere(v); p = f.rond(nom, n)
    x, y, h = p @ u, p @ w, p @ a
    return np.unwrap(np.arctan2(y, x)), np.hypot(x, y), h

print("1. Chaque rond fait-il un tour, et un seul, autour de chaque axe, sans revenir en arriere ?")
for v in f.SOMMETS[+1] + f.SOMMETS[-1]:
    ligne = []
    for nom in "RSI":
        th, rho, h = cylindre(v, nom); d = np.diff(th)
        tours = (th[-1] - th[0] + d.mean()) / (2 * np.pi)
        ligne.append(f"{nom}: {tours:+.0f} tour, monotone={bool(np.all(d > 0) or np.all(d < 0))}, distance a l'axe entre {rho.min():.2f} et {rho.max():.2f}")
    print("   axe", f.nom_quadrant(v), "|", " ; ".join(ligne))

print("\n2. Sens de chaque rond autour de chaque axe, les ronds etant orientes pour tourner tous les trois dans le meme sens autour de (+,+,+)")
ref = {nom: np.sign(np.diff(cylindre((1, 1, 1), nom)[0]).mean()) for nom in "RSI"}
table = {}
for v in f.SOMMETS[+1] + f.SOMMETS[-1]:
    s = {nom: int(np.sign(np.diff(cylindre(v, nom)[0]).mean()) * ref[nom]) for nom in "RSI"}; table[v] = s
    print("   axe", f.nom_quadrant(v), "|", "  ".join(f"{nom} {'+' if s[nom] > 0 else '-'}" for nom in "RSI"), "| nombre de ronds dans le sens de depart :", sum(1 for x in s.values() if x > 0))

print("\n3. Lecture sur le placement propose (tous au sommet (+,+,+))")
H2v = {(1, 1, 1): "tous", (-1, -1, 1): "pas-toute", (1, -1, -1): "exception", (-1, 1, -1): "pas d'exception"}
for v, nomf in H2v.items():
    s = table[v]; print(f"   {nomf:16} | Reel {'avance' if s['R'] > 0 else 'recule'} | Symbolique {'avance' if s['S'] > 0 else 'recule'} | Imaginaire {'avance' if s['I'] > 0 else 'recule'}")

# 4. Dessin : la tresse vue autour de deux axes
def tresse(ax, v, titre):
    for nom in "RSI":
        th, rho, h = cylindre(v, nom)
        sens = table[v][nom]; th = (th - th.min()); segs = []
    courbes = {}
    for nom in "RSI":
        th, rho, h = cylindre(v, nom); th = np.mod(th, 2 * np.pi); o = np.argsort(th); courbes[nom] = (th[o], h[o], rho[o])
    segs = []
    for nom, (th, h, rho) in courbes.items():
        for i in range(len(th) - 1): segs.append(((rho[i] + rho[i + 1]) / 2, nom, (h[i], h[i + 1]), (th[i], th[i + 1])))
    segs.sort(key=lambda s: s[0])
    for z, nom, xs, ys in segs:
        ax.plot(xs, ys, color="white", lw=7, solid_capstyle="butt", zorder=2 + z); ax.plot(xs, ys, color=f.COUL[nom], lw=3.2, zorder=2.01 + z)
    for nom, (th, h, rho) in courbes.items():
        i = len(th) // 2; s = table[v][nom]; j = i + 40 * s
        ax.annotate("", xy=(h[j], th[j]), xytext=(h[i], th[i]), arrowprops=dict(arrowstyle="-|>", color=f.COUL[nom], lw=0, mutation_scale=22), zorder=30)
    ax.set_title(titre, fontsize=10.5); ax.set_ylim(-0.1, 2 * np.pi + 0.1); ax.set_xlim(-2.2, 2.2)
    ax.set_yticks([0, 2 * np.pi]); ax.set_yticklabels(["départ", "un tour"]); ax.set_xticks([]); ax.set_xlabel("le long de l'axe")
    for sp in ("top", "right", "bottom"): ax.spines[sp].set_visible(False)

fig, axs = plt.subplots(1, 2, figsize=(11, 6.4))
tresse(axs[0], (1, 1, 1), "Autour de l'axe du sommet (+, +, +) :\nles trois ronds tournent dans le même sens")
tresse(axs[1], (-1, -1, 1), "Autour de l'axe du sommet (−, −, +) :\nle Réel avance, les deux autres reculent")
for i, nom in enumerate("RSI"): fig.text(0.25 + i * 0.2, 0.02, "━ " + f.NOMR[nom], color=f.COUL[nom], fontsize=10)
fig.suptitle("Le nœud déroulé autour de deux de ses quatre axes", fontsize=12.5, weight="bold")
fig.savefig("exploration_noeud_deroule_autour_d_un_axe.png", dpi=170, bbox_inches="tight", facecolor="white"); print("\necrit exploration_noeud_deroule_autour_d_un_axe.png")
