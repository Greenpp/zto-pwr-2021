import pickle as pkl

import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

from .environment import P4Environment
from .experiment import Experiment, Lab

SEEDS = [81178, 34091, 75746, 65927, 1173, 70912, 19419, 50363, 82748, 4511]


def run_lab():
    lab = Lab(
        name='p4',
        env_cls=P4Environment,
        seeds=SEEDS,
        method='bb',
        init_type='none',
        enqueue_limit=-1,
        tasks=9,
        machines=9,
    )

    e1 = Experiment(
        name='bb_init_type',
        var_name='init_type',
        var_values=['none', 'rand', 'greedy', 'dfs'],
    )
    lab.add_experiment(e1)

    e2 = Experiment(
        name='bb_enq_lim',
        var_name='enqueue_limit',
        var_values=list(range(1, 10)),
    )
    lab.add_experiment(e2)

    e3 = Experiment(
        name='bf',
        var_name='method',
        var_values=['bf'],
    )
    lab.add_experiment(e3)

    e4 = Experiment(
        name='bb_enq_lim_init',
        var_name='enqueue_limit',
        var_values=list(range(1, 10)),
        init_type='greedy',
    )
    lab.add_experiment(e4)

    e5 = Experiment(
        name='bb_tasks_num',
        var_name='tasks',
        var_values=[2, 3, 4, 5, 6, 7, 8, 9],
    )
    lab.add_experiment(e5)

    lab.run()


def report() -> None:
    files = [
        './results/p4_bb_enq_lim.pkl',
        './results/p4_bb_enq_lim_init.pkl',
        './results/p4_bb_init_type.pkl',
        './results/p4_bf.pkl',
        './results/p4_bb_tasks_num.pkl',
    ]

    data = []
    for name in files:
        with open(name, 'rb') as f:
            d = pkl.load(f)
            data.append(d)
    dfs = [pd.DataFrame(d) for d in data]

    dfs[2]['var_val'] = dfs[2]['var_val'].replace(
        {
            'none': 'Brak',
            'rand': 'Losowa',
            'dfs': 'DFS',
            'greedy': 'Greedy',
        }
    )

    bb_dfs = dfs[2][dfs[2]['var_val'] == 'DFS']
    bb_data = bb_dfs.assign(var_val='Branch&Bound')
    bf_data = dfs[3].assign(var_val='BruteForce')
    dfs[3] = pd.concat((bb_data, bf_data))

    error0 = (
        dfs[0][['var_val', 'result']]
        .groupby(['var_val', 'result'], as_index=False)
        .last()
        .rename(columns={'var_val': 'wartość', 'result': 'błąd [%]'})
        .set_index('wartość')
    )
    r_val = error0.iloc[-1].values
    error0 -= r_val
    error0 /= r_val
    error0 *= 100

    error1 = (
        dfs[1][['var_val', 'result']]
        .groupby(['var_val', 'result'], as_index=False)
        .last()
        .rename(columns={'var_val': 'wartość', 'result': 'błąd [%]'})
        .set_index('wartość')
    )
    r_val = error1.iloc[-1].values
    error1 -= r_val
    error1 /= r_val
    error1 *= 100

    td, tm = _get_time_data(dfs[0])
    _plot_data(
        td,
        'Wpływ limitu kolejkowania na szybkość optymalizacji (bez inicjalizacji)',
        'Limit kolejkowania',
        'Czas [s]',
    )
    _print_table(tm.round(4), floatfmt='.4f')
    _plot_error(error0)
    _print_table(error0.round(2), floatfmt='.2f')

    td, tm = _get_time_data(dfs[1])
    _plot_data(
        td,
        'Wpływ limitu kolejkowania na szybkość optymalizacji (inicjalizacja greedy)',
        'Limit kolejkowania',
        'Czas [s]',
    )
    _print_table(tm.round(4), floatfmt='.4f')
    _plot_error(error1)
    _print_table(error1.round(2), floatfmt='.2f')

    td, tm = _get_time_data(dfs[2])
    _plot_data(
        td,
        'Wpływ inicjalizacji na szybkość optymalizacji',
        'Rodzaj inicjalizacji',
        'Czas [s]',
    )
    _print_table(tm.iloc[[0, 3, 1, 2]])

    td, tm = _get_time_data(dfs[3])
    _plot_data(
        td,
        'Wpływ algorytmu na szybkość optymalizacji',
        'Algorytm',
        'Czas [s]',
    )
    _print_table(tm)

    td, tm = _get_time_data(dfs[4])
    _plot_data(
        td,
        'Wpływ wielkości problemu na szybkość optymalizacji',
        'Wielkość',
        'Czas [s]',
    )
    _print_table(tm.round(6), floatfmt='.6f')


def _get_time_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    seed_mean = df.groupby(['var_name', 'var_val', 'seed']).mean().reset_index()
    time_data = seed_mean.rename(columns={'time': 'y'})[['var_val', 'y']]
    time_mean = (
        seed_mean[['var_val', 'time']]
        .groupby('var_val')
        .mean()
        .rename(
            columns={
                'time': 'średni czas [s]',
            },
        )
        .rename_axis('wartość')
    )

    return time_data, time_mean


def _plot_data(data: pd.DataFrame, title: str, lx: str, ly: str, **kwargs) -> None:
    data.set_index(['var_val'])[['y']].boxplot(by='var_val', **kwargs)
    plt.suptitle('')
    plt.title(title)
    plt.xlabel(lx)
    plt.ylabel(ly)
    plt.gcf().set_size_inches(12, 8)
    plt.show()


def _plot_error(data: pd.DataFrame) -> None:
    data.plot(kind='bar', legend=False)
    plt.title('Wielkość błędu w zależności od limitu kolejkowania')
    plt.xlabel('Limit kolejkowania')
    plt.ylabel('Błąd [%]')
    plt.gcf().set_size_inches(12, 8)
    plt.show()


def _print_table(data: pd.DataFrame, **kwargs) -> None:
    print(tabulate(data, 'keys', 'github', **kwargs))
