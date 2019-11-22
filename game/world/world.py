from game.world.actor.actors import Actor
import pymunk

from game.world.actor.dynamics.player import Player


class World:
    """

    """

    def __init__(self):
        self._actors = []
        self._space = pymunk.Space()
        self._space.gravity = (0, 0)
        self._player = Player(  )
        self._space.add(self._player.body, self._player.shape)
        self._actors.append(self._player)

    def step(self, delta: float):
        self._space.step(delta)
        for actor in self._actors:
            if isinstance(actor, Actor):
                actor.update(delta)

    def get_all_actors(self):
        return self._actors
