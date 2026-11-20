# Les placements dessines sur le tableau des formules, et le tableau retrouve dans le noeud vu selon l'axe d'un rond.
import itertools, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figures import Q, LQ, FORM, NOMF, NOMR, COUL, LIG, COT, DIA, SOM, H2, rond, couleur_arete, sauve

def tableau(ax, attribution, titre=None, lw=6.5):
    for nom in "IRS":                                                     # diagonales dessous, cotes et lignes dessus
        for a, b in attribution[nom]: ax.plot(*zip(Q[a], Q[b]), color=COUL[nom], lw=lw, solid_capstyle="round", zorder=2)
    for s in "ENTP":
        x, y = Q[s]; g = x == 0
        ax.scatter(x, y, s=170, color="white", edgecolor="#555555", zorder=3)
        ax.text(x + (-0.13 if g else 0.13), y + 0.075, FORM[s], ha="right" if g else "left", va="center", fontsize=14, zorder=4)
        ax.text(x + (-0.13 if g else 0.13), y - 0.115, NOMF[s].replace(chr(10), " "), ha="right" if g else "left", va="center", fontsize=9.5, zorder=4)
    ax.text(0, 1.26, "côté homme", ha="center", fontsize=9.5, color="#666666"); ax.text(LQ, 1.26, "côté femme", ha="center", fontsize=9.5, color="#666666")
    if titre: ax.set_title(titre, fontsize=11, pad=6)
    ax.set_xlim(-1.8, LQ + 1.8); ax.set_ylim(-0.32, 1.42); ax.set_aspect("equal"); ax.axis("off")

def legende(fig, y, x0=0.17, pas=0.25):
    for i, nom in enumerate("RSI"):
        fig.text(x0 + i * pas, y, "━ " + ("l'" if nom == "I" else "le ") + NOMR[nom] + " ne bouge pas", color=COUL[nom], fontsize=10)

def fig08():
    fig, axs = plt.subplots(1, 2, figsize=(13.5, 4.0))
    tableau(axs[0], {"R": LIG, "S": COT, "I": DIA}, "Le Symbolique tient les côtés, l'Imaginaire les diagonales")
    tableau(axs[1], {"R": LIG, "I": COT, "S": DIA}, "L'Imaginaire tient les côtés, le Symbolique les diagonales")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.2, wspace=0.02)
    fig.text(0.5, 0.955, "Les deux placements qui restent quand le Réel tient les lignes", ha="center", fontsize=12.5, weight="bold")
    fig.text(0.5, 0.085, "Un trait relie deux formules. Il a la couleur du rond qui ne bouge pas quand on passe de l'une à l'autre.", ha="center", fontsize=9.5)
    legende(fig, 0.015); sauve(fig, "fig08_les_deux_placements_restants.png")

def vue_axe(ax, incl=(0.0, 0.0), c=2.5, lw=3.0):
    # Le noeud et son tetraedre, vus selon l'axe de l'Imaginaire (la droite perpendiculaire a son plan).
    # Ecran : x = -X, y = -Z, de sorte que les formules viennent a leur place dans le tableau de Lacan. Repere direct : pas de miroir.
    u, w = np.array([-1.0, 0, 0]), np.array([0, 0, -1.0]); v = np.cross(u, w)
    v = v + incl[0] * u + incl[1] * w; v /= np.linalg.norm(v); u = u - (u @ v) * v; u /= np.linalg.norm(u); w = np.cross(v, u)
    segs = []
    for nom in "RSI":
        p = rond(nom, 600); x, y, z = p @ u, p @ w, p @ v; n = len(x)
        for i in range(n):
            j = (i + 1) % n; segs.append(((z[i] + z[j]) / 2, COUL[nom], (x[i], x[j]), (y[i], y[j]), lw + 0.6))
    for a, b in itertools.combinations("ORSI", 2):
        pa, pb = np.array(SOM[a], float) * c, np.array(SOM[b], float) * c
        for t in np.linspace(0, 1, 120, endpoint=False):
            p, q = pa + t * (pb - pa), pa + (t + 1 / 120) * (pb - pa)
            segs.append((((p + q) / 2) @ v, COUL[couleur_arete(a, b)] if couleur_arete(a, b) in COUL else couleur_arete(a, b), (p @ u, q @ u), (p @ w, q @ w), lw + 2.6))
    for z, coul, xs, ys, l in sorted(segs, key=lambda s: s[0]):
        ax.plot(xs, ys, color="white", lw=l + 3.0, solid_capstyle="butt", zorder=2 + z * 0.01)
        ax.plot(xs, ys, color=coul, lw=l, solid_capstyle="round", zorder=2.001 + z * 0.01)
    for s in "ORSI":
        p = np.array(SOM[s], float) * c; x, y = p @ u, p @ w; g = x < 0
        ax.scatter(x, y, s=170, color="white", edgecolor="#555555", zorder=30)
        ax.text(x + (-0.3 if g else 0.3), y + 0.17, FORM[H2[s]], ha="right" if g else "left", va="center", fontsize=14, zorder=31)
        ax.text(x + (-0.3 if g else 0.3), y - 0.27, NOMF[H2[s]].replace(chr(10), " "), ha="right" if g else "left", va="center", fontsize=9.5, zorder=31)
    ax.set_xlim(-6.6, 6.6); ax.set_ylim(-3.4, 3.4); ax.set_aspect("equal"); ax.axis("off")

def fig23(incl=(0.0, 0.0), fichier="fig23_le_tableau_est_le_noeud_vu_dans_un_axe.png"):
    fig, axs = plt.subplots(1, 2, figsize=(13.5, 5.0))
    tableau(axs[0], {"R": LIG, "S": COT, "I": DIA}, "Le placement proposé, sur le tableau des formules")
    vue_axe(axs[1], incl); axs[1].set_title("Le nœud et son tétraèdre, vus dans l'axe de l'Imaginaire", fontsize=11, pad=6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.13, wspace=0.02)
    legende(fig, 0.02); sauve(fig, fichier)

if __name__ == "__main__":
    print(type(couleur_arete("O", "S")), couleur_arete("O", "S"))
    fig08(); fig23(); fig23((0.16, 0.10), "essai_fig23_incline.png")
