# %%
import pickle as pkl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate

# %%
from .environment import Environment
from .experiment import Experiment, Lab

SEEDS = [81178, 34091, 75746, 65927, 1173, 70912, 19419, 50363, 82748, 4511]
# %%


def run_lab():
    lab = Lab(
        name='p5',
        env_cls=Environment,
        seeds=SEEDS,
        problem_size=25,
        initialization_type='rnd',
        iteration_limit=1000,
        annealing=True,
        temperature_update='geo',
        temperature_change=0.99,
        problem_seed=42,
    )

    e1 = Experiment(
        name='geo',
        var_name='temperature_change',
        var_values=[0.5, 0.95, 0.97, 0.99, 0.999, 0.9999],
    )
    lab.add_experiment(e1)

    e2 = Experiment(
        name='lin',
        var_name='temperature_change',
        var_values=[1, 10, 100, 1000, 10000, 100000],
    )
    lab.add_experiment(e2)

    e3 = Experiment(
        name='rnd',
        var_name='annealing',
        var_values=[False],
    )
    lab.add_experiment(e3)

    e4 = Experiment(
        name='rnd_inits',
        var_name='initialization_type',
        var_values=['rnd', 'best', 'greedy'],
        annealing=False,
    )
    lab.add_experiment(e4)

    e5 = Experiment(
        name='sa_inits',
        var_name='initialization_type',
        var_values=['rnd', 'best', 'greedy'],
    )
    lab.add_experiment(e5)

    lab.run()


def report():
    files = [
        './results/p5_geo.pkl',
        './results/p5_lin.pkl',
        './results/p5_rnd_inits.pkl',
        './results/p5_rnd.pkl',
        './results/p5_sa_inits.pkl',
    ]
    data = []
    for name in files:
        with open(name, 'rb') as f:
            d = pkl.load(f)
            data.append(d)
    dfs = [pd.DataFrame(d) for d in data]

    r0 = _process_results(dfs[0])
    r0b = r0[r0['var_val'] == 0.99]
    _plot_results(r0, 'Współczynnik wyżarzania geometrycznego')
    _show_final_results(r0)

    r1 = _process_results(dfs[1])
    r1b = r1[r1['var_val'] == 10000]
    _plot_results(r1, 'Współczynnik wyżarzania liniowego')
    _show_final_results(r1)

    r2 = _process_results(dfs[2])
    _plot_results(r2, 'Inicjalizacja dla przeszukania losowego')
    _show_final_results(r2)

    r3 = _process_results(dfs[3])
    r3 = r3.append(r0b).append(r1b)

    r3['var_val'] = r3['var_val'].replace({0.99: 'geo', 10000: 'lin', 0: 'rnd'})

    _plot_results(r3, 'Porównanie wyżarzania z przeszukaniem losowym')
    _show_final_results(r3)

    r4 = _process_results(dfs[4])
    _plot_results(r4, 'Inicjalizacja dla wyżarzania')
    _show_final_results(r4)


def _list_mean_agg(series):
    results = []
    for result in series:
        results.append(np.array(result))
    results = np.vstack(results).mean(axis=0)
    return results.tolist()


def _process_results(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=['var_name', 'time'])

    df = df.groupby(['var_val', 'seed'], as_index=False).agg(_list_mean_agg)
    df = (
        df.drop(columns=['seed']).groupby('var_val', as_index=False).agg(_list_mean_agg)
    )

    return df


def _show_final_results(df: pd.DataFrame) -> None:
    df['results'] = df['results'].apply(lambda r: r[-1])
    df = df.set_index('var_val').sort_values('results', ascending=False)
    print(tabulate(df, 'keys', 'github'))


def _plot_results(df: pd.DataFrame, title: str, legend: bool = True) -> None:
    for _, r in df.iterrows():
        l = str(r['var_val'])
        y = r['results']

        if len(y) == 1:
            plt.hlines(y, 0, 1, label=l, colors='g')
        else:
            plt.plot(y, label=l)
    if legend:
        plt.legend()
    plt.gcf().set_size_inches(12, 8)
    plt.title(title)
    plt.show()
