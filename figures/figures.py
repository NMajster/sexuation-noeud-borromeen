# Dessins de l'etude sur les formules de la sexuation et le noeud borromeen.
# Usage : python figures.py   (ecrit les PNG dans ce dossier)
import itertools, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
import fitz

ICI = os.path.dirname(os.path.abspath(__file__))
COUL = {"R": "#1f77b4", "S": "#222222", "I": "#d62728"}          # Reel bleu, Symbolique noir, Imaginaire rouge
NOMR = {"R": "Réel", "S": "Symbolique", "I": "Imaginaire"}
FORM = {"T": r"$\forall x\,\Phi x$", "P": r"$\overline{\forall x}\,\Phi x$", "E": r"$\exists x\,\overline{\Phi x}$", "N": r"$\overline{\exists x}\,\overline{\Phi x}$"}
NOMF = {"T": "tous", "P": "pas-toute", "E": "il en existe un\nqui dit non", "N": "il n'en existe pas\nqui dise non"}
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans", "font.size": 10})

def sauve(fig, nom, dpi=200):
    fig.savefig(os.path.join(ICI, nom), dpi=dpi, bbox_inches="tight", facecolor="white"); plt.close(fig); print("ecrit", nom)

# ---------------------------------------------------------------- figures reprises de l'edition
def reprises():
    base = os.environ.get("LECONS_PDF", "")      # dossier des lecons en PDF de l'edition, non fourni ici
    for f, page, boite, nom in ((r"\S21\S21-L13.pdf", 6, (150, 190, 460, 382), "fig01_lacan_noeud_en_main.png"),
                                (r"\S21\S21-L13.pdf", 14, (190, 138, 405, 300), "fig02_tetraedre_de_l_edition.png"),
                                (r"\S22\S22-L01.pdf", 13, (163, 205, 458, 398), "fig09_rsi_noeud_a_plat.png")):
        d = fitz.open(base + f); d[page - 1].get_pixmap(dpi=220, clip=fitz.Rect(*boite)).save(os.path.join(ICI, nom)); print("ecrit", nom)

# ---------------------------------------------------------------- le noeud borromeen dans l'espace
A, B = 2.0, 1.0
def rond(nom, n=400):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    if nom == "R": return np.c_[A * np.cos(t), B * np.sin(t), 0 * t]       # dans le plan z = 0
    if nom == "S": return np.c_[0 * t, A * np.cos(t), B * np.sin(t)]       # dans le plan x = 0
    return np.c_[B * np.sin(t), 0 * t, A * np.cos(t)]                      # I : dans le plan y = 0
def repere(v):
    v = np.array(v, float) / np.linalg.norm(v)
    k = np.array([0, 0, 1.0]) if abs(v[2]) < 0.9 else np.array([1.0, 0, 0])
    u = np.cross(k, v); u /= np.linalg.norm(u); w = np.cross(v, u)        # (u, w, v) direct : image vue par l'observateur
    return u, w, v
def projette(v):
    u, w, v = repere(v); out = {}
    for nom in "RSI":
        p = rond(nom); out[nom] = (p @ u, p @ w, p @ v)
    return out
def aire(x, y): return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)
def dessine_vue(ax, v, fleches=None, lw=3.2):
    pr = projette(v); segs = []
    for nom in "RSI":
        x, y, z = pr[nom]; n = len(x)
        for i in range(n):
            j = (i + 1) % n; segs.append(((z[i] + z[j]) / 2, nom, (x[i], x[j]), (y[i], y[j])))
    segs.sort(key=lambda s: s[0])
    for z, nom, xs, ys in segs:                                            # le plus loin d'abord, avec un lisere blanc
        ax.plot(xs, ys, color="white", lw=lw + 3.4, solid_capstyle="butt", zorder=2 + z)
        ax.plot(xs, ys, color=COUL[nom], lw=lw, solid_capstyle="round", zorder=2.01 + z)
    if fleches:
        for nom in "RSI":
            x, y, z = pr[nom]; s = fleches[nom]
            for i in (30, 230):
                j = (i + 6 * s) % len(x)
                ax.add_patch(FancyArrowPatch((x[i], y[i]), (x[j], y[j]), arrowstyle="-|>", mutation_scale=15, color=COUL[nom], zorder=20, lw=0))
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
    return pr

