from functools import total_ordering
from random import sample, shuffle

from ..RNG import RandomNumberGenerator


@total_ordering
class QAPSolution:
    def __init__(self, order: list[int], cost: int) -> None:
        self.order = order
        self.cost = cost

    def visualize(self) -> None:
        print('Fac : Loc')
        for i, a in enumerate(self.order):
            print(f'{i:3} : {a:3}')

    def __gt__(self, other: 'QAPSolution') -> bool:
        return self.cost > other.cost

    def __eq__(self, other: 'QAPSolution') -> bool:
        return self.cost == other.cost


class QAPProblem:
    def __init__(self, size: int, rnd_seed: int = 42) -> None:
        rng = RandomNumberGenerator(rnd_seed)
        self.size = size

        self.w = [[rng.nextInt(1, 50) for _ in range(size)] for _ in range(size)]
        self.d = [[rng.nextInt(1, 50) for _ in range(size)] for _ in range(size)]

    def get_random_solution(self) -> QAPSolution:
        order = list(range(self.size))
        shuffle(order)

        cost = self._evaluate_order(order)

        return QAPSolution(order, cost)

    def get_random_neighbor(self, solution: QAPSolution) -> QAPSolution:
        order = solution.order.copy()

        idx_a, idx_b = sample(list(range(self.size)), 2)
        order[idx_a], order[idx_b] = order[idx_b], order[idx_a]

        cost = self._evaluate_order(order)

        return QAPSolution(order, cost)

    def _evaluate_order(self, order: list[int]) -> int:
        total_cost = 0
        for fi, pi in enumerate(order):
            for fj, pj in enumerate(order):
                total_cost += self.w[fi][fj] * self.d[pi][pj]

        return total_cost
