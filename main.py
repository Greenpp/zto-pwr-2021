# %%
from zto.problem_6.ABC import ABCSolver
from zto.problem_6.DKP import DKProblem

s = ABCSolver(5, 5)
p = DKProblem(25)

p.visualize()

sol = s.solve(p)
sol.visualize()

# %%
