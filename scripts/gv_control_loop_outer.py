#!/usr/bin/env python
import argparse
import itertools as itt
import random
import time

from gym_gridverse.envs.yaml.factory import factory_env_from_yaml
from gym_gridverse.outer_env import OuterEnv
from gym_gridverse.representations.observation_representations import (
    DefaultObservationRepresentation,
)


def make_env(path: str) -> OuterEnv:
    inner_env = factory_env_from_yaml(path)
    rep = DefaultObservationRepresentation(inner_env.observation_space)
    return OuterEnv(inner_env, observation_rep=rep)


def print_observation(observation):
    printable_observation = {k: v.tolist() for k, v in observation.items()}
    print('observation:')
    print(f'{printable_observation}')


def main(args):
    env = make_env(args.path)
    env.reset()

    spf = 1 / args.fps

    for ei in itt.count():
        print(f'# Episode {ei}')
        print()

        env.reset()
        print_observation(env.observation)
        time.sleep(spf)

        for ti in itt.count():
            print(f'episode: {ei}')
            print(f'time: {ti}')

            action = random.choice(env.action_space.actions)
            reward, done = env.step(action)

            print(f'action: {action}')
            print(f'reward: {reward}')
            print_observation(env.observation)
            print(f'done: {done}')
            print()

            time.sleep(spf)

            if done:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='env YAML file')
    parser.add_argument(
        '--fps', type=float, default=1.0, help='frames per second'
    )
    main(parser.parse_args())
