from ...RNG import RandomNumberGenerator
from .bandb import Problem, Solution


class PSSPProblem(Problem):
    def __init__(self, tasks: int, machines: int, rng_seed: int = 42) -> None:
        self.tasks = tasks
        self.machines = machines

        rng = RandomNumberGenerator(rng_seed)
        self.cost = [
            [rng.nextInt(1, 99) for _ in range(machines)] for _ in range(tasks)
        ]

    def get_level_max(self, level: int):
        raise Exception('It is a minimization problem')

    def get_level_min(self, level: int):
        pass


class PSSPSolution(Solution):
    pass
