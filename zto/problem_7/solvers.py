from random import random

from .problem import FlowProblem, FlowSolution


class Solver:
    def __init__(self, max_iters: int) -> None:
        self.max_iters = max_iters

    def solve(self, problem: FlowProblem) -> list[FlowSolution]:
        self.problem = problem

        solution = problem.initialize()
        solution.evalueate(problem)
        selected_solutions = [solution]

        add_prob_base = 0.995
        add_prob = 1
        for _ in range(self.max_iters):
            add_prob *= add_prob_base

            new_solution = solution.get_nb()
            new_solution.evalueate(problem)
            if solution > new_solution or random() < add_prob:
                solution = new_solution
                selected_solutions.append(solution)

        return selected_solutions
