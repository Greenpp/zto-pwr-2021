import random

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

    def evaluate_selection_value(self, selected: list[int]) -> int:
        value = sum([self.c[idx] for idx in selected])

        return value

    def evaluate_selection_boundary(self, selected: list[int]) -> bool:
        weight = sum([self.w[idx] for idx in selected])

        return weight <= self.b

    def get_full_neighborhood(self, solution: 'DKSolution') -> list['DKSolution']:
        not_selected = list(
            filter(lambda it: it not in solution.selected, range(self.items))
        )

        nb_solutions = []
        for i in range(len(solution.selected)):
            for n_it in not_selected:
                new_selected = solution.selected.copy()
                new_selected[i] = n_it

                new_value = self.evaluate_selection_value(new_selected)
                new_in_bounds = self.evaluate_selection_boundary(new_selected)

                new_solution = DKSolution(new_selected, new_value, new_in_bounds)
                nb_solutions.append(new_solution)
        for n_it in not_selected:
            new_selected = solution.selected.copy()
            new_selected.append(n_it)

            new_value = self.evaluate_selection_value(new_selected)
            new_in_bounds = self.evaluate_selection_boundary(new_selected)

            new_solution = DKSolution(new_selected, new_value, new_in_bounds)
            nb_solutions.append(new_solution)

        return nb_solutions

    def get_random_neighbor(self, solution: 'DKSolution') -> 'DKSolution':
        not_selected = list(
            filter(lambda it: it not in solution.selected, range(self.items))
        )

        new_item = random.choice(not_selected)
        replace_idx = random.randint(0, len(solution.selected))

        new_selected = solution.selected.copy()
        if replace_idx == len(new_selected):
            new_selected.append(new_item)
        else:
            new_selected[replace_idx] = new_item

        new_value = self.evaluate_selection_value(new_selected)
        new_in_bounds = self.evaluate_selection_boundary(new_selected)

        new_solution = DKSolution(new_selected, new_value, new_in_bounds)

        return new_solution


class DKSolution:
    def __init__(self, selected: list[int], value: int, in_bounds: bool) -> None:
        self.selected = selected
        self.value = value
        self.in_bounds = in_bounds
