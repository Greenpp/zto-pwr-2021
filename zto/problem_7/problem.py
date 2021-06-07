import random
from functools import total_ordering
from typing import Optional

import numpy as np
from zto.RNG.RandomNumberGenerator import RandomNumberGenerator as RNG

TOTAL_FLOW = 'total_flow'
MAX_TARD = 'max_tard'
TOTAL_TARD = 'total_tard'
TOTAL_LATE = 'total_late'
MIX = 'mix'


class FlowProblem:
    def __init__(
        self,
        task_num: int,
        criterions: list[str],
        rnd_seed: int = 42,
    ) -> None:
        self.tasks = task_num
        self.machines = 3

        self.criterions = criterions
        self.mixing_coef = self._calculate_mixing_coefs()

        rng = RNG(rnd_seed)
        self.p = np.array(
            [
                [rng.nextInt(1, 99) for _ in range(self.tasks)]
                for _ in range(self.machines)
            ]
        )
        tmp_a = self.p.sum()

        a = tmp_a / 6
        b = tmp_a / 2

        self.d = np.array([rng.nextInt(a, b) for _ in range(self.tasks)])

    def initialize(self) -> 'FlowSolution':
        order = list(range(self.tasks))
        random.shuffle(order)

        return FlowSolution(order, self.criterions)

    def _calculate_mixing_coefs(self) -> tuple[float, float, float]:
        mean_p = (99 - 1 + 1) / 2
        tmp_mean_A = self.machines * self.tasks * mean_p
        mean_B = tmp_mean_A / 2
        mean_A = tmp_mean_A / 6
        mean_d = (mean_B - mean_A + 1) / 2

        times = np.array(
            [self.machines * mean_p + i * mean_p for i in range(self.tasks)]
        )

        mean_total_flow = times.sum()
        mean_max_tard = np.clip(times - mean_d, 0, None).max()
        mean_total_tard = np.clip(times - mean_d, 0, None).sum()

        max_coef = max(mean_total_flow, mean_max_tard, mean_total_tard)

        return (
            mean_total_flow / max_coef,
            mean_max_tard / max_coef,
            mean_total_tard / max_coef,
        )


@total_ordering
class FlowSolution:
    def __init__(
        self,
        order: list[int],
        criterions: list[str],
    ) -> None:
        self.order = order
        self.criterions = criterions

        self.state = {
            TOTAL_FLOW: 0.0,
            MAX_TARD: 0.0,
            TOTAL_TARD: 0.0,
            TOTAL_LATE: 0.0,
            MIX: 0.0,
        }
        self.evalueated = False

    def get_nb(self) -> 'FlowSolution':
        swap_idx1, swap_idx2 = random.sample(range(len(self.order)), 2)
        new_order = self.order.copy()

        new_order[swap_idx1], new_order[swap_idx2] = (
            new_order[swap_idx2],
            new_order[swap_idx1],
        )

        return FlowSolution(new_order, self.criterions)

    def evalueate(self, problem: FlowProblem) -> None:
        if not self.evalueated:
            last_machine_time = [0 for _ in range(problem.tasks)]
            curr_machine_time = [0 for _ in range(problem.tasks)]
            for m in range(problem.machines):
                for t in range(problem.tasks):
                    task_idx = self.order[t]
                    if t == 0:
                        wait_time = last_machine_time[t]
                    else:
                        wait_time = max(last_machine_time[t], curr_machine_time[t - 1])

                    curr_machine_time[t] = wait_time + problem.p[m, task_idx]

                last_machine_time = curr_machine_time

            finish_time = np.array(last_machine_time)
            self.state[TOTAL_FLOW] = finish_time.sum()
            self.state[MAX_TARD] = np.clip((finish_time - problem.d), 0, None).max()
            self.state[TOTAL_TARD] = np.clip((finish_time - problem.d), 0, None).sum()
            self.state[TOTAL_LATE] = (finish_time - problem.d).sum()

            if problem.mixing_coef is not None:
                c1, c2, c3 = problem.mixing_coef
                self.state[MIX] = (
                    c1 * self.state[TOTAL_FLOW]
                    + c2 * self.state[MAX_TARD]
                    + c3 * self.state[TOTAL_TARD]
                )

        self.evalueated = True

    def __gt__(self, other: 'FlowSolution') -> bool:
        for c in self.criterions:
            if self.state[c] < other.state[c]:
                return False
        return True

    # def __eq__(self, other: 'FlowSolution') -> bool:
    #     for c in self.criterions:
    #         if self.state[c] != other.state[c]:
    #             return False
    #     return True
