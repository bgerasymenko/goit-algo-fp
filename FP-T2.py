#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_pythagoras_tree(ax, x, y, size, angle, depth):
    if depth == 0:
        return
    dx = size * np.cos(angle)
    dy = size * np.sin(angle)
    pdx = -dy
    pdy = dx

    p0 = np.array([x, y])
    p1 = p0 + np.array([dx, dy])
    p2 = p1 + np.array([pdx, pdy])
    p3 = p0 + np.array([pdx, pdy])

    square = np.vstack([p0, p1, p2, p3])
    patch = Polygon(square, closed=True,
                    edgecolor='saddlebrown', facecolor='lightgreen')
    ax.add_patch(patch)

    theta = np.pi / 4
    size_left  = size * np.cos(theta)
    size_right = size * np.sin(theta)

    draw_pythagoras_tree(ax, p3[0], p3[1], size_left,  angle + theta, depth-1)
    draw_pythagoras_tree(ax, p2[0], p2[1], size_right, angle - theta, depth-1)

def main():
    parser = argparse.ArgumentParser(
        description="Фрактал «дерево Піфагора» з рекурсією"
    )
    parser.add_argument('-d', '--depth', type=int, default=6,
                        help="Рівень рекурсії (за замовчуванням: 6)")
    parser.add_argument('-o', '--output', default='tree.png',
                        help="Файл для збереження зображення (за замовчуванням: tree.png)")
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    draw_pythagoras_tree(ax, x=-0.5, y=0.0, size=1.0, angle=0.0, depth=args.depth)
    ax.relim(); ax.autoscale_view()

    plt.tight_layout()
    plt.savefig(args.output, dpi=300)
    print(f"Фрактал збережено у файл: {args.output}")

if __name__ == "__main__":
    main()
