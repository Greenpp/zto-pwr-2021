from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any, Literal

OPTIMIZATION = Literal['min', 'max']
INIT = Literal['none', 'rand', 'greedy', 'dfs']


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class Solution(ABC):
    def __init__(self, is_final: bool = False) -> None:
        self.is_final = is_final

    @abstractmethod
    def __gt__(self, s2):
        pass

    @abstractmethod
    def __lt__(self, s2):
        pass


class Problem(ABC):
    @abstractmethod
    def get_next_min(self):
        pass

    @abstractmethod
    def get_next_max(self):
        pass


class BranchAndBound:
    def __init__(self, optimization_type: OPTIMIZATION, init_type: INIT) -> None:
        self.optimization_type = optimization_type
        self.init_type = init_type
        self.queue = PriorityQueue()  # lower priority first

        self.best_solution = None

    def optimize(self, problem: Problem) -> Solution:
        # TODO init best solution
        # TODO expand first level

        while not self.queue.empty():
            solution: Solution = self.queue.get()

            if solution.is_final:
                if self.optimization_type == 'max':
                    if self.best_solution < solution:
                        self.best_solution = solution
                else:
                    if self.best_solution > solution:
                        self.best_solution = solution
            else:
                pass  # TODO expand ,prune, add to queue

        return self.best_solution
