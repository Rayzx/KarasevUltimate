from game.world.manager import Manager
from game.world.actor.actors import Actor
import pymunk

from game.world.actor.dynamics import Player, Barrel
from game.world.actor.statics import Wall
import resources.resource_manager as rm


class World:
    """

    """

    _instance = None

    def __init__(self):
        World._instance = self
        self._actors = []
        self._add_actors = []
        self._remove_actors = []

        Manager.instance().set_world(self)

        self._space = pymunk.Space()
        self._space.gravity = (0, 0)
        """
        здесь должень быть нормальный обработчик коллизий
        """
        self._space.add_wildcard_collision_handler(0).begin = lambda arbiter, space, data: False
        self._space.add_collision_handler(1, 2).begin = pre_solve
        self._space.add_collision_handler(1, 4).begin = pre_solve

        self._player = None
        self.create_wall()

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

    def create_player(self, x, y):
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
                 Wall(200, -100, t=t, vertices=vertices),
                 Barrel(200, 100, rm.Image_Name.Circle, 10, 'blue'),
                 Barrel(200, 200, rm.Image_Name.Circle, 20, 'blue'),
                 Barrel(200, 300, rm.Image_Name.Circle, 30, 'blue')
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


def no(arbiter, space, data):
    return False


def pre_solve(arbiter, space, data):
    if isinstance(arbiter, pymunk.arbiter.Arbiter):
        actor1 = arbiter.shapes[0].body.data
        actor2 = arbiter.shapes[1].body.data
        if isinstance(actor1, Actor) and isinstance(actor2, Actor):
            actor1.collision(actor2)
            actor2.collision(actor1)
    return True
