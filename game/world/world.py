from game.world.actor.actors import Actor
import pymunk


class World:

    def __init__(self, debug=False):
        World._instance = self
        self._actors = []
        self._add_actors = []
        self._remove_actors = []
        self._debug = debug
        self._space = pymunk.Space(True)
        self._space.threads = 4
        self._space.gravity = (0, 0)
        h = self._space.add_default_collision_handler()
        h.pre_solve = call_pre

    def step(self, delta: float):
        if not self._debug:
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

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            self._add_actors.append(actor)
        else:
            self._add_actors.extend(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor):
            self._remove_actors.append(actor)
        else:
            self._remove_actors.extend(actor)

    def get_space(self):
        return self._space


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
        if c1 & c0 == 0:
            return False
        else:
            c1 = arbiter.shapes[0].body.data
            c2 = arbiter.shapes[1].body.data
            if isinstance(c1, Actor) and isinstance(c2, Actor):
                if c1.collision(c2) and c2.collision(c1):
                    return True
                else:
                    return False

    return True
