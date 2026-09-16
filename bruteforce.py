import csv
from itertools import combinations
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "actions.csv"
MAX_BUDGET = 500


def calculate_profit(cost: float, profit_percent: float) -> float:
    """Calcule le bénéfice en euros d'une action."""
    return cost * profit_percent / 100


def generate_combinations(actions: list[dict]):
    """Génère toutes les combinaisons non vides d'actions."""
    for combination_size in range(1, len(actions) + 1):
        yield from combinations(actions, combination_size)


def find_best_investment(actions: list[dict], budget: float) -> dict:
    """Trouve la combinaison valide qui offre le meilleur bénéfice."""
    best_investment = {
        "actions": [],
        "cost": 0.0,
        "profit": 0.0,
    }

    for combination in generate_combinations(actions):
        total_cost = sum(action["cost"] for action in combination)

        if total_cost <= budget:
            total_profit = sum(action["profit"] for action in combination)

            if total_profit > best_investment["profit"]:
                best_investment = {
                    "actions": list(combination),
                    "cost": total_cost,
                    "profit": total_profit,
                }

    return best_investment


def load_actions(file_path: Path) -> list[dict]:
    """Charge les actions du fichier CSV dans une liste de dictionnaires."""
    actions = []

    with file_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            cost = float(row["Coût par action (en euros)"])
            profit_percent = float(
                row["Bénéfice (après 2 ans)"].rstrip("%")
            )

            action = {
                "name": row["Actions #"],
                "cost": cost,
                "profit_percent": profit_percent,
                "profit": calculate_profit(cost, profit_percent),
            }
            actions.append(action)

    return actions


if __name__ == "__main__":
    actions = load_actions(DATA_FILE)
    best_investment = find_best_investment(actions, MAX_BUDGET)

    print("Meilleur investissement :")
    for action in best_investment["actions"]:
        print(f"- {action['name']}: {action['cost']:.2f} €")

    print(f"Coût total : {best_investment['cost']:.2f} €")
    print(f"Bénéfice total : {best_investment['profit']:.2f} €")