def sens_des_couleurs(pr):
    # sens dans lequel on tourne pour aller, par le plus court, du grand axe du Reel a celui du Symbolique puis de l'Imaginaire
    an = {}
    for n in "RSI":
        x, y, _ = pr[n]; i = int(np.argmax(np.hypot(x, y))); an[n] = np.arctan2(y[i], x[i])
    out = [int(np.sign(np.sin(2 * (an[n] - an[m])))) for m, n in (("R", "S"), ("S", "I"), ("I", "R"))]
    assert len(set(out)) == 1, out
    return out[0]
def fleche_de_sens(ax, pr, r0=2.25, coul="#2ca02c", lw=1.6, taille=13):
    s = sens_des_couleurs(pr); th = np.linspace(np.radians(200), np.radians(200 + s * 70), 60)
    ax.plot(r0 * np.cos(th[:-4]), r0 * np.sin(th[:-4]), color=coul, lw=lw, zorder=40)
    ax.add_patch(FancyArrowPatch((r0 * np.cos(th[-8]), r0 * np.sin(th[-8])), (r0 * np.cos(th[-1]), r0 * np.sin(th[-1])), arrowstyle="-|>", mutation_scale=taille, color=coul, lw=0, zorder=41))
    return s

SOMMETS = {+1: [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], -1: [(-1, -1, -1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]}
def nom_quadrant(v): return "(" + ", ".join("+" if c > 0 else "−" for c in v) + ")"

def fig03():
    fig = plt.figure(figsize=(12.5, 5.6))
    ax = fig.add_axes([0.0, 0.05, 0.32, 0.9], projection="3d")
    for nom in "RSI":
        p = rond(nom); ax.plot(p[:, 0], p[:, 1], p[:, 2], color=COUL[nom], lw=2.2)
    c = 2.4
    for a, b in itertools.combinations(list(itertools.product((-1, 1), repeat=3)), 2):
        if sum(x != y for x, y in zip(a, b)) == 1:
            ax.plot(*zip(np.array(a) * c, np.array(b) * c), color="#bbbbbb", lw=0.8)
    for esp, coul, style in ((+1, "#2ca02c", "-"), (-1, "#9467bd", "--")):
        for a, b in itertools.combinations(SOMMETS[esp], 2):
            ax.plot(*zip(np.array(a) * c, np.array(b) * c), color=coul, lw=1.6, ls=style)
        for a in SOMMETS[esp]: ax.scatter(*(np.array(a) * c), color=coul, s=28)
    ax.set_axis_off(); ax.view_init(elev=18, azim=28); ax.set_box_aspect((1, 1, 1))
    ax.set_title("Les huit quadrants et les deux tétraèdres", fontsize=10)
    for li, (esp, coul, titre) in enumerate(((+1, "#2ca02c", "une espèce"), (-1, "#9467bd", "l'autre espèce"))):
        for k, v in enumerate(SOMMETS[esp]):
            a = fig.add_axes([0.34 + k * 0.165, 0.52 - li * 0.47, 0.155, 0.40]); p_ = dessine_vue(a, v, lw=2.6); assert fleche_de_sens(a, p_, coul=coul) == -esp
            a.set_title(("vue du quadrant " if k == 0 else "") + nom_quadrant(v), fontsize=8.5, color=coul)
        fig.text(0.34, 0.955 - li * 0.47, titre, color=coul, fontsize=10, weight="bold")
    for i, nom in enumerate("RSI"): fig.text(0.02 + i * 0.1, 0.02, "— " + NOMR[nom], color=COUL[nom], fontsize=9.5)
    fig.text(0.34, 0.02, "La flèche va du rond bleu au noir, puis au rouge.", fontsize=9.5, style="italic")
    sauve(fig, "fig03_quadrants_et_tetraedres.png")

def fig04():
    v0 = SOMMETS[+1][0]; pr = projette(v0)
    sens0 = {nom: (1 if aire(pr[nom][0], pr[nom][1]) > 0 else -1) for nom in "RSI"}     # on oriente chaque rond pour qu'il tourne dans le meme sens vu de v0
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.9))
    for ax, v in zip(axs, SOMMETS[+1]):
        pr = dessine_vue(ax, v, fleches=sens0, lw=2.8)
        garde = [nom for nom in "RSI" if (1 if aire(pr[nom][0], pr[nom][1]) * sens0[nom] > 0 else -1) == 1]
        if v == v0: txt = "les trois ronds tournent\ndans le même sens"
        else:
            assert len(garde) == 1, garde
            txt = ("l'" if garde[0] == "I" else "le ") + NOMR[garde[0]] + " seul garde son sens,\nles deux autres l'ont inversé"
        ax.set_title("quadrant " + nom_quadrant(v), fontsize=9); ax.text(0, -2.95, txt, ha="center", va="top", fontsize=9)
    for i, nom in enumerate("RSI"): fig.text(0.33 + i * 0.13, 0.97, "— " + NOMR[nom], color=COUL[nom], fontsize=10)
    sauve(fig, "fig04_les_quatre_vues_et_leurs_fleches.png")

