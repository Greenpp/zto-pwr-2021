from typing import Optional

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

    def expand(self, solution: Optional['PSSPSolution']) -> list['PSSPSolution']:
        if solution is None:
            tasks_left = [i for i in range(self.tasks)]
            sequence = []
            time = [0 for _ in range(self.machines)]
        else:
            tasks_left = solution.tasks_left
            sequence = solution.tasks_sequence
            time = solution.work_time

        new_solutions = []
        for task in tasks_left:
            new_machines_left = tasks_left.copy()
            new_machines_left.remove(task)

            new_sequence = sequence.copy()
            new_sequence.append(task)

            new_time = time.copy()
            prev_machine_time = 0
            for machine, t in enumerate(new_time):
                new_time[machine] += (
                    max(prev_machine_time, t) + self.cost[task][machine]
                )
                prev_machine_time = new_time[machine]

            new_solution = PSSPSolution(new_sequence, new_machines_left, new_time)
            new_solutions.append(new_solution)

    def get_rand_solution(self) -> Solution:
        pass

    def get_greedy_solution(self) -> Solution:
        pass

    def get_dfs_solution(self) -> Solution:
        pass


class PSSPSolution(Solution):
    def __init__(
        self,
        task_sequence: list[int],
        tasks_left: list[int],
        work_time: list[int],
    ) -> None:
        super().__init__(work_time[-1], is_final=not tasks_left)

        self.tasks_sequence = task_sequence
        self.tasks_left = tasks_left
        self.work_time = work_time
