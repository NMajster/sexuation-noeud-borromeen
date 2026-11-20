# Le placement propose, lu sur le noeud deroule : chaque formule est une facon de tourner.
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figures as f
import essai_section3 as e

ordre = [(1, 1, 1), (-1, -1, 1), (1, -1, -1), (-1, 1, -1)]          # les trois montent ; le Reel seul ; le Symbolique seul ; l'Imaginaire seul
A = ["T", "P", "E", "N"]
fig, axs = plt.subplots(1, 4, figsize=(12.5, 6.9))
for k, (ax, v) in enumerate(zip(axs, ordre)):
    s = e.tresse(ax, v, {"R": 1, "S": 1, "I": 1})
    if len(set(s.values())) == 1: txt = "les trois ronds montent"
    else:
        seul = [n for n in "RSI" if s[n] > 0][0]; txt = ("l'" if seul == "I" else "le ") + f.NOMR[seul] + " monte seul"
    ax.set_title(f.FORM[A[k]], fontsize=17, pad=14)
    ax.text(0.5, 1.005, f.NOMF[A[k]].replace("\n", " "), transform=ax.transAxes, ha="center", va="bottom", fontsize=10)
    ax.text(0.5, -0.03, txt, transform=ax.transAxes, ha="center", va="top", fontsize=10.5, weight="bold")
for i, nom in enumerate("RSI"): fig.text(0.27 + i * 0.19, 0.012, "━ " + f.NOMR[nom], color=f.COUL[nom], fontsize=10)
fig.suptitle("Le placement proposé, sur le nœud déroulé", fontsize=12.5, weight="bold", y=1.03)
fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.11, wspace=0.05)
fig.savefig("fig21_le_placement_propose_sur_le_noeud_deroule.png", dpi=180, bbox_inches="tight", facecolor="white"); print("ecrit fig21")