# ---------------------------------------------------------------- le tetraedre et ses aretes
P = {"O": np.array([0.0, 0.15]), "R": np.array([-1.5, -0.85]), "S": np.array([1.5, -0.85]), "I": np.array([0.0, 1.75])}
ETIQ = {"O": "les trois ronds\nen place", "R": "le Réel seul\nreste en place", "S": "le Symbolique seul\nreste en place", "I": "l'Imaginaire seul\nreste en place"}
def couleur_arete(a, b):
    if "O" in (a, b): return COUL[a if b == "O" else b]
    return COUL[({"R", "S", "I"} - {a, b}).pop()]
def tetra(ax, placement=None, etiquettes=True, lw=4.5, taille=13, noms=False, petit=False, lettres=None):
    for a, b in itertools.combinations("ORSI", 2):
        ax.plot(*zip(P[a], P[b]), color=couleur_arete(a, b), lw=lw, solid_capstyle="round", zorder=1)
    for s in "ORSI":
        ax.scatter(*P[s], s=70 if petit else 150, color="white", edgecolor="#555555", zorder=3)
        dx, dy, ha, va = {"O": (0.0, -0.20, "center", "top"), "R": (-0.12, -0.14, "right", "top"), "S": (0.12, -0.14, "left", "top"), "I": (0.0, 0.16, "center", "bottom")}[s]
        lignes = []
        if placement: lignes.append(r"$\mathit{" + lettres[placement[s]] + "}$" if lettres else FORM[placement[s]])
        if placement and noms: lignes.append(NOMF[placement[s]])
        if etiquettes: lignes.append(ETIQ[s])
        if s == "O" and (placement or etiquettes):
            ax.text(P[s][0], P[s][1] - 0.22, "\n".join(lignes), ha="center", va="top", fontsize=(taille if placement else 8.5) * (0.92 if not petit else 1), zorder=4)
        elif lignes:
            ax.text(P[s][0] + dx, P[s][1] + dy, "\n".join(lignes), ha=ha, va=va, fontsize=taille if placement else 8.5, zorder=4)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.0, 2.9)
def legende_ronds(fig, y=0.02, x0=0.2, pas=0.22, suffixe=" ne bouge pas"):
    for i, nom in enumerate("RSI"): fig.text(x0 + i * pas, y, "━ le " + NOMR[nom] + suffixe if nom != "I" else "━ l'" + NOMR[nom] + suffixe, color=COUL[nom], fontsize=9.5)

def fig05():
    fig, ax = plt.subplots(figsize=(7.2, 5.6)); tetra(ax, etiquettes=True)
    ax.set_title("Chaque arête a la couleur du rond qui ne bouge pas quand on la parcourt.\nLes deux arêtes d'une même couleur n'ont pas de sommet commun.", fontsize=10)
    legende_ronds(fig, x0=0.08, pas=0.3); sauve(fig, "fig05_tetraedre_aux_aretes_colorees.png")

