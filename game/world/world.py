from game.world.actor.actors import Actor
from game.world.actor.dynamics.Ball import Ball


class World:
    """

    """
    def __init__(self):
        self._actors = []
        for i in range(80):
            self._actors.append(Ball())

    def step(self, delta: float):
        for actor in self._actors:
            if isinstance(actor, Actor):
                actor.update(delta)

    def get_all_actors(self):
        return self._actors
