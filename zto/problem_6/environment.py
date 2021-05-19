import random

from zto.problem_6.ABC import ABCSolver
from zto.problem_6.DKP import NB_TYPE, DKProblem


class ABCEnvironment:
    def __init__(
        self,
        items: int,
        nb_type: NB_TYPE,
        population: int,
        change_limit: int,
        iteration_limit: int,
        no_progress_limit: int,
        seed: int,
        problem_seed: int,
    ) -> None:
        random.seed(seed)

        self.problem = DKProblem(items, nb_type, problem_seed)
        self.solver = ABCSolver(
            population, change_limit, iteration_limit, no_progress_limit
        )

    def run(self) -> None:
        self.solver.solve(self.problem)
