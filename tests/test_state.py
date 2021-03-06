import dataclasses
from copy import deepcopy

import pytest

from gym_gridverse.agent import Agent
from gym_gridverse.geometry import Orientation
from gym_gridverse.grid import Grid
from gym_gridverse.grid_object import Color, Floor, Key, NoneGridObject, Wall
from gym_gridverse.state import State


def _change_grid(state: State):
    """changes one object in the grid"""
    state.grid[0, 0] = (
        Wall() if isinstance(state.grid[0, 0], Floor) else Floor()
    )


def _change_agent_position(state: State):
    """changes agent position"""
    state.agent.position = dataclasses.replace(
        state.agent.position,
        y=(state.agent.position.y + 1) % state.grid.height,
        x=(state.agent.position.x + 1) % state.grid.width,
    )


def _change_agent_orientation(state: State):
    """changes agent orientation"""
    state.agent.orientation = state.agent.orientation.rotate_back()


def _change_agent_object(state: State):
    """changes agent object"""
    state.agent.obj = (
        Key(Color.RED)
        if isinstance(state.agent.obj, NoneGridObject)
        else NoneGridObject()
    )


@pytest.mark.parametrize(
    'state',
    [
        State(Grid(2, 3), Agent((0, 0), Orientation.N)),
        State(Grid(3, 2), Agent((1, 1), Orientation.S, Key(Color.RED))),
    ],
)
def test_state_eq(state: State):
    other_state = deepcopy(state)
    assert state == other_state

    other_state = deepcopy(state)
    _change_grid(other_state)
    assert state != other_state

    other_state = deepcopy(state)
    _change_agent_position(other_state)
    assert state != other_state

    other_state = deepcopy(state)
    _change_agent_orientation(other_state)
    assert state != other_state

    other_state = deepcopy(state)
    _change_agent_object(other_state)
    assert state != other_state

    other_state = deepcopy(state)
    _change_agent_object(other_state)
    assert state != other_state


def test_state_hash():
    wall_position = (0, 0)
    agent_position = (0, 1)
    agent_orientation = Orientation.N
    agent_object = None

    grid = Grid(2, 2)
    grid[wall_position] = Wall()
    agent = Agent(agent_position, agent_orientation, agent_object)
    state = State(grid, agent)

    hash(state)
