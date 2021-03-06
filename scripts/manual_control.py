""" Manually control the agent in an environment """

import argparse

from gym_gridverse.action import Action
from gym_gridverse.envs import InnerEnv
from gym_gridverse.envs.factory import STRING_TO_GYM_CONSTRUCTOR, env_from_descr
from gym_gridverse.render_as_string import str_render_obs, str_render_state


def get_user_action() -> Action:
    """Prompts the user for an action input

    Returns:
        Action: action to take
    """
    while True:
        input_action = input(f"Action? (in (0,{len(Action)})): ")

        try:
            action = Action(int(input_action))
        except ValueError:
            pass
        else:
            return action


def manually_control(domain: InnerEnv):
    domain.reset()
    while True:

        a = get_user_action()

        r, t = domain.step(a)

        if t:
            print("Resetting environment")
            domain.reset()

        state = domain.state
        obs = domain.observation

        print(
            f"Reward {r}, "
            f"next state:\n{str_render_state(state)}\n"
            f"observation:\n{str_render_obs(obs)}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'descr',
        help=f"Gym description, available: {list(STRING_TO_GYM_CONSTRUCTOR.keys())}",
    )
    manually_control(env_from_descr(parser.parse_args().descr))
