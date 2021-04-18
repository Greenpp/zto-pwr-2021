# %%
from zto.problem_4.jc import PSSP, solvers

# %%
bandb = solvers.BranchAndBound('min', 'dfs')
bf = solvers.BruteForce('min')
problem = PSSP.PSSPProblem(8, 4)

bandb.solve(problem)
bf.solve(problem)

bandb.report()
bf.report()
# %%
