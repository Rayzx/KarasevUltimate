from game.world.actor.actors import Actor
import pymunk

from game.world.actor.dynamics import Player
from game.world.actor.statics import Wall


class World:
    """

    """

    def __init__(self):
        self._actors = []
        self._space = pymunk.Space()
        self._space.gravity = (0, -100)
        self._player = None
        self.create_wall()

    def pre_solve(self, arbiter, space, data):
        # We want to update the collision normal to make the bounce direction
        # dependent of where on the paddle the ball hits. Note that this
        # calculation isn't perfect, but just a quick example.
        return True

    def step(self, delta: float):
        self._space.step(delta)
        for actor in self._actors:
            if isinstance(actor, Actor):
                actor.update(delta)

    def get_all_actors(self):
        return self._actors

    def create_player(self, x=200, y=200):
        self._player = Player(x, y)
        self._space.add(self._player.body, self._player.shape)
        self._actors.append(self._player)
        return self._player

    def create_wall(self):
        wall = Wall(500)
        self._space.add(wall.body, wall.shape)
        self._actors.append(wall)
        wall = Wall(-100)
        self._space.add(wall.body, wall.shape)
        self._actors.append(wall)
