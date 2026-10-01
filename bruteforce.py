"""Partie 1 : essayer tous les groupes possibles d'actions.

Exemple : python3 bruteforce.py
Avec n actions, le temps augmente comme O(n × 2**n).
"""

import argparse
from decimal import Decimal
from itertools import combinations
from pathlib import Path
from time import perf_counter

from actions import BUDGET_EUROS, DEFAULT_FILE, load_actions, print_result


def find_best_investment(actions, budget_euros=BUDGET_EUROS):
    """Renvoie le groupe au bénéfice maximal qui respecte le budget."""
    best_actions = []
    best_profit = Decimal("0")

    # combinations donne chaque groupe une seule fois, sans répéter d'action.
    for group_size in range(1, len(actions) + 1):
        for group in combinations(actions, group_size):
            group_cost = sum((action[1] for action in group), Decimal("0"))
            if group_cost > budget_euros:
                continue

            group_profit = sum((action[3] for action in group), Decimal("0"))
            if group_profit > best_profit:
                best_profit = group_profit
                best_actions = list(group)

    return best_actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", nargs="?", type=Path, default=DEFAULT_FILE)
    arguments = parser.parse_args()

    start_time = perf_counter()
    try:
        actions, report = load_actions(arguments.csv_file)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    # Avec 1 000 actions, la force brute aurait un nombre gigantesque de groupes.
    if len(actions) > 25:
        parser.error("La force brute est réservée au petit fichier initial.")

    best_actions = find_best_investment(actions)
    elapsed_seconds = perf_counter() - start_time
    print_result(best_actions, report)
    print(f"Temps de lecture et de recherche : {elapsed_seconds:.4f} s")


if __name__ == "__main__":
    main()
