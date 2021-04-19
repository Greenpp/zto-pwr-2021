from .environment import P4Environment
from .experiment import Experiment, Lab


def run_lab():
    lab = Lab(
        name='p4',
        env_cls=P4Environment,
        method='bb',
        init_typ='none',
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

    lab.run()
