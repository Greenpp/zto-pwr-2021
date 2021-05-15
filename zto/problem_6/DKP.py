import random
from functools import total_ordering

from ..RNG import RandomNumberGenerator as RNG


class DKProblem:
    def __init__(self, items: int, rnd_seed: int = 42) -> None:
        self.rgen = RNG(rnd_seed)
        self.items = items

        # Wartość
        self.c = [self.rgen.nextInt(1, 30) for _ in range(items)]
        # Waga
        self.w = [self.rgen.nextInt(1, 30) for _ in range(items)]
        # Pojemność
        self.b = self.rgen.nextInt(5 * items, 10 * items)

    def evaluate_selection_value(self, selected: set[int]) -> int:
        value = sum([self.c[idx] for idx in selected])

        return value

    def evaluate_selection_weight(self, selected: set[int]) -> int:
        weight = sum([self.w[idx] for idx in selected])

        return weight

    def is_in_bounds(self, weight: int) -> bool:
        return weight <= self.b

    def selected_to_solution(self, selected: set[int]) -> 'DKSolution':
        value = self.evaluate_selection_value(selected)
        weight = self.evaluate_selection_weight(selected)
        in_bounds = self.is_in_bounds(weight)

        new_solution = DKSolution(selected, value, weight, in_bounds)

        return new_solution

    def get_not_selected(self, selected: set[int]) -> list[int]:
        not_selected = list(filter(lambda it: it not in selected, range(self.items)))

        return not_selected

    def get_full_neighborhood(self, solution: 'DKSolution') -> list['DKSolution']:
        not_selected = self.get_not_selected(solution.selected)

        nb_solutions = []
        for it in solution.selected:
            for n_it in not_selected:
                new_selected = solution.selected.copy()
                new_selected.remove(it)
                new_selected.add(n_it)

                new_solution = self.selected_to_solution(new_selected)
                nb_solutions.append(new_solution)
        for n_it in not_selected:
            new_selected = solution.selected.copy()
            new_selected.add(n_it)

            new_solution = self.selected_to_solution(new_selected)
            nb_solutions.append(new_solution)

        return nb_solutions

    def get_random_neighbor(self, solution: 'DKSolution') -> 'DKSolution':
        not_selected = self.get_not_selected(solution.selected)

        new_item = random.choice(not_selected)
        replace_it = random.choice(list(solution.selected | {None}))

        new_selected = solution.selected.copy()
        if replace_it is not None:
            new_selected.remove(replace_it)

        new_selected.add(new_item)

        new_solution = self.selected_to_solution(new_selected)

        return new_solution

    def get_random_solution(self, allow_out_of_bounds: bool = False) -> 'DKSolution':
        s_len = random.randint(1, self.items)

        selected = set(random.sample(range(self.items), s_len))
        solution = self.selected_to_solution(selected)
        if not allow_out_of_bounds:
            while not solution.in_bounds:
                s_len = random.randint(1, self.items)
                selected = set(random.sample(range(self.items), s_len))
                solution = self.selected_to_solution(selected)

        return solution


@total_ordering
class DKSolution:
    def __init__(
        self, selected: set[int], value: int, weight: int, in_bounds: bool
    ) -> None:
        self.selected = selected
        self.value = value
        self.weight = weight
        self.in_bounds = in_bounds

    def __gt__(self, other: 'DKSolution') -> bool:
        if self.in_bounds and other.in_bounds:
            return self.value > other.value
        elif self.in_bounds and not other.in_bounds:
            return True
        elif not self.in_bounds and other.in_bounds:
            return False
        else:
            return self.weight < other.weight
