# %%
from random import seed

from zto.problem_5.QAP import QAPProblem
from zto.problem_5.solver import RandomSolver

p = QAPProblem(25)
seed(42)
solver = RandomSolver(
    annealing=True,
    iteration_limit=100,
    initialization='rnd',
)
s = solver.solve(p)
s.visualize()
# %%
from zto.problem_5.analysis import report

report()

# %%
