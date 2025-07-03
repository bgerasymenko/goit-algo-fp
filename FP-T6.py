#!/usr/bin/env python3

# Дані про їжу: вартість (cost) і калорійність (calories)
ITEMS = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}

def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм: вибирає страви за найбільшим співвідношенням calories/cost,
    поки бюджет не вичерпається.
    Повертає (selection_dict, total_cost, total_calories).
    """
    sorted_items = sorted(
        items.items(),
        key=lambda kv: kv[1]['calories'] / kv[1]['cost'],
        reverse=True
    )
    selection = {}
    total_cost = 0
    total_cal = 0
    for name, data in sorted_items:
        cost = data['cost']
        cal  = data['calories']
        if total_cost + cost <= budget:
            selection[name] = selection.get(name, 0) + 1
            total_cost += cost
            total_cal  += cal
    return selection, total_cost, total_cal

def dynamic_programming(items, budget):
    """
    0/1 knapsack DP: максимізує калорії при обмеженні budget.
    Повертає (selection_dict, total_cost, total_calories).
    """
    names = list(items.keys())
    costs = [items[n]['cost']     for n in names]
    cals  = [items[n]['calories'] for n in names]
    n = len(names)

    dp = [[0]*(budget+1) for _ in range(n+1)]
    keep = [[0]*(budget+1) for _ in range(n+1)]

    for i in range(1, n+1):
        ci, vi = costs[i-1], cals[i-1]
        for w in range(budget+1):
            dp[i][w] = dp[i-1][w]
            if ci <= w:
                val = dp[i-1][w-ci] + vi
                if val > dp[i][w]:
                    dp[i][w] = val
                    keep[i][w] = 1

    w = budget
    selection = {}
    for i in range(n, 0, -1):
        if keep[i][w]:
            name = names[i-1]
            selection[name] = selection.get(name, 0) + 1
            w -= costs[i-1]

    total_cal = dp[n][budget]
    total_cost = sum(items[name]['cost']*cnt for name,cnt in selection.items())
    return selection, total_cost, total_cal

if __name__ == '__main__':
    BUDGET = 100
    print(f"Приклад: бюджет = {BUDGET}\n")

    sel_g, cost_g, cal_g = greedy_algorithm(ITEMS, BUDGET)
    print("=== Жадібний алгоритм ===")
    print(f"Вибрано страв: {sel_g}")
    print(f"Витрачено коштів: {cost_g}")
    print(f"Отримано калорій: {cal_g}\n")

    sel_dp, cost_dp, cal_dp = dynamic_programming(ITEMS, BUDGET)
    print("=== Динамічне програмування ===")
    print(f"Вибрано страв: {sel_dp}")
    print(f"Витрачено коштів: {cost_dp}")
    print(f"Отримано калорій: {cal_dp}\n")

    print("=== Порівняння ===")
    if cal_dp > cal_g:
        print("DP-підхід дав кращий результат.")
    elif cal_dp == cal_g:
        print("Обидва підходи дали однакову калорійність.")
    else:
        print("Жадібний підхід дав кращий результат.")
