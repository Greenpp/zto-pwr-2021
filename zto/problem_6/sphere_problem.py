from functools import total_ordering

import numpy as np


class SphereProblem:
    def __init__(
        self, vars: int, upper_bound: float = 100, lowe_bound: float = -100
    ) -> None:
        self.vars = vars
        self.upper_bound = upper_bound
        self.lower_bound = lowe_bound

    def get_random_solution(self) -> 'SphereSolution':
        values = (
            np.random.random(self.vars) * (self.upper_bound - self.lower_bound)
            + self.lower_bound
        )
        value = self.evaluate_values(values)

        solution = SphereSolution(values, value)
        return solution

    def evaluate_values(self, values: np.ndarray) -> float:
        value = (values ** 2).sum()

        return value

    def visualize(self) -> None:
        print(40 * '=')
        print('Sphere function')
        print(40 * '=')
        print(f'Variables: {self.vars}')


@total_ordering
class SphereSolution:
    def __init__(self, values: np.ndarray, value: float) -> None:
        self.values = values
        self.value = value

    def __gt__(self, other: 'SphereSolution') -> bool:
        return self.value > other.value

    def visualize(self) -> None:
        print(40 * '=')
        print('Solution')
        print(40 * '=')
        print(f'Result: {self.value}')
        print(f'Values: {self.values}')
