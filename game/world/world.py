from game.world.actor.actors import Actor
import pymunk


class World:
    def __init__(self):
        World._instance = self
        self._actors = []
        self._add_actors = []
        self._remove_actors = []

        self._space = pymunk.Space()
        self._space.gravity = (0, 0)
        """
        здесь должень быть нормальный обработчик коллизий
        """
        self._space.add_wildcard_collision_handler(0).begin = lambda arbiter, space, data: False
        
        self._space.add_collision_handler(Actor.collision_type['Bullet'],
                                          Actor.collision_type['Bullet']).begin = lambda \
                arbiter, space, data: False
        self._space.add_collision_handler(Actor.collision_type['Bullet'],
                                          Actor.collision_type['Player']).begin = lambda \
                arbiter, space, data: False
        self._space.add_collision_handler(Actor.collision_type['Bullet'],
                                          Actor.collision_type['Ghost']).begin = pre_solve
        self._space.add_collision_handler(Actor.collision_type['Bullet'],
                                          Actor.collision_type['Environment']).begin = pre_solve

    #        h = self._space.add_default_collision_handler()
    #       h.pre_solve = call_pre

    def step(self, delta: float):
        self._space.step(delta)
        for actor in self._actors:
            if isinstance(actor, Actor):
                actor.update(delta)
        self._update_actors_list()

    def _update_actors_list(self):
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

    def add_actor(self, actor: Actor):
        self._add_actors.append(actor)

    def remove_actor(self, actor: Actor):
        self._remove_actors.append(actor)


def pre_solve(arbiter, space, data):
    if isinstance(arbiter, pymunk.arbiter.Arbiter):
        actor1 = arbiter.shapes[0].body.data
        actor2 = arbiter.shapes[1].body.data
        if isinstance(actor1, Actor) and isinstance(actor2, Actor):
            actor1.collision(actor2)
            actor2.collision(actor1)
    return True


def call_pre(arbiter, space, data):
    if isinstance(arbiter, pymunk.arbiter.Arbiter):
        shape0 = arbiter.shapes[0]
        shape1 = arbiter.shapes[1]
        c0 = shape0.collision_type
        c1 = shape1.collision_type
        if c1 == 0 or c0 == 0:
            return False

    return True
