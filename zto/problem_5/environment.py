import random

from zto.problem_5.QAP import QAPProblem

from .solver import INIT_LITERAL, UPDATE_LITERAL, RandomSolver


class Environment:
    def __init__(
        self,
        problem_size: int,
        initialization_type: INIT_LITERAL,
        iteration_limit: int,
        annealing: bool,
        temperature_update: UPDATE_LITERAL,
        temperature_change: float,
        seed: int,
        problem_seed: int,
    ) -> None:
        random.seed(seed)

        self.problem = QAPProblem(problem_size, problem_seed)
        self.solver = RandomSolver(
            initialization_type,
            iteration_limit,
            annealing,
            temperature_update,
            temperature_change,
        )

    def run(self) -> None:
        self.solver.solve(self.problem)
