import random
from functools import total_ordering
from typing import Literal

import numpy as np

from ..RNG import RandomNumberGenerator as RNG

NB_TYPE = Literal['nb', 'gen']


class DKProblem:
    def __init__(self, items: int, nb_type: NB_TYPE = 'nb', rnd_seed: int = 42) -> None:
        self.rgen = RNG(rnd_seed)
        self.items = items
        self.nb_type = nb_type

        # Wartość
        self.c = [self.rgen.nextInt(1, 30) for _ in range(items)]
        # Waga
        self.w = [self.rgen.nextInt(1, 30) for _ in range(items)]
        # Pojemność
        self.b = self.rgen.nextInt(5 * items, 10 * items)

    def evaluate_selection_value(self, selected: set[int]) -> int:
        # Wartość wybranych przedmiotów
        value = sum([self.c[idx] for idx in selected])

        return value

    def evaluate_selection_weight(self, selected: set[int]) -> int:
        # Waga wybranych przedmiotów
        weight = sum([self.w[idx] for idx in selected])

        return weight

    def is_in_bounds(self, weight: int) -> bool:
        # Czy mieści się w torbie
        return weight <= self.b

    def selected_to_solution(self, selected: set[int]) -> 'DKSolution':
        # Tworzy rozwiązanie z ciągu wybranych przedmiotów
        value = self.evaluate_selection_value(selected)
        weight = self.evaluate_selection_weight(selected)
        in_bounds = self.is_in_bounds(weight)

        new_solution = DKSolution(selected, value, weight, in_bounds)

        return new_solution

    def get_not_selected(self, selected: set[int]) -> list[int]:
        # Odwrotność zbioru wybranych przedmiotów
        not_selected = list(filter(lambda it: it not in selected, range(self.items)))

        return not_selected

    def get_full_neighborhood(self, solution: 'DKSolution') -> list['DKSolution']:
        # Podaj wszystkich sąsiadów rozwiązania
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

    def get_next_random(self, solution: 'DKSolution') -> 'DKSolution':
        # Kolejny losowy element dla rozwiązania
        # nb - sąsiad
        # gen - połączenie z losowym (jak genetyczny)
        if self.nb_type == 'nb':
            return self.get_random_neighbor(solution)
        else:
            return self.get_random_gen_neighbour(solution)

    def get_random_gen_neighbour(self, solution: 'DKSolution') -> 'DKSolution':
        # Połączenie z losowym rozwiązaniem
        s2 = self.get_random_solution()
        while solution == s2:
            s2 = self.get_random_solution()

        gen1 = self._selected_to_bin(solution.selected)
        gen2 = self._selected_to_bin(s2.selected)

        ngen = self._combine_bin(gen1, gen2)

        new_selected = self._bin_to_selected(ngen)
        new_solution = self.selected_to_solution(new_selected)

        return new_solution

    def _combine_bin(self, g1: np.ndarray, g2: np.ndarray) -> np.ndarray:
        # Połączenie rozwiązań w postaci binarnej (cięcie na pół)
        cut = self.items // 2

        ng1 = g1[:cut]
        ng2 = g2[cut:]

        ng = np.concatenate([ng1, ng2])
        return ng

    def _selected_to_bin(self, selected: set[int]) -> np.ndarray:
        # Transformacja zbiór przedmiotów -> postać binarna
        bin = np.zeros(self.items)
        selected_idx = np.array(list(selected))

        bin[selected_idx] = 1
        return bin

    def _bin_to_selected(self, bin: np.ndarray) -> set[int]:
        # Transformacja postać binarna -> zbiór przedmiotów
        selected = set(np.where(bin == 1)[0])

        return selected

    def get_random_neighbor(self, solution: 'DKSolution') -> 'DKSolution':
        # Losowy sąsiad danego rozwiązania
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
        # Losowe rozwiązanie
        s_len = random.randint(1, self.items)

        selected = set(random.sample(range(self.items), s_len))
        solution = self.selected_to_solution(selected)
        if not allow_out_of_bounds:
            while not solution.in_bounds:
                s_len = random.randint(1, self.items)
                selected = set(random.sample(range(self.items), s_len))
                solution = self.selected_to_solution(selected)

        return solution

    def visualize(self) -> None:
        print(40 * '=')
        print('Discrete Knapsack Problem')
        print(40 * '=')
        print(f'Bag size: {self.b}')
        print(32 * '-')
        print(f'{"Item":10} {"Value":10} {"Weight":10}')
        print(32 * '-')
        for i in range(self.items):
            print(f'{i:10} {self.c[i]:10} {self.w[i]:10}')


@total_ordering
class DKSolution:
    def __init__(
        self, selected: set[int], value: int, weight: int, in_bounds: bool
    ) -> None:
        self.selected = selected
        self.value = value
        self.weight = weight
        self.in_bounds = in_bounds

    def __eq__(self, other: 'DKSolution') -> bool:
        return self.selected == other.selected

    def __gt__(self, other: 'DKSolution') -> bool:
        if self.in_bounds and other.in_bounds:
            return self.value > other.value
        elif self.in_bounds and not other.in_bounds:
            return True
        elif not self.in_bounds and other.in_bounds:
            return False
        else:
            return self.weight < other.weight

    def visualize(self) -> None:
        print(40 * '=')
        print('Solution')
        print(40 * '=')
        print(f'Total value:  {self.value:10}')
        print(f'Total weight: {self.weight:10}')
        print(40 * '-')
        print('Selected items:')
        print(self.selected)
