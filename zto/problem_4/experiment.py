# %%
import pickle as pkl
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from .environment import Environment

# %%

SEEDS = [81178, 34091, 75746, 65927, 1173, 70912, 19419, 50363, 82748, 4511]


class Experiment:
    def __init__(self, name: str, var_name: str, var_values: list, **cont_args) -> None:
        self.var_name = var_name
        self.var_values = var_values
        self.const_args = cont_args
        self.name = name

    def construct_args(self) -> Iterator[dict]:
        for v in self.var_values:
            self.var_value = v
            args = self.const_args | {self.var_name: v}

            yield args


class Lab:
    def __init__(
        self,
        name: str,
        env_cls: type,
        repetitions: int = 10,
        results_dir_path: str = './results',
        **const_args,
    ) -> None:
        self.env_cls = env_cls
        self.experiments: list[Experiment] = []
        self.repetitions = repetitions
        self.const_args = const_args

        self.name = name
        self.results_dir = Path(results_dir_path)
        self.results_dir.mkdir(exist_ok=True)

        self.experiment_runs = self.repetitions * len(SEEDS)

    def _reset_environment(self, **kwargs) -> None:
        self.env: Environment = self.env_cls(**kwargs)

    def add_experiment(self, e: Experiment) -> None:
        self.experiments.append(e)

    def run(self) -> None:
        for i, e in enumerate(self.experiments):
            exp_r = 1
            exp_r_all = self.experiment_runs * len(e.var_values)
            print(f'Running experiment {i + 1}/{len(self.experiments)}:')
            self.results = {
                'var_name': [],
                'var_val': [],
                'time': [],
                'result': [],
                'seed': [],
            }
            for args in e.construct_args():
                for seed in SEEDS:
                    seed_arg = {'seed': seed}
                    for _ in range(self.repetitions):
                        print(
                            f'\r({exp_r:-4}/{exp_r_all:-4})',
                            end='',
                            flush=True,
                        )
                        args = self.const_args | seed_arg | args
                        self._reset_environment(**args)
                        self.env.run()
                        self._add_result(e, seed)
                        exp_r += 1
            print('\rDone')
            self._save_results(e.name)

    def _add_result(self, e: Experiment, seed: int) -> None:
        self.results['var_name'].append(e.var_name)
        self.results['var_val'].append(e.var_value)
        self.results['time'].append(self.env.solver.solution_time)
        self.results['result'].append(self.env.solver.best_solution.value)
        self.results['seed'].append(seed)

    def _save_results(self, name: str) -> None:
        f_name = f'{self.name}_{name}.pkl'

        f_path = self.results_dir / f_name
        with open(f_path, 'wb') as f:
            pkl.dump(self.results, f, pkl.HIGHEST_PROTOCOL)
