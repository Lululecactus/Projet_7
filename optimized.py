from decimal import Decimal
from time import perf_counter

from bruteforce import DATA_FILE, MAX_BUDGET, load_actions


def convert_to_cents(amount: Decimal) -> int:
    """Convertit un montant positif ou nul en centimes, sans arrondi."""
    if not amount.is_finite() or amount < 0:
        raise ValueError("Le montant doit être un nombre fini positif ou nul.")

    amount_in_cents = amount * 100
    if amount_in_cents != amount_in_cents.to_integral_value():
        raise ValueError("Le montant doit être un multiple de 0,01 euro.")

    return int(amount_in_cents)


def reconstruct_selected_actions(
    actions,
    action_costs_cents,
    purchase_decisions_by_action,
    budget_cents,
):
    """Retrouve un portefeuille optimal en remontant les décisions."""
    selected_actions = []
    remaining_budget_cents = budget_cents

    for action_index in range(len(actions) - 1, -1, -1):
        purchase_decisions = purchase_decisions_by_action[action_index]
        if purchase_decisions[remaining_budget_cents]:
            selected_actions.append(actions[action_index])
            remaining_budget_cents -= action_costs_cents[action_index]

    selected_actions.reverse()
    return selected_actions


def find_best_investment(actions, budget):
    """Renvoie un portefeuille optimal, son coût et son bénéfice.

    Chaque action est un tuple (nom, coût, taux, bénéfice), avec des Decimal.
    Les prix sont strictement positifs et exprimables en centimes entiers.
    En cas d'ex aequo, on conserve le choix déjà enregistré.
    """
    budget_cents = convert_to_cents(budget)
    action_costs_cents = []
    for action in actions:
        action_cost_cents = convert_to_cents(action[1])
        if action_cost_cents == 0:
            raise ValueError("Le prix d'une action doit être strictement positif.")
        if not action[3].is_finite():
            raise ValueError("Le bénéfice d'une action doit être un nombre fini.")
        action_costs_cents.append(action_cost_cents)

    best_profit_by_budget = [Decimal("0")] * (budget_cents + 1)
    purchase_decisions_by_action = []

    for action_index, action in enumerate(actions):
        action_cost_cents = action_costs_cents[action_index]
        action_profit = action[3]
        # Un octet par budget : 1 si on achète cette action, 0 sinon.
        purchase_decisions = bytearray(budget_cents + 1)

        # Descendre empêche de réutiliser la même action dans ce passage.
        for available_budget_cents in range(
            budget_cents, action_cost_cents - 1, -1
        ):
            profit_without_action = best_profit_by_budget[available_budget_cents]
            remaining_budget_cents = available_budget_cents - action_cost_cents
            profit_with_action = (
                action_profit + best_profit_by_budget[remaining_budget_cents]
            )

            if profit_with_action > profit_without_action:
                best_profit_by_budget[available_budget_cents] = profit_with_action
                purchase_decisions[available_budget_cents] = 1

        purchase_decisions_by_action.append(purchase_decisions)

    selected_actions = reconstruct_selected_actions(
        actions, action_costs_cents, purchase_decisions_by_action, budget_cents
    )
    total_cost = sum((action[1] for action in selected_actions), Decimal("0"))
    best_profit = best_profit_by_budget[budget_cents]

    return selected_actions, total_cost, best_profit


if __name__ == "__main__":
    start_time = perf_counter()
    actions = load_actions(DATA_FILE)
    selected_actions, total_cost, best_profit = find_best_investment(
        actions, MAX_BUDGET
    )
    elapsed_seconds = perf_counter() - start_time

    print("Portefeuille optimal :")
    for action_name, action_cost, profit_percent, action_profit in selected_actions:
        print(f"  - {action_name}: {action_cost:.2f} €")

    print(f"Coût total : {total_cost:.2f} €")
    print(f"Bénéfice total : {best_profit:.2f} €")
    print(f"Temps de lecture et de recherche : {elapsed_seconds:.4f} s")
