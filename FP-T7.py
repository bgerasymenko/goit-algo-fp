#!/usr/bin/env python3
"""
Завдання 7. Імітація кидків двох кубиків методом Монте-Карло
та порівняння з аналітичними ймовірностями.
"""
import argparse
import random
from collections import Counter
import matplotlib.pyplot as plt
import os

# Аналітичні ймовірності для суми двох шестигранних кубиків
ANALYTICAL = {
    2: 1/36,  3: 2/36,  4: 3/36,  5: 4/36,
    6: 5/36,  7: 6/36,  8: 5/36,  9: 4/36,
    10:3/36, 11:2/36, 12:1/36
}

def simulate(trials: int) -> Counter:
    """Повертає лічильник випадків для сум двох кубиків."""
    counts = Counter()
    for _ in range(trials):
        s = random.randint(1,6) + random.randint(1,6)
        counts[s] += 1
    return counts

def plot_probabilities(sim_probs, analytic_probs, output: str):
    """Будує та зберігає графік порівняння імовірностей."""
    sums = list(range(2,13))
    mc = [sim_probs[s] for s in sums]
    an = [analytic_probs[s] for s in sums]

    plt.figure(figsize=(8,5))
    plt.bar(sums, mc, width=0.6, label='Monte Carlo', alpha=0.7)
    plt.plot(sums, an, 'r-o', label='Аналітична', linewidth=2)
    plt.xlabel('Сума на кубиках')
    plt.ylabel('Ймовірність')
    plt.title('Ймовірності сум при киданні двох кубиків')
    plt.xticks(sums)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
    plt.savefig(output, dpi=300)
    plt.close()
    print(f"Plot saved to {output}")

def generate_readme(sim_probs, analytic_probs, trials, plot_file, path='README.md'):
    """Генерує README.md з таблицею та висновками."""
    lines = []
    lines.append('# Завдання 7. Імітація кидків двох кубиків методом Монте-Карло')
    lines.append(f'- Кількість симуляцій: **{trials:,}**\n')
    lines.append('| Сума | MC імовірність | Аналітична імовірність |')
    lines.append('|:----:|:--------------:|:----------------------:|')
    for s in range(2, 13):
        p_mc = sim_probs[s]
        p_an = analytic_probs[s]
        lines.append(f'|  {s}  |    {p_mc:.4%}    |       {p_an:.4%}       |')
    lines.append('\n## Графік\n')
    lines.append(f'![]({plot_file})\n')
    lines.append('## Висновки')
    lines.append('- Імітація методом Монте-Карло добре апроксимує аналітичні ймовірності.')
    lines.append('- Похибка зменшується зі збільшенням кількості симуляцій.')
    lines.append('- Для найчастішої суми (7) симульована ймовірність найближча до теоретичної.\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"README generated at {path}")

def main():
    parser = argparse.ArgumentParser(
        description="Завдання 7: кидки двох кубиків Monte Carlo"
    )
    parser.add_argument('--trials', '-n', type=int, default=1_000_000,
                        help='Кількість симуляцій (за замовчуванням: 1_000_000)')
    parser.add_argument('--plot', '-p', default='dice_probs.png',
                        help='Файл для збереження графіка (PNG)')
    parser.add_argument('--readme', '-r', default='README.md',
                        help='Шлях до README (Markdown)')
    args = parser.parse_args()

    # Імітація
    counts = simulate(args.trials)
    # Переводимо лічильники у ймовірності
    sim_probs = {s: counts[s]/args.trials for s in range(2,13)}

    # Побудова графіка
    plot_probabilities(sim_probs, ANALYTICAL, args.plot)

    # Генерація README
    generate_readme(sim_probs, ANALYTICAL, args.trials, args.plot, path=args.readme)

if __name__ == '__main__':
    main()
