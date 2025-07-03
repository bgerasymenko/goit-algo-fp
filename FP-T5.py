#!/usr/bin/env python3
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import os

def build_heap_graph(heap):
    G = nx.DiGraph()
    pos = {}
    def _add(i, x, y, layer):
        if i >= len(heap):
            return
        G.add_node(i, label=str(heap[i]))
        pos[i] = (x, y)
        left, right = 2*i + 1, 2*i + 2
        if left < len(heap):
            G.add_edge(i, left)
            _add(left, x - 1/2**layer, y - 1, layer + 1)
        if right < len(heap):
            G.add_edge(i, right)
            _add(right, x + 1/2**layer, y - 1, layer + 1)
    _add(0, 0.0, 0.0, 1)
    return G, pos

def get_color_list(base_hex, n):
    base_rgb = tuple(int(base_hex[i:i+2],16) for i in (1,3,5))
    colors = []
    for idx in range(n):
        t = idx/(n-1) if n>1 else 0
        r = int(base_rgb[0]*(1-t) + 255*t)
        g = int(base_rgb[1]*(1-t) + 255*t)
        b = int(base_rgb[2]*(1-t) + 255*t)
        colors.append(f'#{r:02X}{g:02X}{b:02X}')
    return colors

def bfs_order(G, start=0):
    visited = {start}
    order = [start]
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in G.successors(u):
            if v not in visited:
                visited.add(v)
                order.append(v)
                queue.append(v)
    return order

def dfs_order(G, start=0):
    visited = {start}
    order = [start]
    stack = [start]
    while stack:
        u = stack.pop()
        for v in reversed(list(G.successors(u))):
            if v not in visited:
                visited.add(v)
                order.append(v)
                stack.append(v)
    return order

def draw_and_save(G, pos, labels, color_map, output_file):
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, labels=labels, with_labels=True,
            arrows=False, node_size=1500,
            node_color=color_map, edge_color='#555555',
            font_weight='bold')
    plt.axis('off')
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    plt.savefig(output_file, dpi=300)
    plt.close()

def generate_readme(heap, bfs_vals, dfs_vals, bfs_img, dfs_img, readme_path):
    lines = [
        '# Завдання 5. Візуалізація обходу бінарного дерева\n',
        '## Вхідні дані\n',
        f'- Купа (масив): {heap}\n',
        '## Порядок обходу BFS\n',
        ' '.join(str(v) for v in bfs_vals) + '\n',
        '## Порядок обходу DFS\n',
        ' '.join(str(v) for v in dfs_vals) + '\n',
        '## Візуалізації\n',
        f'![BFS]({bfs_img})\n',
        f'![DFS]({dfs_img})\n',
        '## Висновок\n',
        '- **BFS** (черга) відвідує вузли по рівнях зверху вниз.\n',
        '- **DFS** (стек) заглиблюється в дерево, відвідуючи дітей перед переходом до інших гілок.\n'
    ]
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(
        description="Візуалізація обходу бінарного дерева (heap)"
    )
    parser.add_argument('--heap', '-H',
                        default="10,5,3,2,4,1",
                        help="(Опційно) Елементи купи через коми, напр.: 10,5,3,2,4,1")
    parser.add_argument('--prefix', '-p',
                        default='heap',
                        help="Префікс для вихідних файлів (default: heap)")
    parser.add_argument('--readme', '-r',
                        default='README.md',
                        help="Шлях до README (default: README.md)")
    args = parser.parse_args()

    # Розбираємо рядок у список цілих
    heap = [int(x) for x in args.heap.split(',') if x.strip()]

    # Будуємо граф та позиції
    G, pos = build_heap_graph(heap)
    labels = nx.get_node_attributes(G, 'label')

    # Обчислюємо порядки обходу і мапимо на значення
    bfs_idx = bfs_order(G)
    dfs_idx = dfs_order(G)
    bfs_vals = [heap[i] for i in bfs_idx]
    dfs_vals = [heap[i] for i in dfs_idx]

    # Генеруємо градації кольорів від #1296F0 до білих
    n = len(heap)
    base_color = '#1296F0'
    bfs_colors = get_color_list(base_color, n)
    dfs_colors = get_color_list(base_color, n)
    bfs_color_map = [bfs_colors[bfs_idx.index(i)] for i in G.nodes()]
    dfs_color_map = [dfs_colors[dfs_idx.index(i)] for i in G.nodes()]

    # Файли для збереження
    bfs_img = f"{args.prefix}_bfs.png"
    dfs_img = f"{args.prefix}_dfs.png"

    print("1) Малюємо BFS...") 
    draw_and_save(G, pos, labels, bfs_color_map, bfs_img)
    print(f"   BFS-зображення збережено: {bfs_img}")

    print("2) Малюємо DFS...")
    draw_and_save(G, pos, labels, dfs_color_map, dfs_img)
    print(f"   DFS-зображення збережено: {dfs_img}")

    print("3) Генеруємо README...")
    generate_readme(heap, bfs_vals, dfs_vals, bfs_img, dfs_img, args.readme)
    print(f"   README збережено у: {args.readme}")

if __name__ == '__main__':
    main()
