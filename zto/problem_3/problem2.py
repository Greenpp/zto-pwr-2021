# %%
import io

from docplex.mp.model import Model
from matplotlib import pyplot as plt

from ..RNG import RandomNumberGenerator as RNG


# %%
class Problem2:
    def __init__(self, n: int, seed: int = 42) -> None:
        self.n = n

        gen = RNG(seed)

        self.a = [gen.nextFloat(5, 35) for _ in range(n)]
        self.b = [gen.nextFloat(5, 35) for _ in range(n)]
        self.r = [gen.nextFloat(1, 7) for _ in range(n)]

        self.f = [
            [0 if i == j else gen.nextFloat(1, 20) for j in range(n)] for i in range(n)
        ]

        self.m = Model(name='Kwadratowe zagadnienie przydzialu')

    def setup(self) -> None:
        self.x = [
            [self.m.continuous_var(name=f'x{i}'), self.m.continuous_var(name=f'y{i}')]
            for i in range(self.n)
        ]

        self.m.minimize(
            self.m.sum(
                self.f[i][j]
                * (
                    self.m.abs(self.x[i][0] - self.x[j][0])
                    + self.m.abs(self.x[i][1] - self.x[j][1])
                )
                for i in range(self.n)
                for j in range(self.n)
            )
        )

        for i in range(self.n):
            self.m.add_constraint(
                (
                    self.m.abs(self.x[i][0] - self.a[i])
                    + self.m.abs(self.x[i][1] - self.b[i])
                    <= self.r[i]
                )
            )

    def solve(self) -> None:
        out_stream = io.StringIO()
        self.solution = self.m.solve(log_output=out_stream)

        self.ex_time = float(out_stream.getvalue().splitlines()[-1].split()[-4])
        self.values = (
            self.solution.as_df().head(20).set_index('name').to_dict()['value']
        )

    def visualize(self) -> None:
        fig, ax = plt.subplots()

        circles = [
            plt.Circle((self.a[i], self.b[i]), self.r[i], fill=False)
            for i in range(self.n)
        ]
        p_x, p_y = zip(
            *[(self.values[f'x{i}'], self.values[f'y{i}']) for i in range(self.n)]
        )

        ax.set_aspect(1)
        ax.set(xlim=(-10, 50), ylim=(-10, 50))
        fig.set_size_inches(10, 10)
        plt.axis('off')

        ax.scatter(p_x, p_y, c='r')
        for c in circles:
            ax.add_artist(c)
        for i in range(self.n):
            ax.annotate(
                f'Z{i+1}',
                (self.values[f'x{i}'], self.values[f'y{i}']),
                size=12,
                weight='bold',
            )
        plt.show()


# %%
p = Problem2(10)

p.setup()
p.solve()
p.visualize()
# %%
