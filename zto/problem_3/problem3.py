# %%
import numpy as np
from docplex.mp.model import Model
from matplotlib import pyplot as plt

from ..RNG import RandomNumberGenerator as RNG

# %%
n = 25
m = Model(name='Zagadnienie przydziału')

gen = RNG(42)
k = [[gen.nextInt(1, 50) for _ in range(n)] for _ in range(n)]
x = [[m.binary_var(name=f'x_{i}_{j}') for j in range(n)] for i in range(n)]

m.minimize(m.sum(x[i][j] * k[i][j] for j in range(n) for i in range(n)))
for i in range(n):
    m.add_constraint(m.sum(x[i]) == 1)
    m.add_constraint(m.sum(x[j][i] for j in range(n)) == 1)

s = m.solve(log_output=True)
vals = s.as_df().set_index('name').to_dict()['value']

mat = np.zeros((n, n))
for n, v in vals.items():
    _, x, y = n.split('_')
    mat[int(x)][int(y)] = 1
# %%
s.display()
plt.axis('off')
plt.imshow(mat)

# %%
