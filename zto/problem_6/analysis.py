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
