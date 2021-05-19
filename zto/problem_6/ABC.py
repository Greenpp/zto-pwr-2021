import random

from .DKP import DKProblem, DKSolution


class ABCSolver:
    def __init__(
        self,
        population: int,
        change_limit: int,
        iteration_limit: int = 1000,
        no_progress_limit: int = -1,
    ) -> None:
        self.population = population
        self.change_limit = change_limit
        self.iteration_limit = iteration_limit
        self.no_progress_limit = no_progress_limit

        self.best_history = []

    def update_best(self, solution: DKSolution) -> None:
        # Aktualizacja najlepszego rozwiązania (w razie potrzeby)
        if solution > self.best_solution:
            self.best_solution = solution

    def log_best(self) -> None:
        self.best_history.append(self.best_solution.value)

    def should_stop(self) -> bool:
        # Warunek stopu
        if self.iteration_limit <= self.iteration:
            return True
        if self.no_progress_limit > 0 and self.no_progress_limit <= self.no_progress:
            return True
        return False

    def try_solution_neighbor(
        self, problem: DKProblem, solution: 'ABCSolution'
    ) -> None:
        # Sprawdzenie kolejnego rozwiązania dla podanego
        nb_solution = problem.get_next_random(solution.solution)
        if nb_solution > solution.solution:
            solution.replace_solution(nb_solution)
            self.no_progress = 0
            self.update_best(nb_solution)
        else:
            solution.fail()

    def solve(self, problem: DKProblem) -> DKSolution:
        solutions = [
            ABCSolution(problem.get_random_solution()) for _ in range(self.population)
        ]

        self.iteration = 0
        self.no_progress = 0

        self.best_solution = solutions[0].solution
        for s in solutions:
            self.update_best(s.solution)
        while not self.should_stop():
            self.iteration += 1
            self.no_progress = +1
            # Zbieracze
            # Sprawdzanie kolejnych rozwiązań
            for s in solutions:
                self.try_solution_neighbor(problem, s)

            # Obserwatorzy
            # Sprawdzanie kolejnych rozwiązań z naciskiem na najlepsze
            for i in range(self.population):
                exp_solution = random.sample(
                    solutions, 1, counts=[s.solution.value for s in solutions]
                )[0]
                self.try_solution_neighbor(problem, exp_solution)

            # Zwiadowcy
            # Podmiana rozwiązań bez możliwości poprawy
            for s in solutions:
                if s.c > self.change_limit:
                    new_solution = problem.get_random_solution()
                    s.replace_solution(new_solution)
                    self.no_progress = 0
                    self.update_best(new_solution)

            self.log_best()

        return self.best_solution


class ABCSolution:
    def __init__(self, solution: DKSolution) -> None:
        self.replace_solution(solution)

    def replace_solution(self, solution: DKSolution) -> None:
        self.solution = solution
        self.c = 0

    def fail(self) -> None:
        self.c += 1
