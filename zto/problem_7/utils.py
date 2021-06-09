from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np

from .problem import FlowSolution


def get_pareto(solutions: list[FlowSolution]) -> list[FlowSolution]:
    s_num = len(solutions)

    drop_idx = []
    for i in range(s_num):
        for j in range(s_num):
            if i != j and solutions[j].dominates(solutions[i]):
                drop_idx.append(i)
                break

    return [solutions[i] for i in range(s_num) if i not in drop_idx]


def solutions_to_points(
    solutions: list[FlowSolution],
    criterions: list[str],
) -> list[np.ndarray]:
    points = [[s.state[c] for c in criterions] for s in solutions]

    return [np.array(v) for v in zip(*points)]


def visualize_pareto(
    results: list[FlowSolution],
    pareto: list[FlowSolution],
    criterions: list[str],
) -> None:
    all_x, all_y = solutions_to_points(results, criterions)
    pareto_x, pareto_y = solutions_to_points(pareto, criterions)

    pareto_sort = pareto_x.argsort()
    pareto_x, pareto_y = pareto_x[pareto_sort], pareto_y[pareto_sort]

    plt.scatter(all_x, all_y)
    plt.plot(pareto_x, pareto_y, 'ro-')
    plt.show()


def get_area(x1: tuple[float, float], x2: tuple[float, float]) -> float:
    return (x2[0] - x1[0]) * (x2[1] - x1[1])


def get_hvi(
    paretos: list[list[FlowSolution]],
    criterions: list[str],
) -> list[float]:
    pareto_ps = []
    xs, ys = [], []
    for pareto in paretos:
        p = solutions_to_points(pareto, criterions)
        pareto_ps.append(p)

        xs.append(p[0])
        ys.append(p[1])
    z = [np.concatenate(xs).max(), np.concatenate(ys).max()]

    areas = []
    for pareto_p in pareto_ps:
        curr_z = z.copy()
        pareto_x, pareto_y = pareto_p
        sort_idx = pareto_x.argsort()
        pareto_x, pareto_y = pareto_x[sort_idx], pareto_y[sort_idx]

        total_area = 0
        for ps in zip(pareto_x, pareto_y):
            total_area += get_area(ps, curr_z)
            curr_z[1] = ps[1]

        areas.append(total_area)

    return areas


def bar_plot(solutions: list[FlowSolution], criterions: list[str]) -> None:
    width = 0.8 / len(criterions)
    ticks = np.array(range(len(solutions))) - width * 1.5

    points = solutions_to_points(solutions, criterions)
    for p, l in zip(points, criterions):
        plt.bar(ticks, p, width, label=l)
        ticks = ticks + width
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    plt.xticks(np.arange(len(ticks)), [f's{i}' for i in range(len(ticks))])
    plt.show()


def line_plot(solutions: list[FlowSolution], criterions: list[str]) -> None:
    points = solutions_to_points(solutions, criterions)
    points_m = np.stack(points)

    ito = plt.plot(points_m)
    plt.legend(
        ito,
        [f's{i}' for i in range(len(solutions))],
        bbox_to_anchor=(1.04, 1.0),
        loc='upper left',
    )
    plt.xticks(np.arange(len(criterions)), criterions)
    plt.show()


def scatter_plot(solutions: list[FlowSolution], criterions: list[str]) -> None:
    points = solutions_to_points(solutions, criterions)
    points_m = np.stack(points)

    all_ticks = []
    y_ticks = np.arange(len(criterions))
    for i, c_pt in enumerate(points_m.T):
        all_ticks.extend(y_ticks)
        plt.scatter(c_pt, y_ticks, label=f's{i}')
        y_ticks = y_ticks + len(criterions) + 1

    plt.yticks(all_ticks, len(solutions) * criterions)
    plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--')
    plt.show()
