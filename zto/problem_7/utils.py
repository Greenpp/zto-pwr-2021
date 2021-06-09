import random

import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

from .problem import (
    MAX_TARD,
    MIX,
    TOTAL_FLOW,
    TOTAL_LATE,
    TOTAL_TARD,
    FlowProblem,
    FlowSolution,
)
from .solvers import Solver

SEEDS = [81178, 34091, 75746, 65927, 1173, 70912, 19419, 50363, 82748, 4511]
ITER_LIMITS = [100, 200, 400, 800, 1600]
TASKS = 15


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
    scale: float = 1.0,
) -> list[float]:
    pareto_ps = []
    xs, ys = [], []
    for pareto in paretos:
        p = solutions_to_points(pareto, criterions)
        pareto_ps.append(p)

        xs.append(p[0])
        ys.append(p[1])
    z = [
        scale * np.concatenate(xs).max(),
        scale * np.concatenate(ys).max(),
    ]

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


def visualize_for_iteration_limit(vales: list[float]) -> None:
    plt.plot(ITER_LIMITS, vales)
    plt.xticks(ITER_LIMITS)
    plt.show()


def tabularize_for_iteration_limit(values: list[float], name: str) -> None:
    t = tabulate(
        [[il, v] for il, v in zip(ITER_LIMITS, values)],
        headers=['Iteration limit', name],
        tablefmt='github',
        floatfmt='.1f',
    )

    print(t)


def get_latex_star(
    selected: list[FlowSolution],
    all_solutions: list[FlowSolution],
    criterions: list[str],
) -> None:
    vals = solutions_to_points(all_solutions, criterions)
    max_vals = [v.max() for v in vals]
    positions = [(0, 0), (0, 3), (3, 0), (3, 3)]

    for ss, pos in zip(selected, positions):
        x, y = pos

        total_flow = ss.state[TOTAL_FLOW] / max_vals[0]
        max_tard = ss.state[MAX_TARD] / max_vals[1]
        total_tard = ss.state[TOTAL_TARD] / max_vals[2]
        total_late = ss.state[TOTAL_LATE] / max_vals[3]
        star_code = f'\\startcord{{{total_flow}}}{{{max_tard}}}{{{total_tard}}}{{{total_late}}}{{{x}}}{{{y}}}{{yellow}}'

        print(star_code)


def zad1(seeds: list[int]) -> None:
    criterions = [TOTAL_FLOW, MAX_TARD]

    all_hvis = []
    for il in ITER_LIMITS:
        all_paretos = []
        for seed in seeds:
            random.seed(seed)

            problem = FlowProblem(TASKS, criterions)
            solver = Solver(il)
            solutions = solver.solve(problem)

            pareto = get_pareto(solutions)

            all_paretos.append(pareto)
        visualize_pareto(solutions, pareto, criterions)

        hvis = get_hvi(all_paretos, criterions, 1.2)
        all_hvis.append(np.mean(hvis))

    visualize_for_iteration_limit(all_hvis)
    tabularize_for_iteration_limit(all_hvis, 'HVI')


def zad2(seeds: list[int]) -> None:
    criterions = [MIX]

    all_mixs = []
    for il in ITER_LIMITS:
        seed_mixs = []
        for seed in seeds:
            random.seed(seed)

            problem = FlowProblem(TASKS, criterions)
            solver = Solver(il)
            solutions = solver.solve(problem)

            final_mix = solutions[-1].state[MIX]
            seed_mixs.append(final_mix)
        all_mixs.append(np.mean(seed_mixs))

    visualize_for_iteration_limit(all_mixs)
    tabularize_for_iteration_limit(all_mixs, 'Value')


def zad3(seed: int) -> None:
    random.seed(seed)

    criterions = [TOTAL_FLOW, MAX_TARD, TOTAL_TARD, TOTAL_LATE]

    problem = FlowProblem(5, criterions)
    solver = Solver(800)

    solutions = solver.solve(problem)
    pareto = get_pareto(solutions)

    good_s = pareto[:3]
    bad_s = [solutions[0]]
    combined_solutions = good_s + bad_s

    bar_plot(combined_solutions, criterions)
    line_plot(combined_solutions, criterions)
    scatter_plot(combined_solutions, criterions)

    get_latex_star(combined_solutions, solutions, criterions)
