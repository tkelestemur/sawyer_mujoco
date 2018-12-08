import os
import numpy as np
from spinup.utils.test_policy import load_policy
from envs.sawyer_env import SawyerReachEnv, SawyerGraspEnv
GRIPPER_LINK = 'right_gripper_tip'

PATH = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = PATH + '/results/sawyer/ppo'


def play():
    _, get_action = load_policy(SAVE_PATH)
    env = SawyerGraspEnv(n_substeps=1)
    n_episode = 1
    ep_len, ep_ret, i = 0, 0, 0
    max_ep_len = 10000
    obs = env.reset()

    while i < n_episode:
        action = get_action(obs)
        # print('Action: {}'.format(action))
        obs, r, d, reward_info = env.step(action)
        ep_len += 1
        ep_ret += r
        # print('dist_reward: {} grasp_reward: {} terminal_reward: {}'.format(reward_info['dist_reward'],
        #                                                                     reward_info['grasp_reward'],
        #                                                                     reward_info['terminal_reward']))
        env.render()
        if d or (ep_len == max_ep_len):
            print('DONE: Episode Length: {} Episode Reward {}'.format(ep_len, ep_ret))
            obs = env.reset()
            ep_len, ep_ret, r = 0, 0, 0
            d = False
            i += 1
            # time.sleep(1)


if __name__ == '__main__':
    play()
