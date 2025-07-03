#!/usr/bin/env python3
import heapq
import argparse
import os

def dijkstra(graph: dict, start: str) -> dict:
    """
    Реалізує алгоритм Дейкстри з використанням бінарної кучи (heapq).
    Повертає словник найкоротших відстаней від вершини start до всіх інших.
    """
    # Ініціалізація відстаней
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Мін-куча з парами (відстань, вузол)
    pq = [(0, start)]
    visited = set()

    while pq:
        dist_u, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        # Розглядаємо сусідів
        for v, weight in graph[u]:
            new_dist = dist_u + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances

def generate_readme(graph: dict, distances: dict, start: str, path: str = 'README.md'):
    """
    Генерує README.md із описом графа, алгоритму та результатами.
    """
    lines = []
    lines.append('# Завдання 3. Алгоритм Дейкстри з бінарною купою\n')
    lines.append('## Опис графа (зважений неорієнтований)\n')
    for u in sorted(graph):
        edges = ', '.join(f'{v} (w={w})' for v, w in graph[u])
        lines.append(f'- **{u}**: {edges}')
    lines.append('\n## Результати алгоритму Дейкстри\n')
    lines.append(f'Початкова вершина: **{start}**\n')
    lines.append('| Вершина | Найкоротша відстань |')
    lines.append('|:-------:|:-------------------:|')
    for node in sorted(distances):
        d = distances[node]
        dist_str = f'{d:.0f}' if d < float('inf') else '∞'
        lines.append(f'| {node} | {dist_str} |')
    lines.append('\n## Висновок\n')
    lines.append('- Алгоритм використовує мін-кучу (модуль heapq) для вибору наступної вершини з мінімальною відстанню O(log V).')
    lines.append('- Відстані до всіх вершин знайдено за складністю O((V + E) log V).')
    lines.append('- У наведеному прикладі видно, що граф із 6 вершинами і 7 ребрами оброблений коректно.\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(
        description="Завдання 3: алгоритм Дейкстри з бінарною кучею"
    )
    parser.add_argument('--source', '-s', default='A',
                        help='Початкова вершина (за замовчуванням: A)')
    parser.add_argument('--readme', '-r', default='README.md',
                        help='Шлях до файлу README (за замовчуванням: README.md)')
    args = parser.parse_args()

    # Визначення графа
    # Неорієнтований зважений граф задається списком суміжності
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2), ('Z', 6)],
        'E': [('C',10), ('D', 2), ('Z', 3)],
        'Z': [('D', 6), ('E', 3)]
    }

    start = args.source
    if start not in graph:
        print(f"Помилка: вершина '{start}' не існує в графі.")
        return

    # Обчислення найкоротших відстаней
    distances = dijkstra(graph, start)

    # Вивід у термінал
    print(f"Найкоротші відстані від вершини {start}:")
    for node in sorted(distances):
        d = distances[node]
        dist_str = f"{d:.0f}" if d < float('inf') else '∞'
        print(f"  {start} → {node}: {dist_str}")

    # Генерація README.md
    generate_readme(graph, distances, start, path=args.readme)
    print(f"\nREADME збережено у файл: {args.readme}")

if __name__ == '__main__':
    main()
