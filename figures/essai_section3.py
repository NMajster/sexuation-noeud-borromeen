# Essai pour la section 3 : le noeud deroule autour de chacun de ses quatre axes, avec deux flechages des ronds.
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import figures as f

def cylindre(v, nom, n=1500):
    u, w, a = f.repere(v); p = f.rond(nom, n)
    x, y, h = p @ u, p @ w, p @ a
    return np.unwrap(np.arctan2(y, x)), np.hypot(x, y), h
AXES = f.SOMMETS[+1]
ref = {nom: np.sign(np.diff(cylindre(AXES[0], nom)[0]).mean()) for nom in "RSI"}
def sens(v, fleches): return {nom: int(np.sign(np.diff(cylindre(v, nom)[0]).mean()) * ref[nom]) * fleches[nom] for nom in "RSI"}

def tresse(ax, v, fleches):
    courbes = {}
    thR, rhoR, hR = cylindre(v, "R"); depart = thR[np.argmax(hR)]            # meme origine des angles autour des quatre axes : le point le plus haut du Reel
    for nom in "RSI":
        th, rho, h = cylindre(v, nom); th = np.mod(th - depart + 0.5, 2 * np.pi); o = np.argsort(th); courbes[nom] = (th[o], h[o], rho[o])
    segs = []
    for nom, (th, h, rho) in courbes.items():
        for i in range(len(th) - 1): segs.append(((rho[i] + rho[i + 1]) / 2, nom, (h[i], h[i + 1]), (th[i], th[i + 1])))
    segs.sort(key=lambda s: s[0])
    for z, nom, xs, ys in segs:
        ax.plot(xs, ys, color="white", lw=6, solid_capstyle="butt", zorder=2 + z); ax.plot(xs, ys, color=f.COUL[nom], lw=2.8, zorder=2.01 + z)
    s = sens(v, fleches)
    for nom, (th, h, rho) in courbes.items():
        n = len(th); pente = np.abs(np.gradient(h))
        for a0, a1 in ((0.06, 0.46), (0.54, 0.94)):                          # une fleche par moitie, la ou le brin monte droit
            i0, i1 = int(n * a0), int(n * a1); i = i0 + int(np.argmin(pente[i0:i1])); k = 26
            x0, y0, x1, y1 = h[i - k], th[i - k], h[i + k], th[i + k]
            if s[nom] < 0: x0, y0, x1, y1 = x1, y1, x0, y0
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=f.COUL[nom], lw=0, mutation_scale=24), zorder=30)
    ax.set_ylim(-0.25, 2 * np.pi + 0.25); ax.set_xlim(-2.1, 2.1); ax.axis("off")
    return s

# l'exemple de placement est celui de la figure des quatre triangles (fig19) : sommet O = axe 1, S = axe 2, I = axe 3, R = axe 4
groupes = {}
for pl in f.tous_les_placements(): groupes.setdefault(f.attribution(pl), []).append(pl)
ex = groupes[("côtés", "lignes", "diagonales")][0]; EXEMPLE = [ex["O"], ex["S"], ex["I"], ex["R"]]
fig, axs = plt.subplots(2, 4, figsize=(12.5, 11.0))
for li, (fleches, titre) in enumerate((({"R": 1, "S": 1, "I": 1}, "Le nœud déroulé autour de chacun de ses quatre axes, les ronds étant fléchés"), ({"R": -1, "S": 1, "I": -1}, "Le même nœud, après avoir retourné les flèches du Réel et de l'Imaginaire"))):
    for k, v in enumerate(AXES):
        ax = axs[li][k]; s = tresse(ax, v, fleches)
        tous = len(set(s.values())) == 1
        if tous:
            ax.add_patch(FancyBboxPatch((0.02, 0.01), 0.96, 0.98, transform=ax.transAxes, boxstyle="round,pad=0.0,rounding_size=0.04", fc="#fff6d6", ec="#d4a100", lw=1.8, zorder=0, clip_on=False))
            txt = "les trois ronds montent" if s["R"] > 0 else "les trois ronds descendent"
        else:
            seul = [n for n in "RSI" if list(s.values()).count(s[n]) == 1][0]
            art = "l'" if seul == "I" else "le "
            txt = art + f.NOMR[seul] + (" monte," + chr(10) + "les deux autres descendent" if s[seul] > 0 else " descend," + chr(10) + "les deux autres montent")
        ax.text(0.5, -0.06, txt, transform=ax.transAxes, ha="center", va="top", fontsize=9.5)
        ax.text(0.5, 1.03, r"$\mathit{" + "abcd"[k] + "}$", transform=ax.transAxes, ha="center", va="bottom", fontsize=16, color="#444444")
        if li == 0: ax.text(0.5, 1.10, f"autour de l'axe {k + 1}", transform=ax.transAxes, ha="center", va="bottom", fontsize=10.5, color="#222222", weight="bold")
    fig.text(0.5, 0.965 - li * 0.478, titre, ha="center", fontsize=11.5, weight="bold")
for i, nom in enumerate("RSI"): fig.text(0.27 + i * 0.19, 0.012, "━ " + f.NOMR[nom], color=f.COUL[nom], fontsize=10)
fig.subplots_adjust(hspace=0.50, wspace=0.05, top=0.885, bottom=0.085)
fig.savefig("fig06_noeud_deroule_autour_de_ses_quatre_axes.png", dpi=190, bbox_inches="tight", facecolor="white"); print("ecrit fig06_noeud_deroule_autour_de_ses_quatre_axes.png")
