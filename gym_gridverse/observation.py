from .info import Agent, Grid


class Observation:
    def __init__(self, grid: Grid, agent: Agent):
        self.grid = grid
        self.agent = agent

    def __eq__(self, other):
        if isinstance(other, Observation):
            return self.grid == other.grid and self.agent == other.agent
        return NotImplemented
