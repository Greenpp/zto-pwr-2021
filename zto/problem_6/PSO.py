import numpy as np
from zto.problem_6.sphere_problem import SphereProblem, SphereSolution


class PSOSolver:
    def __init__(
        self,
        population: int,
        learning_rate: float,
        omega: float,
        phi_local: float,
        phi_global: float,
        iteration_limit: int = 1000,
        no_progress_limit: int = -1,
    ) -> None:
        self.population = population
        self.learning_rate = learning_rate
        self.omega = omega
        self.phi_local = phi_local
        self.phi_global = phi_global

        self.iteration_limit = iteration_limit
        self.no_progress_limit = no_progress_limit

    def update_best_solution(self, solution: SphereSolution) -> None:
        if solution < self.best_solution:
            self.best_solution = solution
            self.no_progress = 0

    def should_stop(self) -> bool:
        if self.iteration >= self.iteration_limit:
            return True
        if self.no_progress_limit > -1 and self.no_progress >= self.no_progress_limit:
            return True
        return False

    def solve(self, problem: SphereProblem) -> SphereSolution:
        solutions = [
            PSOSolution(
                problem.get_random_solution(), problem.upper_bound, problem.lower_bound
            )
            for _ in range(self.population)
        ]
        self.best_solution = solutions[0].solution

        for s in solutions:
            self.update_best_solution(s.solution)

        self.iteration = 0
        self.no_progress = 0
        while not self.should_stop():
            self.iteration += 1
            self.no_progress += 1
            for s in solutions:
                rnd_local = np.random.random(problem.vars)
                rnd_global = np.random.random(problem.vars)
                s.update_velocity(
                    self.omega,
                    self.phi_local,
                    rnd_local,
                    self.phi_global,
                    rnd_global,
                    self.best_solution,
                )
                new_solution = s.update_position(self.learning_rate, problem)
                self.update_best_solution(new_solution)

        return self.best_solution


class PSOSolution:
    def __init__(
        self,
        solution: SphereSolution,
        upper_bound: float,
        lower_bound: float,
    ) -> None:
        self.solution = solution
        self.best_local = solution

        u = lower_bound - upper_bound
        l = upper_bound - lower_bound
        self.velocity = np.random.random(len(solution.values)) * (u - l) + l

    def update_velocity(
        self,
        omega: float,
        phi_local: float,
        rnd_local: np.ndarray,
        phi_global: float,
        rnd_global: np.ndarray,
        best_solution: SphereSolution,
    ) -> None:
        self.velocity = (
            self.velocity * omega
            + phi_local * rnd_local * (self.best_local.values - self.solution.values)
            + phi_global * rnd_global * (best_solution.values - self.solution.values)
        )

    def update_position(
        self, learning_rate: float, problem: SphereProblem
    ) -> SphereSolution:
        new_values = self.solution.values + learning_rate * self.velocity
        new_value = problem.evaluate_values(new_values)
        new_solution = SphereSolution(new_values, new_value)

        self.solution = new_solution
        if new_solution < self.best_local:
            self.best_local = new_solution

        return new_solution
