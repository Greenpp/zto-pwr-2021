# %%
from zto.problem_6.ABC import ABCSolver
from zto.problem_6.DKP import DKProblem

s = ABCSolver(5, 5)
p = DKProblem(25)

p.visualize()

sol = s.solve(p)
sol.visualize()

# %%
from zto.problem_6.sphere_problem import SphereProblem
from zto.problem_6.PSO import PSOSolver

s = PSOSolver(100, 0.1, 0.5, 0.5, 0.5, 1000, 100)
p = SphereProblem(5)

p.visualize()

sol = s.solve(p)
sol.visualize()
# %%
