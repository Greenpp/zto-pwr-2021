# %%
import pickle as pkl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
from zto.problem_6.environment import ABCEnvironment
from zto.problem_6.experiment import Experiment, Lab

SEEDS = [81178, 34091, 75746, 65927, 1173, 70912, 19419, 50363, 82748, 4511]

# %%
def run_lab():
    lab = Lab(
        name='p6abc',
        repetitions=1,
        env_cls=ABCEnvironment,
        seeds=SEEDS,
        items=50,
        nb_type='nb',
        population=10,
        change_limit=5,
        iteration_limit=1000,
        no_progress_limit=-1,
        problem_seed=42,
    )

    e1 = Experiment(
        name='nb_nb',
        var_name='problem_seed',
        var_values=[42, 252, 3636, 95092, 22],
    )
    lab.add_experiment(e1)

    e2 = Experiment(
        name='nb_gen',
        var_name='problem_seed',
        var_values=[42, 252, 3636, 95092, 22],
        nb_type='gen',
    )
    lab.add_experiment(e2)

    lab.run()


# %%
def _process(x: pd.DataFrame) -> np.ndarray:
    seed_g_x = x.groupby(['var_val'], as_index=False).agg(
        lambda xdf: (
            np.vstack([np.array(r['results']) for _, r in xdf.iterrows()]).mean(axis=0),
        )
    )
    y = np.vstack([r['results'] for _, r in seed_g_x.iterrows()]).mean(axis=0)

    return y


def report():
    files = [
        './results/p6abc_nb_gen.pkl',
        './results/p6abc_nb_gen.pkl',
    ]

    data = []
    for name in files:
        with open(name, 'rb') as f:
            d = pkl.load(f)
            data.append(d)
    dfs = [pd.DataFrame(d) for d in data]

    x1 = dfs[0][['var_val', 'results']]
    x2 = dfs[1][['var_val', 'results']]

    y1 = _process(x1)
    y2 = _process(x2)

    plt.plot(y1, alpha=0.5, label='sąsiad')
    plt.plot(y2, alpha=0.5, label='genetyczny')
    plt.xlabel('iteracja')
    plt.ylabel('wartość')
    plt.legend()
    plt.title('Optymalizacja w zależności od typu doboru kolejnego rozwiązania')
    plt.show()
