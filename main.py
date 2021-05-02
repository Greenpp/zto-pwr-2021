# %%
from random import seed

from zto.problem_5.QAP import QAPProblem
from zto.problem_5.solver import RandomSolver

p = QAPProblem(10)
seed(42)
solver = RandomSolver(annealing=True, iteration_limit=1000)
s = solver.solve(p)
s.visualize()
# %%
