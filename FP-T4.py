#!/usr/bin/env python3
import argparse
import networkx as nx
import matplotlib.pyplot as plt
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

def visualize_heap(heap, output):
    print("1) Building heap graph from:", heap)
    G, pos = build_heap_graph(heap)

    labels = nx.get_node_attributes(G, 'label')
    print("2) Rendering and saving visualization to:", output)
    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos,
        labels=labels,
        with_labels=True,
        arrows=False,
        node_size=1500,
        node_color='skyblue',
        edge_color='#555555',
        font_weight='bold'
    )
    plt.axis('off')
    plt.tight_layout()

    # Створюємо теку, якщо потрібно
    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)

    plt.savefig(output, dpi=300)
    plt.close()
    print(f"3) Done! File available at: {output}")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Візуалізація бінарної купи як дерева"
    )
    parser.add_argument(
        '--heap', '-H',
        default="10,5,3,2,4,1",
        help="(Опційно) Елементи купи через коми, напр.: 10,5,3,2,4,1"
    )
    parser.add_argument(
        '--output', '-o',
        default='heap.png',
        help="Файл для збереження зображення (PNG). За замовчуванням: heap.png"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    # Розбираємо рядок у список цілих
    try:
        heap = [int(x.strip()) for x in args.heap.split(',') if x.strip()!='']
    except ValueError:
        print("Error: всі елементи heap повинні бути цілими числами, розділеними комами.")
        return

    visualize_heap(heap, args.output)

if __name__ == '__main__':
    main()
