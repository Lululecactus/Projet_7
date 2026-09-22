import csv
from itertools import combinations
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "actions.csv"
MAX_BUDGET = 500

# Une action : (nom, coût en euros, taux en %, bénéfice en euros).
Action = tuple[str, float, float, float]


def calculate_profit(cost: float, profit_percent: float) -> float:
    """Calcule le bénéfice en euros d'une action."""
    return cost * profit_percent / 100


def generate_combinations(actions: list[Action]):
    """Génère toutes les combinaisons non vides d'actions."""
    for combination_size in range(1, len(actions) + 1):
        yield from combinations(actions, combination_size)


def find_best_investment(
    actions: list[Action], budget: float
) -> tuple[list[Action], float, float]:
    """Renvoie les actions choisies, leur coût et leur bénéfice."""
    best_actions = []
    best_cost = 0.0
    best_profit = 0.0

    for combination in generate_combinations(actions):
        total_cost = sum(action[1] for action in combination)

        if total_cost <= budget:
            total_profit = sum(action[3] for action in combination)

            if total_profit > best_profit:
                best_actions = list(combination)
                best_cost = total_cost
                best_profit = total_profit

    return best_actions, best_cost, best_profit


def load_actions(file_path: Path) -> list[Action]:
    """Charge les actions du fichier CSV dans une liste de tuples."""
    actions = []

    with file_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            cost = float(row["Coût par action (en euros)"])
            profit_percent = float(
                row["Bénéfice (après 2 ans)"].rstrip("%")
            )

            action = (
                row["Actions #"],
                cost,
                profit_percent,
                calculate_profit(cost, profit_percent),
            )
            actions.append(action)

    return actions


if __name__ == "__main__":
    actions = load_actions(DATA_FILE)
    best_actions, total_cost, total_profit = find_best_investment(
        actions, MAX_BUDGET
    )

    print("Meilleur investissement :")
    for name, cost, profit_percent, profit in best_actions:
        print(f"- {name}: {cost:.2f} €")

    print(f"Coût total : {total_cost:.2f} €")
    print(f"Bénéfice total : {total_profit:.2f} €")