F2 = {"T": (0, 0), "P": (0, 1), "E": (1, 0), "N": (1, 1)}
def commun(a, b):
    (f1, q1), (f2, q2) = F2[a], F2[b]
    return "lignes" if f1 == f2 else ("côtés" if q1 == q2 else "diagonales")
def attribution(pl): return tuple(commun(pl["O"], pl[x]) for x in "RSI")
def tous_les_placements(): return [dict(zip("ORSI", p)) for p in itertools.permutations("TPEN")]
H2 = {"O": "T", "R": "P", "S": "E", "I": "N"}; H1 = {"O": "T", "R": "P", "S": "N", "I": "E"}
assert attribution(H2) == ("lignes", "côtés", "diagonales") and attribution(H1) == ("lignes", "diagonales", "côtés")

def fig06():
    groupes = {}
    for pl in tous_les_placements(): groupes.setdefault(attribution(pl), []).append(pl)
    assert len(groupes) == 6 and all(len(g) == 4 for g in groupes.values())
    ordre = sorted(groupes, key=lambda a: (a != attribution(H2), a != attribution(H1), a))
    fig, axs = plt.subplots(6, 4, figsize=(11.5, 13.5))
    for i, att in enumerate(ordre):
        for j, pl in enumerate(groupes[att]):
            ax = axs[i][j]; tetra(ax, placement=pl, etiquettes=False, lw=2.6, taille=8.5, petit=True)
        axs[i][0].text(-3.3, 2.75, "Réel : " + att[0] + "   Symbolique : " + att[1] + "   Imaginaire : " + att[2], fontsize=9.5, weight="bold", ha="left", va="bottom")
    fig.suptitle("Vingt-quatre dispositions, six placements. Sur chaque ligne, quatre dessins du même placement,\nqui ne diffèrent que par le sommet où l'on a mis les trois ronds en place (au centre).", fontsize=11, y=0.995)
    legende_ronds(fig, y=0.005, x0=0.12, pas=0.28); fig.subplots_adjust(hspace=0.35, wspace=0.02, top=0.94, bottom=0.03)
    sauve(fig, "fig06_vingt_quatre_dispositions_six_placements.png", dpi=170)

LQ = 1.7
Q = {"E": (0, 1), "N": (LQ, 1), "T": (0, 0), "P": (LQ, 0)}
def carre(ax, paires, coul, titre, sous=None, noms72=None):
    for a, b in itertools.combinations("ENTP", 2):
        ax.plot(*zip(Q[a], Q[b]), color="#dddddd", lw=1.2, zorder=1)
    for a, b in paires: ax.plot(*zip(Q[a], Q[b]), color=coul, lw=6, solid_capstyle="round", zorder=2)
    for s in "ENTP":
        x, y = Q[s]
        ax.text(x + (-0.09 if x == 0 else 0.09), y, FORM[s], ha="right" if x == 0 else "left", va="center", fontsize=12.5, zorder=3)
        ax.scatter(x, y, s=60, color="white", edgecolor="#555555", zorder=3)
    if noms72:
        for (a, b), mot in noms72.items():
            xm, ym = (np.array(Q[a]) + np.array(Q[b])) / 2
            ax.text(xm, ym, mot, ha="center", va="center", fontsize=8.5, style="italic", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=5)
    ax.set_title(titre, fontsize=10.5)
    if sous: ax.text(LQ / 2, -0.33, sous, ha="center", va="top", fontsize=9)
    ax.set_xlim(-1.0, LQ + 1.0); ax.set_ylim(-0.75, 1.3); ax.set_aspect("equal"); ax.axis("off")
LIG, COT, DIA = [("E", "N"), ("T", "P")], [("E", "T"), ("N", "P")], [("E", "P"), ("T", "N")]

