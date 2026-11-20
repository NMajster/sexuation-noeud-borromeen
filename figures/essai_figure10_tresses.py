# Essai : les deux placements restants, lus sur le noeud deroule.
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figures as f
import essai_section3 as e

ordre = [(1, 1, 1), (-1, -1, 1), (1, -1, -1), (-1, 1, -1)]          # les trois montent ; le Reel seul ; le Symbolique seul ; l'Imaginaire seul
A = ["T", "P", "E", "N"]; B = ["T", "P", "N", "E"]
fig, axs = plt.subplots(1, 4, figsize=(12.5, 7.4))
for k, (ax, v) in enumerate(zip(axs, ordre)):
    s = e.tresse(ax, v, {"R": 1, "S": 1, "I": 1})
    if len(set(s.values())) == 1: txt = "les trois ronds montent"
    else:
        seul = [n for n in "RSI" if s[n] > 0][0]; txt = ("l'" if seul == "I" else "le ") + f.NOMR[seul] + " monte seul"
    ax.text(0.5, -0.03, txt, transform=ax.transAxes, ha="center", va="top", fontsize=10)
    for li, (pl, y) in enumerate(((A, -0.17), (B, -0.33))):
        change = k >= 2
        ax.text(0.5, y, f.FORM[pl[k]] + "\n" + f.NOMF[pl[k]].replace("\n", " "), transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
                bbox=dict(boxstyle="round,pad=0.35", fc="#fff6d6" if change else "#f2f2f2", ec="#d4a100" if change else "#bbbbbb", lw=1.2))
fig.text(0.015, 0.262, "premier\nplacement", fontsize=9.5, ha="left", va="center", weight="bold")
fig.text(0.015, 0.135, "second\nplacement", fontsize=9.5, ha="left", va="center", weight="bold")
for i, nom in enumerate("RSI"): fig.text(0.27 + i * 0.19, 0.012, "━ " + f.NOMR[nom], color=f.COUL[nom], fontsize=10)
fig.subplots_adjust(left=0.1, right=0.99, top=0.97, bottom=0.36, wspace=0.05)
fig.savefig("essai_figure10_tresses.png", dpi=170, bbox_inches="tight", facecolor="white"); print("ecrit essai_figure10_tresses.png")
