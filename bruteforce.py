import csv
from itertools import combinations
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "actions.csv"


def calculate_profit(cost: float, profit_percent: float) -> float:
    """Calcule le bénéfice en euros d'une action."""
    return cost * profit_percent / 100


def generate_combinations(actions: list[dict]):
    """Génère toutes les combinaisons non vides d'actions."""
    for combination_size in range(1, len(actions) + 1):
        yield from combinations(actions, combination_size)


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
    combination_count = sum(1 for _ in generate_combinations(actions))

    print(f"{len(actions)} actions chargées.")
    print(f"{combination_count} combinaisons non vides générées.")
