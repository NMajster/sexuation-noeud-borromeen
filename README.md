# Les formules de la sexuation sur le nœud borroméen : programmes et résultats

Ce dépôt accompagne une étude de topologie lacanienne, « Une réponse à Charles Melman, un coup de main à Jacques Lacan. Enquête sur la place des formules de la sexuation dans le nœud borroméen ».

Le 14 mai 1974 (*Les non-dupes errent*), Lacan dit que les quatre formules de la sexuation se placent aux quatre sommets d'un tétraèdre que dessine le nœud borroméen, et il ne dit pas laquelle va où. L'étude reprend ce programme.

Le dépôt contient les programmes qui ont servi aux calculs, leurs résultats, les figures calculées et les programmes qui les tracent, ainsi que deux programmes de vérification écrits à part. Il ne contient ni le texte de l'étude, ni les textes cités, ni les figures reprises de l'édition.

## Le modèle

Le nœud borroméen est fait de trois ellipses centrées à l'origine, de demi-axes 2 et 1, chacune dans un plan de coordonnées : le Réel dans le plan z = 0, le Symbolique dans le plan x = 0, l'Imaginaire dans le plan y = 0. Les trois plans partagent l'espace en huit compartiments, que Lacan appelle des quadrants. Les quatre formules sont notées T (tous), P (pas-toute), E (il en existe un qui dit non), N (il n'en existe pas qui dise non).

## Ce que les calculs établissent

| Résultat | Où |
|---|---|
| Vu depuis les huit quadrants, le nœud donne deux espèces de dessins, quatre de chaque. Deux quadrants opposés donnent deux dessins images l'un de l'autre dans un miroir | `figures/figures.py`, `verification/verifier_geometrie.py` |
| Les quatre quadrants d'une même espèce sont les sommets d'un tétraèdre. Entre deux sommets, un rond et un seul reste du même côté de son plan. Chaque rond tient ainsi deux arêtes opposées | `figures/figures.py`, `verification/verifier_geometrie.py` |
| Les vingt-quatre façons de poser quatre formules sur quatre sommets se réduisent à six placements, chacun dit par le rond attaché aux lignes, aux côtés et aux diagonales du tableau des formules | `figures/figures.py`, `verification/verifier_geometrie.py` |
| Le nœud borroméen a quarante-huit symétries. Quand chaque rond garde sa couleur, le nombre de ronds dont le sens est inversé est zéro ou deux. C'est l'énoncé que Pierre Soury donnait en 1975 pour non démontré (*Chaînes et nœuds*, texte 3). Il est démontré en général par Berglund et al., « Intrinsic Symmetry Groups of Links with 8 and Fewer Crossings », *Symmetry* 4 (1), 2012, énoncé 8.2 | `calcul/borromeen_colorie_oriente.py` |
| Autour de chacun des quatre axes du tétraèdre, chaque rond fait un tour et un seul, et le nœud se déroule en une tresse à trois brins et six croisements, la même pour les quatre axes. Les ronds étant fléchés, un seul axe les voit tourner tous trois dans le même sens | `calcul/exploration_tores.py`, `figures/essai_section3.py`, `verification/verifier_geometrie.py` |
| Regardé dans l'axe d'un rond, le tétraèdre se projette sur un carré et ses deux diagonales. Avec le placement de l'étude, vu dans l'axe de l'Imaginaire, chaque formule vient à la place qu'elle a dans le tableau de Lacan, sans miroir | `figures/figures_tableau.py`, `verification/verifier_geometrie.py` |
| Les relations entre les quatre formules en logique classique et en logique intuitionniste, avec les modèles qui les séparent | `verification/verifier_logique.py` |
| Dans l'algèbre à trois valeurs que suggère l'écriture x = x³ (14 mai 1974), vingt-sept façons d'écrire les quatre formules, dont sept font tenir les deux côtés du tableau | `calcul/trois_valeurs_boole.py` |
| Sur le nœud à quatre ronds, dont les ronds vont par couples, les vingt-quatre façons de poser les formules se rangent en trois classes | `calcul/formules_sur_quatre_ronds.py` |

## Contenu

- `calcul/` : les programmes de calcul et, pour chacun, le fichier `resultats_….txt` qu'il produit.
- `figures/` : les programmes qui tracent les figures de l'étude, et les figures calculées. `figures.py` contient le modèle du nœud et la plupart des figures. Les autres programmes s'en servent.
- `verification/` : deux programmes écrits indépendamment pour contrôler la géométrie et la logique, avec leurs sorties. Ils n'utilisent que la bibliothèque standard de Python.

## Pour relancer

Python 3 avec `numpy` et `matplotlib` pour les figures. `calcul/borromeen_colorie_oriente.py` demande de plus `snappy` et `spherogram`. Les figures reprises de l'édition ne sont pas fournies : la fonction `reprises()` de `figures.py` n'est utile qu'à qui possède les volumes en PDF.

```sh
python -X utf8 verification/verifier_geometrie.py
python -X utf8 verification/verifier_logique.py
python -X utf8 calcul/trois_valeurs_boole.py
python -X utf8 calcul/formules_sur_quatre_ronds.py
```

## Étude précédente

Les nœuds à quatre de 1975 : https://github.com/NMajster/noeuds-a-quatre-1975
