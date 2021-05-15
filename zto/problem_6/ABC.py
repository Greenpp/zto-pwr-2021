import random

from .DKP import DKProblem, DKSolution


class ABCSolver:
    def __init__(self, population: int, change_limit: int) -> None:
        self.population = population
        self.change_limit = change_limit

    def update_best(self, solution: DKSolution) -> None:
        if solution > self.best_solution:
            self.best_solution = solution

    def should_stop(self) -> bool:
        return self.iteration > 100

    def try_solution_neighbor(
        self, problem: DKProblem, solution: 'ABCSolution'
    ) -> None:
        nb_solution = problem.get_random_neighbor(solution.solution)
        if nb_solution > solution.solution:
            solution.replace_solution(nb_solution)
            self.update_best(nb_solution)
        else:
            solution.fail()

    def solve(self, problem: DKProblem) -> DKSolution:
        solutions = [
            ABCSolution(problem.get_random_solution()) for _ in range(self.population)
        ]

        self.iteration = 0

        self.best_solution = solutions[0].solution
        for s in solutions:
            self.update_best(s.solution)
        while not self.should_stop():
            self.iteration += 1
            print(f'Iteration: {self.iteration}')
            # Zbieracze
            for s in solutions:
                self.try_solution_neighbor(problem, s)

            # Obserwatorzy
            for i in range(self.population):
                exp_solution = random.sample(
                    solutions, 1, counts=[s.solution.value for s in solutions]
                )[0]
                self.try_solution_neighbor(problem, exp_solution)

            # Zwiadowcy
            for s in solutions:
                if s.c > self.change_limit:
                    new_solution = problem.get_random_solution()
                    s.replace_solution(new_solution)
                    self.update_best(new_solution)

        return self.best_solution


class ABCSolution:
    def __init__(self, solution: DKSolution) -> None:
        self.replace_solution(solution)

    def replace_solution(self, solution: DKSolution) -> None:
        self.solution = solution
        self.c = 0

    def fail(self) -> None:
        self.c += 1
