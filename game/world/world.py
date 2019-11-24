from game.world.manager import Manager
from game.world.actor.actors import Actor
import pymunk

from game.world.actor.dynamics import Player
from game.world.actor.statics import Wall
import resources.resource_manager as rm


class World:
    """

    """

    _instance = None

    def __init__(self):
        self._actors = []
        self._add_actors = []
        self._remove_actors = []

        Manager.set_world(self)

        self._space = pymunk.Space()
        self._space.gravity = (0, 0)
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
        self.update_actors_list()

    def update_actors_list(self):
        if len(self._add_actors) > 0:
            for actor in self._add_actors:
                self._actors.append(actor)
                self._space.add(actor.body, actor.shape)
            self._add_actors.clear()
        if len(self._remove_actors) > 0:
            for actor in self._remove_actors:
                self._actors.remove(actor)
                self._space.remove(actor.shape, actor.body)
            self._remove_actors.clear()

    def get_all_actors(self):
        return self._actors

    def create_player(self, x=200, y=200):
        self._player = Player(x, y)
        self._space.add(self._player.body, self._player.shape)
        self._actors.append(self._player)
        return self._player

    def create_wall(self):
        vertices = [(-100, -100), (-100, 100), (100, 100), (100, -100)]
        t = rm.Image_Name.Polygon
        walls = [Wall(200, 500, t=t, vertices=vertices),
                 Wall(200, -100, t=t, vertices=vertices),
                 Wall(200, 500, t=t, vertices=vertices),
                 Wall(0, 100, t=t, vertices=vertices),
                 Wall(0, 300, t=t, vertices=vertices),
                 Wall(400, 100, t=t, vertices=vertices),
                 Wall(400, 300, t=t, vertices=vertices),
                 Wall(200, -100, t=t, vertices=vertices)
                 ]
        for wall in walls:
            self._space.add(wall.body, wall.shape)
            self._actors.append(wall)

    def add_actor(self, actor: Actor):
        self._add_actors.append(actor)

    def remove_actor(self, actor: Actor):
        self._remove_actors.append(actor)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = World()
        return cls._instance


class BodyFactory:
    pass
