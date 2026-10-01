"""Partie 2 : sac à dos 0/1 par programmation dynamique.

Exemple : python3 optimized.py data/dataset1.csv
Temps O(n × B), où B est le budget exprimé en centimes.
"""

import argparse
from decimal import Decimal
from pathlib import Path
from time import perf_counter

import numpy as np

from actions import BUDGET_EUROS, DEFAULT_FILE, load_actions, print_result


def find_best_investment(actions, budget_euros=BUDGET_EUROS):
    """Compare, pour chaque action et budget, acheter ou ne pas acheter.

    Les coûts sont des centimes entiers. Les bénéfices deviennent aussi des
    entiers, avec assez de décimales pour éviter un arrondi prématuré.
    """
    budget_cents = int(budget_euros * 100)
    if budget_cents < 0 or Decimal(budget_cents) != budget_euros * 100:
        raise ValueError("Le budget doit être un montant positif en centimes.")

    decimal_places = max(
        (max(0, -action[3].as_tuple().exponent) for action in actions),
        default=0,
    )
    profit_scale = 10 ** decimal_places
    action_profits = [int(action[3] * profit_scale) for action in actions]
    if sum(action_profits) > np.iinfo(np.int64).max:
        raise ValueError("Bénéfices trop grands pour le tableau de calcul.")

    best_profit_by_budget = np.zeros(budget_cents + 1, dtype=np.int64)
    decisions_by_action = []

    for action, profit_units in zip(actions, action_profits):
        action_price_cents = int(action[1] * 100)
        bought_at_budget = np.zeros(budget_cents + 1, dtype=bool)

        if action_price_cents <= budget_cents:
            # Les tranches associent chaque budget à son budget restant.
            # L'addition produit un nouveau tableau AVANT la mise à jour :
            # on ne peut donc pas acheter deux fois l'action en cours.
            profit_with_purchase = (
                best_profit_by_budget[:-action_price_cents] + profit_units
            )
            profit_without_purchase = best_profit_by_budget[action_price_cents:]
            bought_at_budget[action_price_cents:] = (
                profit_with_purchase > profit_without_purchase
            )
            np.maximum(
                profit_without_purchase,
                profit_with_purchase,
                out=profit_without_purchase,
            )

        decisions_by_action.append(bought_at_budget)

    # On remonte les décisions pour retrouver les noms des actions achetées.
    selected_actions = []
    remaining_budget = budget_cents
    for index in range(len(actions) - 1, -1, -1):
        if decisions_by_action[index][remaining_budget]:
            selected_actions.append(actions[index])
            remaining_budget -= int(actions[index][1] * 100)
    selected_actions.reverse()
    return selected_actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", nargs="?", type=Path, default=DEFAULT_FILE)
    arguments = parser.parse_args()

    start_time = perf_counter()
    try:
        actions, report = load_actions(arguments.csv_file)
        best_actions = find_best_investment(actions)
        elapsed_seconds = perf_counter() - start_time
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print_result(best_actions, report)
    print(f"Temps de lecture et de recherche : {elapsed_seconds:.4f} s")


if __name__ == "__main__":
    main()
