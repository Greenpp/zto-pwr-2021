from random import shuffle
from typing import Optional

from ...RNG import RandomNumberGenerator
from .solvers import Problem, Solution


class PSSPProblem(Problem):
    def __init__(self, tasks: int, machines: int, rng_seed: int = 42) -> None:
        self.tasks = tasks
        self.machines = machines

        rng = RandomNumberGenerator(rng_seed)
        self.cost = [
            [rng.nextInt(1, 99) for _ in range(machines)] for _ in range(tasks)
        ]

    def expand(self, solution: Optional['PSSPSolution'] = None) -> list['PSSPSolution']:
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
            new_tasks_left = tasks_left.copy()
            new_tasks_left.remove(task)

            new_sequence = sequence.copy()
            new_sequence.append(task)

            new_time = time.copy()
            prev_machine_time = 0
            for machine, t in enumerate(new_time):
                new_time[machine] = max(prev_machine_time, t) + self.cost[task][machine]
                prev_machine_time = new_time[machine]
            estimated_cost = sum([self.cost[t][-1] for t in new_tasks_left])

            new_solution = PSSPSolution(
                new_sequence, new_tasks_left, new_time, estimated_cost
            )
            new_solutions.append(new_solution)

        return new_solutions

    def get_rand_solution(self) -> Solution:
        sequence = list(range(self.tasks))
        shuffle(sequence)

        solution = PSSPSolution([], [], [0 for _ in range(self.machines)], 0)
        for task in sequence:
            solution.tasks_left.append(task)
            solution = self.expand(solution)[0]

        return solution

    def get_greedy_solution(self) -> Solution:
        # TODO
        return PSSPSolution([], [], [], 0)

    def get_dfs_solution(self) -> Solution:
        # TODO
        return PSSPSolution([], [], [], 0)


class PSSPSolution(Solution):
    def __init__(
        self,
        task_sequence: list[int],
        tasks_left: list[int],
        work_time: list[int],
        estimated_cost: int,
    ) -> None:
        super().__init__(work_time[-1] + estimated_cost, is_final=not tasks_left)

        self.tasks_sequence = task_sequence
        self.tasks_left = tasks_left
        self.work_time = work_time

    def visualize(self) -> None:
        print(f'Task sequence: {self.tasks_sequence}')
        print(f'Final time: {self.work_time[-1]}')
