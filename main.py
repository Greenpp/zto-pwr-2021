# %%
from random import seed

from zto.problem_6.ABC import ABCSolver
from zto.problem_6.DKP import DKProblem

seed(42)

s = ABCSolver(5, 5)
p = DKProblem(50, 'gen')

p.visualize()

sol = s.solve(p)
sol.visualize()


# %%
from random import seed

from zto.problem_6.PSO import PSOSolver
from zto.problem_6.sphere_problem import SphereProblem

seed(42)

s = PSOSolver(100, 0.1, 0.5, 0.5, 0.5, 1000, 100)
p = SphereProblem(5)

p.visualize()

sol = s.solve(p)
sol.visualize()
# %%
