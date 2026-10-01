# Projet 7 — Optimiser un portefeuille d'actions

Objectif : maximiser le bénéfice après deux ans avec un budget maximal de 500 €.
Chaque action ne peut être achetée qu'une fois.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 bruteforce.py
python3 optimized.py
python3 optimized.py data/dataset1.csv
python3 optimized.py data/dataset2.csv
```

`bruteforce.py` essaie tous les groupes du petit fichier initial.
`optimized.py` utilise la programmation dynamique pour les trois fichiers.
`actions.py` contient seulement le code commun de lecture et d'affichage :
il ne se lance pas directement.

Les deux scripts indiquent les actions à acheter, le coût, le bénéfice après
deux ans et le temps de lecture et de recherche. Les lignes invalides et les
noms ambigus sont écartés ; les CSV d'origine restent inchangés.

Le rapport d'exploration et la présentation se trouvent dans le dossier
`Projet_7_livrables` à côté de ce dépôt.
