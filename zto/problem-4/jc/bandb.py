from abc import ABC
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
    def __init__(self, value: int) -> None:
        self.value = value

    def __gt__(self, s2):
        pass


class Problem(ABC):
    def get_next_min(self):
        pass

    def get_next_max(self):
        pass


class BranchAndBound:
    def __init__(self, optimization: OPTIMIZATION, init: INIT) -> None:
        self.optimization = optimization
        self.queue = PriorityQueue()
