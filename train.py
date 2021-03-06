import os
from spinup import ppo, ddpg, trpo, td3, sac
from spinup.utils.mpi_tools import mpi_fork
import tensorflow as tf
from envs.sawyer_env import SawyerReachEnv, SawyerGraspEnv

PATH = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = os.path.join(PATH, 'results')
EXP_NAME = 'sawyer'


def train(alg, task):
    if task == 'reach':
        env_fn = lambda: SawyerReachEnv(n_substeps=25, reward_type='dense')
    elif task == 'grasp':
        env_fn = lambda: SawyerGraspEnv(n_substeps=5, reward_type='dense')

    ac_kwargs = dict(hidden_sizes=[64, 64], activation=tf.nn.relu)
    save_path = os.path.join(SAVE_PATH, task, alg)
    if alg == 'ppo':
        # mpi_fork(2)

        logger_kwargs = dict(output_dir=save_path, exp_name=EXP_NAME)
        ppo(env_fn=env_fn, steps_per_epoch=4000, epochs=20000,
             logger_kwargs=logger_kwargs, max_ep_len=1000)

    elif alg == 'ddpg':

        logger_kwargs = dict(output_dir=SAVE_PATH + '/ddpg_suite', exp_name=EXP_NAME)
        ddpg(env_fn=env_fn, steps_per_epoch=5000, batch_size=256, epochs=2000,
             logger_kwargs=logger_kwargs, max_ep_len=200)

    elif alg == 'trpo':

        logger_kwargs = dict(output_dir=SAVE_PATH + '/trpo_suite', exp_name=EXP_NAME)
        trpo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000, epochs=2000,
             logger_kwargs=logger_kwargs, max_ep_len=200)

    elif alg == 'td3':

        logger_kwargs = dict(output_dir=save_path, exp_name=EXP_NAME)
        td3(env_fn=env_fn, start_steps=100000, steps_per_epoch=5000, epochs=2000,
            logger_kwargs=logger_kwargs, max_ep_len=1000)

    elif alg == 'sac':

        logger_kwargs = dict(output_dir=save_path, exp_name=EXP_NAME)
        sac(env_fn=env_fn, start_steps=100000, steps_per_epoch=5000, epochs=2000,
            logger_kwargs=logger_kwargs, max_ep_len=200)


def plot():
    pass


if __name__ == '__main__':
    alg = 'ppo'
    task = 'grasp'
    train(alg, task)
