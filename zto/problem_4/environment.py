from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

from .PSSP import PSSPProblem
from .solvers import INIT, BranchAndBound, BruteForce

if TYPE_CHECKING:
    from .solvers import Problem, Solver

METHOD = Literal['bb', 'bf']


class Environment(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.solver: Solver
        self.problem: Problem

    @abstractmethod
    def run(self) -> None:
        pass


class P4Environment(Environment):
    def __init__(
        self,
        method: METHOD,
        init_type: INIT,
        enqueue_limit: int,
        tasks: int,
        machines: int,
        seed: int,
    ) -> None:
        optimization_type = 'min'

        if method == 'bb':
            self.solver = BranchAndBound(optimization_type, init_type, enqueue_limit)
        elif method == 'bf':
            self.solver = BruteForce(optimization_type)

        self.problem = PSSPProblem(tasks, machines, seed)

    def run(self) -> None:
        self.solver.solve(self.problem)
