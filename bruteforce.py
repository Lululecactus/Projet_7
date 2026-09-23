import csv
from decimal import Decimal
from itertools import combinations
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "actions.csv"
MAX_BUDGET = Decimal("500")


def load_actions(file_path):
    """Charge les actions du CSV en liste de tuples (nom, coût, %, bénéfice_euros)."""
    actions = []
    with file_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Conversion directe du texte, sans passer par un float.
            cost = Decimal(row["Coût par action (en euros)"])
            profit_percent = Decimal(row["Bénéfice (après 2 ans)"].rstrip("%"))
            profit_euros = cost * profit_percent / 100
            actions.append((row["Actions #"], cost, profit_percent, profit_euros))
    return actions


def generate_combinations(actions):
    """Génère toutes les combinaisons non vides, toutes tailles confondues."""
    for size in range(1, len(actions) + 1):
        yield from combinations(actions, size)


def find_best_investment(actions, budget):
    """Renvoie TOUTES les combinaisons atteignant le bénéfice maximal, plus ce bénéfice.

    Renvoie une liste de (combinaison, coût) car plusieurs portefeuilles distincts
    peuvent atteindre exactement le même bénéfice maximal.
    Les coûts et les bénéfices des actions sont des Decimal.
    """
    best_combinations = []
    best_profit = Decimal("0")

    for combination in generate_combinations(actions):
        total_cost = sum(action[1] for action in combination)

        if total_cost <= budget:
            total_profit = sum(action[3] for action in combination)

            if total_profit > best_profit:
                # nouveau meilleur bénéfice : on repart d'une liste neuve
                best_profit = total_profit
                best_combinations = [(list(combination), total_cost)]
            elif total_profit == best_profit:
                # égalité avec le meilleur actuel : on l'ajoute aux solutions
                best_combinations.append((list(combination), total_cost))

    return best_combinations, best_profit


if __name__ == "__main__":
    actions = load_actions(DATA_FILE)
    best_combinations, best_profit = find_best_investment(actions, MAX_BUDGET)

    print(f"Bénéfice maximal possible : {best_profit:.2f} €")
    print(f"Nombre de portefeuilles atteignant ce maximum : {len(best_combinations)}\n")

    for i, (combo, cost) in enumerate(best_combinations, start=1):
        print(f"Solution {i} — coût total : {cost:.2f} €")
        for name, action_cost, _, _ in combo:
            print(f"  - {name}: {action_cost:.2f} €")
        print()