def fig07():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.3))
    carre(axs[0], LIG, "#7f7f7f", "Par lignes", "en haut ce qui dit non,\nen bas ce qui dit oui", {("E", "N"): "l'existence", ("T", "P"): "le manque, l'objet a"})
    carre(axs[1], COT, "#7f7f7f", "Par côtés", "à gauche le côté homme,\nà droite le côté femme", {("E", "T"): "la contradiction", ("N", "P"): "l'indécidable"})
    carre(axs[2], DIA, "#7f7f7f", "Par diagonales", "les couples que la logique ordinaire\ntient pour équivalents")
    fig.text(0.5, 0.0, "En italique : les noms que Lacan donne aux quatre côtés de son carré le 1er juin 1972. Il n'en donne pas aux diagonales.", ha="center", fontsize=9)
    sauve(fig, "fig07_trois_rangements_des_formules.png")

def fig08():
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.4))
    tetra(axs[0], placement=H2, etiquettes=False, noms=True, taille=11.5); axs[0].set_title("Le Symbolique tient les côtés, l'Imaginaire les diagonales", fontsize=10.5)
    tetra(axs[1], placement=H1, etiquettes=False, noms=True, taille=11.5); axs[1].set_title("L'Imaginaire tient les côtés, le Symbolique les diagonales", fontsize=10.5)
    fig.text(0.5, 0.955, "Les deux placements qui restent quand le Réel tient les lignes", ha="center", fontsize=12, weight="bold")
    fig.text(0.5, 0.06, "Au centre, le sommet où les trois ronds sont en place. Les deux dessins ont le même « tous » et le même « pas-toute ».\nIls échangent seulement les deux formules du haut du tableau.", ha="center", fontsize=9.5)
    legende_ronds(fig, y=0.005, x0=0.16, pas=0.25); sauve(fig, "fig08_les_deux_placements_restants.png")

def fig10():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.5))
    carre(axs[0], LIG, "#1f77b4", "Dans aucune logique", "une formule et la même au quanteur barré\nne tiennent jamais ensemble")
    carre(axs[1], DIA, "#d62728", "Chez Aristote et Boole", "les diagonales tiennent ensemble,\net elles seules")
    carre(axs[2], COT, "#222222", "Chez Lacan", "les deux formules d'un même côté tiennent ensemble :\ncelle du haut fonde celle du bas")
    for a, b in COT:
        axs[2].add_patch(FancyArrowPatch(np.array(Q[a]) + (0.16 if a == "E" else -0.16, -0.18), np.array(Q[b]) + (0.16 if a == "E" else -0.16, 0.18), arrowstyle="-|>", mutation_scale=16, color="#222222", lw=1.2, zorder=6))
    fig.suptitle("Quelles formules vont ensemble ? Trois réponses", fontsize=12, weight="bold", y=1.0)
    sauve(fig, "fig10_trois_logiques.png")

