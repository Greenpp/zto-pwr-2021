# %%
from timeit import default_timer

from zto.problem_4.jc import PSSP, solvers

# %%
bandb = solvers.BranchAndBound('min', 'none')
bf = solvers.BruteForce('min')
problem = PSSP.PSSPProblem(9, 6)

bbtime = default_timer()
s1 = bandb.optimize(problem)
print(f'B&B: {default_timer() - bbtime}')

bftime = default_timer()
s2 = bf.optimize(problem)
print(f'BF: {default_timer() - bftime}')

# %%
s1.visualize()
# %%
s2.visualize()
# %%
