from .problem import FlowSolution


def get_pareto(solutions: list[FlowSolution]) -> list[FlowSolution]:
    s_num = len(solutions)

    pareto_idx = []
    for i in range(s_num):
        append = True
        for j in range(s_num):
            if i != j and j not in pareto_idx and solutions[i] > solutions[j]:
                append = False
                break
        if append:
            pareto_idx.append(i)

    return [solutions[i] for i in pareto_idx]
