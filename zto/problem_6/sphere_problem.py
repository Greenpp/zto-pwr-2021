from functools import total_ordering

import numpy as np


class SphereProblem:
    def __init__(self, vars: int) -> None:
        self.vars = vars

    def get_random_solution(self) -> 'SphereSolution':
        values = np.random.random(self.vars) * 200 - 100
        value = self.evaluate_values(values)

        solution = SphereSolution(values, value)
        return solution

    def evaluate_values(self, values: np.ndarray) -> float:
        value = (values ** 2).sum()

        return value


@total_ordering
class SphereSolution:
    def __init__(self, values: np.ndarray, value: float) -> None:
        self.values = values
        self.value = value

    def __gt__(self, other: 'SphereSolution') -> bool:
        return self.value > other.value
