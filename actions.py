"""Lecture commune des actions pour les deux algorithmes du projet."""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parent / "data"
DEFAULT_FILE = DATA_DIRECTORY / "actions.csv"
BUDGET_EUROS = Decimal("500")

# Une action contient, dans cet ordre : nom, prix, taux, bénéfice en euros.
Action = tuple[str, Decimal, Decimal, Decimal]


def load_actions(file_path: Path) -> tuple[list[Action], dict]:
    """Lit un CSV et écarte les lignes inutilisables ou ambiguës.

    Le rapport sert à expliquer combien de lignes ont été écartées.
    Les fichiers d'origine ne sont jamais modifiés.
    """
    file_path = Path(file_path)
    valid_actions = []
    invalid_names = set()
    rejection_reasons = {}
    total_rows = 0

    with file_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        french_columns = (
            "Actions #", "Coût par action (en euros)", "Bénéfice (après 2 ans)",
        )
        english_columns = ("name", "price", "profit")
        if reader.fieldnames and set(french_columns) <= set(reader.fieldnames):
            name_column, price_column, rate_column = french_columns
        elif reader.fieldnames and set(english_columns) <= set(reader.fieldnames):
            name_column, price_column, rate_column = english_columns
        else:
            raise ValueError(f"Colonnes CSV inconnues dans {file_path.name}.")

        for row in reader:
            total_rows += 1
            name = (row.get(name_column) or "").strip()
            price_text = (row.get(price_column) or "").strip()
            rate_text = (row.get(rate_column) or "").strip().removesuffix("%")

            reason = None
            if not name or not price_text or not rate_text or None in row:
                reason = "valeur manquante ou colonne en trop"
            else:
                try:
                    price_euros = Decimal(price_text)
                    profit_percent = Decimal(rate_text)
                except InvalidOperation:
                    reason = "nombre illisible"
                else:
                    if not price_euros.is_finite() or not profit_percent.is_finite():
                        reason = "nombre non fini"
                    elif price_euros <= 0:
                        reason = "prix nul ou négatif"
                    elif price_euros * 100 != (price_euros * 100).to_integral_value():
                        reason = "prix avec fraction de centime"
                    elif profit_percent <= 0:
                        reason = "taux nul ou négatif"

            if reason:
                rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
                if name:
                    invalid_names.add(name)
                continue

            profit_euros = price_euros * profit_percent / 100
            valid_actions.append((name, price_euros, profit_percent, profit_euros))

    # Un même nom avec deux valeurs différentes est ambigu : on l'écarte.
    # Si les lignes sont identiques, une seule action peut être achetée.
    actions_by_name = {}
    for action in valid_actions:
        actions_by_name.setdefault(action[0], []).append(action)

    actions = []
    for name, same_name_actions in actions_by_name.items():
        if name in invalid_names or len(set(same_name_actions)) > 1:
            reason = "nom avec données contradictoires"
            rejected_count = len(same_name_actions)
        else:
            actions.append(same_name_actions[0])
            reason = "nom répété à l'identique"
            rejected_count = len(same_name_actions) - 1
        if rejected_count:
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + rejected_count

    report = {
        "total_rows": total_rows,
        "accepted_rows": len(actions),
        "rejected_rows": total_rows - len(actions),
        "reasons": rejection_reasons,
    }
    return actions, report


def print_result(actions: list[Action], report: dict) -> None:
    """Affiche les achats, leur coût et leur bénéfice après deux ans."""
    total_cost = sum((action[1] for action in actions), Decimal("0"))
    total_profit = sum((action[3] for action in actions), Decimal("0"))
    print(f"{report['accepted_rows']} actions retenues, {report['rejected_rows']} lignes écartées.")
    print("Actions à acheter :")
    for name, price, percentage, profit in actions:
        print(f"  {name} : {price:.2f} €")
    print(f"Coût total : {total_cost:.2f} €")
    print(f"Bénéfice après deux ans : {total_profit:.2f} €")
