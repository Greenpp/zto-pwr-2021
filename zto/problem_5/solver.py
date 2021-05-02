import math
import random
from timeit import default_timer
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .QAP import QAPProblem, QAPSolution

INIT_LITERAL = Literal['rnd', 'best', 'greedy']
UPDATE_LITERAL = Literal['geo', 'lin']


class RandomSolver:
    def __init__(
        self,
        initialization: INIT_LITERAL = 'rnd',
        iteration_limit: int = 100,
        annealing: bool = False,
        temperature_update: UPDATE_LITERAL = 'geo',
        temperature_change: float = 0.9,
    ) -> None:
        self.initialization = initialization

        self.iteration_limit = iteration_limit

        self.annealing = annealing
        self.temperature_update = temperature_update
        self.temperature_change = temperature_change

    def _stop_condition_not_met(self) -> bool:
        if self.iteration_limit > 0:
            iteration_limit = self.iteration < self.iteration_limit
        else:
            iteration_limit = True

        # TODO
        # - local minimum
        # - timeout

        return iteration_limit

    def _init_temperature(self, problem: 'QAPProblem') -> None:
        problems = [problem.get_random_solution() for _ in range(1000)]
        p_max = max(problems, key=lambda p: p.cost)
        p_min = min(problems, key=lambda p: p.cost)

        p_range = p_max.cost - p_min.cost

        self.temperature = p_range

    def _accept(self, solution: 'QAPSolution') -> bool:
        last_val = self.current_solution.cost
        new_val = solution.cost

        threshold = math.e ** (-(new_val - last_val) / self.temperature)
        return random.random() < threshold

    def _update_temperature(self) -> None:
        if self.temperature_update == 'geo':
            self.temperature *= self.temperature_change
        elif self.temperature_update == 'lin':
            self.temperature = max(0, self.temperature - self.temperature_change)

    def _init_solution(self, problem: 'QAPProblem') -> None:
        if self.initialization == 'rnd':
            self.best_solution = problem.get_random_solution()
        elif self.initialization == 'best':
            solutions = [problem.get_random_solution() for _ in range(100)]
            self.best_solution = min(solutions, key=lambda s: s.cost)
        elif self.initialization == 'greedy':
            # TODO
            # - greedy
            pass

        self.current_solution = self.best_solution

    def _solve(self, problem: 'QAPProblem') -> 'QAPSolution':
        if self.annealing:
            self._init_temperature(problem)

        self._init_solution(problem)
        self.iteration = 0
        while self._stop_condition_not_met():
            new_solution = problem.get_random_neighbor(self.current_solution)
            if new_solution < self.best_solution:
                self.best_solution = new_solution
                self.current_solution = new_solution
            elif self.annealing and self._accept(new_solution):
                self.current_solution = new_solution

            if self.annealing:
                self._update_temperature()
            self.iteration += 1

        return self.best_solution

    def solve(self, problem: 'QAPProblem') -> 'QAPSolution':
        time_start = default_timer()
        solution = self._solve(problem)
        time_end = default_timer()

        self.solution_time = time_end - time_start

        return solution