def fig11():
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.6))
    ax = axs[0]; ax.set_title("Deux individus : le pas-tout sans exception désignée", fontsize=10.5)
    pos = {"départ": (0, 0), "g": (-1.6, 1.5), "d": (1.6, 1.5)}
    for k in ("g", "d"): ax.add_patch(FancyArrowPatch(pos["départ"], pos[k], arrowstyle="-|>", mutation_scale=16, color="#666666", lw=1.3, shrinkA=38, shrinkB=42))
    ax.text(0, 0, "on ne sait encore\nrien de a ni de b", ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#f2f2f2", ec="#888888"))
    ax.text(-1.6, 1.5, "a dit oui\nb dit non", ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#f2f2f2", ec="#888888"))
    ax.text(1.6, 1.5, "a dit non\nb dit oui", ha="center", va="center", fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#f2f2f2", ec="#888888"))
    ax.text(0, -0.75, "Quoi qu'il arrive, les deux ne diront pas oui : pas-tout.\nMais on ne peut pas dire lequel dit non : pas d'exception désignée.", ha="center", va="top", fontsize=9)
    ax.set_xlim(-3, 3); ax.set_ylim(-1.7, 2.2); ax.axis("off")
    ax = axs[1]; ax.set_title("Une suite sans fin : le pas-tout avec « il n'en existe pas qui dise non »", fontsize=10.5)
    for k in range(5):
        for n in range(8):
            ax.add_patch(Rectangle((n * 0.62, -k * 0.5), 0.5, 0.36, fc="#222222" if n < k + 1 else "white", ec="#888888", lw=0.8))
        ax.text(-0.2, -k * 0.5 + 0.18, f"étape {k + 1}", ha="right", va="center", fontsize=8.5)
    ax.text(8 * 0.62 + 0.1, -1.0, "…", fontsize=16, va="center"); ax.text(2.2, -2.45, "⋮", fontsize=16, ha="center")
    ax.text(2.4, -2.75, "En noir, les individus pour qui le oui est déjà établi. À aucune étape on ne peut dire « tous ».\nÀ aucune étape on ne trouve celui qui dit non : chacun finira par être en noir.", ha="center", va="top", fontsize=9)
    ax.set_xlim(-1.3, 6); ax.set_ylim(-3.7, 0.7); ax.axis("off")
    sauve(fig, "fig11_deux_modeles.png")

def fig12():
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.add_patch(FancyBboxPatch((-0.72, -0.22), 0.86, 1.44, boxstyle="round,pad=0.05", fc="#eeeeee", ec="#222222", lw=1.5, zorder=0))
    ax.text(-0.29, 1.36, "le Symbolique,\n« de l'ordre du Un »", ha="center", va="bottom", fontsize=9.5)
    for s in "ENTP":
        x, y = Q[s]; ax.text(-0.29 if x == 0 else 1.6, y, FORM[s], ha="center", va="center", fontsize=14)
    ax.text(-0.29, 0.78, "« le Un unique,\nqui seul fonde le tout »", ha="center", va="center", fontsize=8.5, style="italic")
    ax.text(-0.29, 0.22, "« le Un dont on fait le tout »", ha="center", va="center", fontsize=8.5, style="italic")
    ax.add_patch(FancyArrowPatch((0.2, 1.0), (1.3, 1.0), arrowstyle="-|>", mutation_scale=16, color="#555555", lw=1.2))
    ax.text(0.75, 1.07, "« Nier l'Un unique »", ha="center", va="bottom", fontsize=8.5, style="italic"); ax.text(0.75, 0.93, "15 janvier 1974", ha="center", va="top", fontsize=7.5)
    ax.add_patch(FancyArrowPatch((0.2, 0.0), (1.3, 0.0), arrowstyle="-|>", mutation_scale=16, color="#555555", lw=1.2))
    ax.text(0.75, 0.07, "« ce qui s'oppose à l'Un\ndu tout de L'homme »", ha="center", va="bottom", fontsize=8.5, style="italic"); ax.text(0.75, -0.07, "19 février 1974", ha="center", va="top", fontsize=7.5)
    ax.text(0.65, -0.5, "Barrer un quanteur, c'est nier un Un, et c'est passer de l'autre côté.", ha="center", fontsize=9.5)
    ax.set_xlim(-1.0, 2.2); ax.set_ylim(-0.65, 1.75); ax.axis("off")
    sauve(fig, "fig12_les_figures_du_un.png")

def fig14():
    fig, ax = plt.subplots(figsize=(13, 7.6))
    dates = {"déc. 1971": 1971.95, "été 1972": 1972.55, "avril 1973": 1973.3, "janv. 1974": 1974.05, "mai 1974": 1974.4, "nov. 1974": 1974.85, "janv. 1975": 1975.07, "mai 1975": 1975.4, "déc. 1975": 1975.95, "1977": 1977.4, "1979": 1979.03}
    fils = [("L'exception", "#1f77b4", [("déc. 1971", "la forclusion,\nau point de la fonction"), ("été 1972", "un point\nsans valeur de vérité"), ("mai 1974", "« le pas de ce\nqui ex-siste »"), ("janv. 1975", "le père exception,\nfonction du symptôme"), ("déc. 1975", "un quatrième rond")]),
            ("Le pas-tout", "#d62728", [("déc. 1971", "la discordance"), ("été 1972", "ce qui suit de l'absence\nd'exception"), ("avril 1973", "l'infini"), ("mai 1974", "deux jouissances,\ncelle du corps"), ("nov. 1974", "le réel « de ne pas\nfaire tout »"), ("1977", "« il n'y a pas\nde tous »")]),
            ("Les trois ronds", "#222222", [("janv. 1974", "strictement équivalents"), ("mai 1974", "une première différence,\npar l'orientation"), ("janv. 1975", "consistance, trou,\nek-sistence"), ("mai 1975", "« peu importe »\nlequel est le Réel"), ("déc. 1975", "il en faut quatre"), ("1979", "« abus de\nmétaphore »")])]
    for k, (nom, coul, pts) in enumerate(fils):
        y = 3.6 - 1.8 * k; ax.plot([1971.7, 1979.4], [y, y], color=coul, lw=1.5, alpha=0.5); ax.text(1971.6, y, nom, ha="right", va="center", color=coul, fontsize=10.5, weight="bold")
        for i, (d, txt) in enumerate(pts):
            x = dates[d]; ax.scatter(x, y, color=coul, s=40, zorder=3)
            dy = (0.14, -0.14, 0.56, -0.56)[i % 4]; ax.text(x, y + dy, txt, ha="center", va="bottom" if dy > 0 else "top", fontsize=7.6, color=coul)
    for an in range(1972, 1980): ax.text(an, -1.35, str(an), ha="center", fontsize=9, color="#666666"); ax.plot([an, an], [-1.0, 4.4], color="#eeeeee", lw=0.8, zorder=0)
    ax.axvspan(1974.33, 1974.47, color="#ffe9a8", zorder=0); ax.text(1974.4, 4.75, "14 et 21 mai 1974 :\nle programme", ha="center", fontsize=8.5)
    ax.set_xlim(1970.3, 1979.7); ax.set_ylim(-1.55, 5.2); ax.axis("off")
    sauve(fig, "fig14_frise_1971_1979.png")

def fig15():
    fig = plt.figure(figsize=(9.5, 9.2))
    ax = fig.add_axes([0.02, 0.33, 0.96, 0.62]); tetra(ax, placement=H2, etiquettes=True, noms=False, taille=12, lw=5.5)
    ax.set_title("Le placement proposé", fontsize=13, weight="bold")
    ax2 = fig.add_axes([0.30, 0.045, 0.40, 0.19]); tetra(ax2, placement=H1, etiquettes=False, taille=8.5, lw=2.4, petit=True)
    ax2.set_title("L'autre placement, non écarté", fontsize=9)
    fig.text(0.5, 0.305, "Le Réel ne bouge pas le long des lignes, le Symbolique le long des côtés, l'Imaginaire le long des diagonales.", ha="center", fontsize=9.5)
    legende_ronds(fig, y=0.012, x0=0.1, pas=0.29); sauve(fig, "fig15_le_placement_propose.png")



# ---------------------------------------------------------------- le tetraedre pose sur le noeud
SOM = {"O": (1, 1, 1), "S": (1, -1, -1), "I": (-1, 1, -1), "R": (-1, -1, 1)}      # quadrant ou ce rond seul garde son sens (verifie par fig04)
def fig16(formules=True, fichier="fig17_tetraedre_autour_du_noeud_avec_formules.png"):
    c = 2.5; fig = plt.figure(figsize=(8.6, 8.2)); ax = fig.add_subplot(111, projection="3d")
    for nom in "RSI":
        p = rond(nom); ax.plot(p[:, 0], p[:, 1], p[:, 2], color=COUL[nom], lw=3.2)
    for a, b in itertools.combinations(list(itertools.product((-1, 1), repeat=3)), 2):
        if sum(x != y for x, y in zip(a, b)) == 1: ax.plot(*zip(np.array(a) * c, np.array(b) * c), color="#cccccc", lw=0.7)
    for a, b in itertools.combinations("ORSI", 2):
        ax.plot(*zip(np.array(SOM[a]) * c, np.array(SOM[b]) * c), color=couleur_arete(a, b), lw=3.0, alpha=0.95)
    for s in "ORSI":
        v = np.array(SOM[s]) * c; ax.scatter(*v, color="white", edgecolor="#444444", s=90, depthshade=False)
        w = v * 1.16
        if formules: ax.text(w[0], w[1], w[2], FORM[H2[s]], fontsize=14, ha="center", va="center")
    ax.set_axis_off(); ax.view_init(elev=16, azim=24); ax.set_box_aspect((1, 1, 1))
    lim = c * 1.05; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    fig.text(0.5, 0.955, "Le tétraèdre autour du nœud, dans l'espace", ha="center", fontsize=12.5, weight="bold")
    fig.text(0.5, 0.075, "Chaque arête a la couleur d'un rond : elle est parallèle au plan de ce rond.\nLes deux arêtes d'une même couleur passent de part et d'autre de lui.", ha="center", fontsize=9.5)
    for i, nom in enumerate("RSI"): fig.text(0.2 + i * 0.25, 0.03, "━ " + NOMR[nom], color=COUL[nom], fontsize=10)
    sauve(fig, fichier)

def fig17():
    fig, ax = plt.subplots(figsize=(8.4, 8.4)); v = SOM["O"]; u, w, n = repere(v)
    dessine_vue(ax, v, lw=3.4); c = 1.75
    pts = {s: (c * np.dot(SOM[s], u), c * np.dot(SOM[s], w)) for s in "ORSI"}
    for a, b in itertools.combinations("ORSI", 2):
        ax.plot(*zip(pts[a], pts[b]), color=couleur_arete(a, b), lw=2.2, ls=(0, (5, 3)), zorder=40, alpha=0.9)
    for s in "ORSI":
        x, y = pts[s]; ax.scatter(x, y, s=120, color="white", edgecolor="#444444", zorder=50)
        r = np.hypot(x, y)
        if s == "O": ax.text(x + 0.16, y + 0.2, FORM[H2[s]], fontsize=14, ha="left", va="bottom", zorder=60, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
        else: ax.text(x * (1 + 0.42 / r), y * (1 + 0.42 / r), FORM[H2[s]], fontsize=14, ha="center", va="center", zorder=60)
    ax.set_xlim(-3.9, 3.9); ax.set_ylim(-3.9, 3.9)
    ax.set_title("Le tétraèdre sur le nœud mis à plat", fontsize=12.5, weight="bold")
    fig.text(0.5, 0.06, "Le nœud est vu du sommet qui porte « tous » : ce sommet est au centre, au-dessus du triangle central.\nLes trois autres sommets tombent chacun dans l'axe d'une boucle. En pointillé, les arêtes, à la couleur du rond qui ne bouge pas.", ha="center", fontsize=9.5)
    for i, nom in enumerate("RSI"): fig.text(0.2 + i * 0.25, 0.02, "━ " + NOMR[nom], color=COUL[nom], fontsize=10)
    sauve(fig, "fig18_tetraedre_sur_le_noeud_a_plat.png")

def fig19():
    groupes = {}
    for pl in tous_les_placements(): groupes.setdefault(attribution(pl), []).append(pl)
    att = ("côtés", "lignes", "diagonales")                         # un exemple pris parmi les six, qui n'est aucun des deux retenus plus loin
    fig, axs = plt.subplots(1, 4, figsize=(12.5, 3.5))
    ex = groupes[att][0]; lettres = {ex["O"]: "a", ex["S"]: "b", ex["I"]: "c", ex["R"]: "d"}        # des lettres et non des formules : rien n'est encore place
    for ax, pl in zip(axs, groupes[att]): tetra(ax, placement=pl, etiquettes=False, lw=3.0, taille=15, petit=True, lettres=lettres)
    legende_ronds(fig, y=0.0, x0=0.14, pas=0.27); fig.subplots_adjust(wspace=0.02, bottom=0.12)
    sauve(fig, "fig19_un_placement_dessine_de_quatre_facons.png")

if __name__ == "__main__":
    reprises(); fig03(); fig04(); fig05(); fig06(); fig07(); fig08(); fig10(); fig11(); fig12(); fig14(); fig15()
    fig16(formules=False, fichier="fig16_tetraedre_autour_du_noeud.png"); fig16(); fig17(); fig19()
