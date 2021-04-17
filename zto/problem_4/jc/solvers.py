from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import total_ordering
from queue import PriorityQueue
from typing import Any, Literal, Optional

OPTIMIZATION = Literal['min', 'max']
INIT = Literal['none', 'rand', 'greedy', 'dfs']


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


@total_ordering
class Solution(ABC):
    def __init__(self, value: int, is_final: bool = False) -> None:
        self.is_final = is_final
        self.value = value

    def __gt__(self, other: 'Solution') -> bool:
        return self.value > other.value

    def __eq__(self, other: 'Solution') -> bool:
        return self.value == other.value

    @abstractmethod
    def visualize(self) -> None:
        pass


class Problem(ABC):
    @abstractmethod
    def get_rand_solution(self) -> Solution:
        pass

    @abstractmethod
    def get_greedy_solution(self) -> Solution:
        pass

    @abstractmethod
    def get_dfs_solution(self) -> Solution:
        pass

    @abstractmethod
    def expand(self, solution: Optional[Solution] = None) -> list[Solution]:
        pass


class Solver(ABC):
    def __init__(self, optimization_type: OPTIMIZATION) -> None:
        self.optimization_type = optimization_type
        self.best_solution = None

    @abstractmethod
    def optimize(self, problem: Problem) -> Optional[Solution]:
        pass

    def _update_best_solution(self, solution: Solution) -> None:
        if self.best_solution is None:
            self.best_solution = solution
        elif self.optimization_type == 'max':
            if self.best_solution < solution:
                self.best_solution = solution
        else:
            if self.best_solution > solution:
                self.best_solution = solution


class BranchAndBound(Solver):
    def __init__(self, optimization_type: OPTIMIZATION, init_type: INIT) -> None:
        super().__init__(optimization_type)
        self.init_type = init_type
        self.queue: PriorityQueue[
            PrioritizedItem
        ] = PriorityQueue()  # lower priority first

    def optimize(self, problem: Problem) -> Optional[Solution]:
        self._init_best_solution(problem)

        solutions = problem.expand()
        for solution in self._prune(solutions):
            self._enqueue_solution(solution)

        while not self.queue.empty():
            solution: Solution = self.queue.get().item

            if solution.is_final:
                self._update_best_solution(solution)
            else:
                subsolutions = problem.expand(solution)
                for new_solution in self._prune(subsolutions):
                    self._enqueue_solution(new_solution)

        return self.best_solution

    def _enqueue_solution(self, solution: Solution) -> None:
        priority = (
            -solution.value if self.optimization_type == 'max' else solution.value
        )

        self.queue.put(PrioritizedItem(priority, solution))

    def _init_best_solution(self, problem: Problem) -> None:
        if self.init_type == 'rand':
            self.best_solution = problem.get_rand_solution()
        elif self.init_type == 'greedy':
            self.best_solution = problem.get_greedy_solution()
        elif self.init_type == 'dfs':
            self.best_solution = problem.get_dfs_solution()

    def _prune(self, solutions: list[Solution]) -> list[Solution]:
        if self.best_solution is None:
            return solutions

        # NOTE is gt/lt better than ge/le ?
        if self.optimization_type == 'max':
            f = lambda s: s > self.best_solution
        else:
            f = lambda s: s < self.best_solution
        f_solutions = filter(f, solutions)

        return list(f_solutions)


class BruteForce(Solver):
    def __init__(self, optimization_type: OPTIMIZATION) -> None:
        super().__init__(optimization_type)
        self.queue = []

    def optimize(self, problem: Problem) -> Optional[Solution]:
        self.queue = problem.expand()

        while self.queue:
            solution = self.queue.pop()

            if solution.is_final:
                self._update_best_solution(solution)
            else:
                new_solutions = problem.expand(solution)
                self.queue.extend(new_solutions)

        return self.best_solution
