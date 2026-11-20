# Essai : un quadrant, l'oeil qui s'y place, et ce qu'il voit.
import itertools, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyArrowPatch
from figures import rond, repere, dessine_vue, COUL, NOMR, sauve

CAM = (1.75, -2.2, 1.05)                     # d'ou le dessinateur regarde la scene
U, W, V = repere(CAM)
def pr(p): p = np.asarray(p, float); return p @ U, p @ W, p @ V
C = 2.5                                      # demi-cote du cube
PLAN = {"R": [(1, 1, 0), (-1, 1, 0), (-1, -1, 0), (1, -1, 0)],      # plancher
        "S": [(0, 1, 1), (0, -1, 1), (0, -1, -1), (0, 1, -1)],      # un mur
        "I": [(1, 0, 1), (-1, 0, 1), (-1, 0, -1), (1, 0, -1)]}      # l'autre mur

def oeil(ax, pos, vers, taille=0.34):
    x, y, _ = pr(pos); cx, cy, _ = pr(vers); a = np.degrees(np.arctan2(cy - y, cx - x))
    ax.add_patch(Ellipse((x, y), 2.1 * taille, 1.15 * taille, angle=a + 90, fc="white", ec="black", lw=1.6, zorder=60))
    d = np.array([cx - x, cy - y]); d = d / np.linalg.norm(d)
    ax.add_patch(Circle((x + 0.12 * taille * d[0], y + 0.12 * taille * d[1]), 0.36 * taille, fc="#555555", ec="black", lw=0.8, zorder=61))
    ax.add_patch(FancyArrowPatch((x + 0.75 * taille * d[0], y + 0.75 * taille * d[1]), (x + 0.62 * (cx - x), y + 0.62 * (cy - y)),
                                 arrowstyle="-|>", mutation_scale=13, color="black", lw=1.1, ls=(0, (4, 3)), zorder=59))
    return x, y

def scene(ax):
    for nom in "RSI":                                                     # les trois plans, en teinte legere
        q = np.array(PLAN[nom], float) * C; x, y, _ = pr(q)
        ax.add_patch(Polygon(np.c_[x, y], closed=True, fc=COUL[nom], ec=COUL[nom], alpha=0.07, lw=0.8, zorder=1))
        ax.add_patch(Polygon(np.c_[x, y], closed=True, fill=False, ec=COUL[nom], alpha=0.55, lw=0.9, zorder=1.5))
    for a, b in itertools.combinations(list(itertools.product((-1, 1), repeat=3)), 2):   # le cube
        if sum(i != j for i, j in zip(a, b)) == 1:
            x, y, _ = pr(np.array([a, b]) * C); ax.plot(x, y, color="#aaaaaa", lw=0.8, zorder=1.2)
    for a, b in itertools.combinations(list(itertools.product((0, 1), repeat=3)), 2):   # un compartiment : celui du premier oeil
        if sum(i != j for i, j in zip(a, b)) == 1:
            x, y, _ = pr(np.array([a, b]) * C); ax.plot(x, y, color="#2ca02c", lw=1.5, ls=(0, (5, 2)), zorder=1.8)
    for d in np.eye(3):
        x, y, _ = pr(np.array([-d, d]) * C); ax.plot(x, y, color="#666666", lw=1.0, ls=(0, (1, 2)), zorder=1.9)
    segs = []
    for nom in "RSI":
        x, y, z = pr(rond(nom)); n = len(x)
        for i in range(n):
            j = (i + 1) % n; segs.append(((z[i] + z[j]) / 2, nom, (x[i], x[j]), (y[i], y[j])))
    for z, nom, xs, ys in sorted(segs, key=lambda s: s[0]):
        ax.plot(xs, ys, color="white", lw=5.6, solid_capstyle="butt", zorder=5 + z)
        ax.plot(xs, ys, color=COUL[nom], lw=2.8, solid_capstyle="round", zorder=5.01 + z)
    ax.set_aspect("equal"); ax.axis("off")

def sens(p):
    # Chaque rond se projette en une ellipse allongee. On lit dans quel sens on tourne pour aller,
    # par le plus court, du grand axe du Reel a celui du Symbolique, puis a celui de l'Imaginaire.
    ax_ = {}
    for n in "RSI":
        x, y, _ = p[n]; i = int(np.argmax(np.hypot(x, y))); ax_[n] = np.arctan2(y[i], x[i])
    out = [int(np.sign(np.sin(2 * (ax_[n] - ax_[m])))) for m, n in (("R", "S"), ("S", "I"), ("I", "R"))]
    assert len(set(out)) == 1, out
    return out[0]

fig = plt.figure(figsize=(12.6, 6.2))
ax = fig.add_axes([0.0, 0.04, 0.56, 0.9]); scene(ax)
A, B = np.array([1, 1, 1]) * C, np.array([-1, -1, -1]) * C
xa, ya = oeil(ax, A, (0, 0, 0)); xb, yb = oeil(ax, B, (0, 0, 0))
ax.text(xa + 0.35, ya + 0.25, "l'œil, dans un quadrant\n(le compartiment en vert)", fontsize=9.5, ha="left", va="bottom")
ax.text(xb - 0.35, yb - 0.25, "l'œil, dans le quadrant opposé", fontsize=9.5, ha="right", va="top")
ax.set_xlim(-5.6, 6.6); ax.set_ylim(-4.6, 5.0)
ax.set_title("Les trois plans, les huit quadrants, deux places pour l'œil", fontsize=10.5)
for k, (v, t) in enumerate((((1, 1, 1), "ce que voit le premier"), ((-1, -1, -1), "ce que voit le second"))):
    a = fig.add_axes([0.57 + k * 0.215, 0.24, 0.205, 0.52]); p = dessine_vue(a, v, lw=3.0); a.set_title(t, fontsize=10.5); s_ = sens(p); print(v, 'sens', s_)
    th = np.linspace(np.radians(200), np.radians(200 + s_ * 70), 60); r0 = 2.25
    a.plot(r0 * np.cos(th[:-4]), r0 * np.sin(th[:-4]), color=("#2ca02c", "#9467bd")[k], lw=2.0, zorder=40)
    a.add_patch(FancyArrowPatch((r0 * np.cos(th[-8]), r0 * np.sin(th[-8])), (r0 * np.cos(th[-1]), r0 * np.sin(th[-1])), arrowstyle="-|>", mutation_scale=16, color=("#2ca02c", "#9467bd")[k], lw=0, zorder=41))
fig.text(0.785, 0.2, "Le même nœud, mis à plat depuis deux quadrants opposés.\nLes deux dessins sont l'image l'un de l'autre dans un miroir.\nLa flèche va du rond bleu au noir, puis au rouge.", ha="center", va="top", fontsize=9.5, style="italic")
for i, (nom, quoi) in enumerate((("R", "plancher"), ("S", "un mur"), ("I", "l'autre mur"))):
    fig.text(0.04 + i * 0.17, 0.03, f"— {NOMR[nom]} ({quoi})", color=COUL[nom], fontsize=9.5)
sauve(fig, "fig22_un_quadrant_et_l_oeil.png")
