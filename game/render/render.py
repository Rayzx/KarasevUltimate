import numpy
import pygame
import pygame.gfxdraw
from pymunk import Vec2d

from game.world.actor.actors import Actor
from game.world.world import World
import resources.resource_manager as rm


class Loader:
    """
        загрузчик текстур
    """
    _texture = {}

    @classmethod
    def load(cls):
        for k in rm.names.keys():
            Loader._texture[k] = pygame.image.load(rm.names[k])

    @classmethod
    def get(cls, t):
        return cls._texture[t]


class Render:

    def __init__(self):
        self._screen = pygame.display.get_surface()
        self.coord = numpy.array([0, 0])

    def draw_world(self, w: World):
        """
        :param w: экзепляр класса World
        """
        actors = w.get_all_actors()
        for actor in actors:
            if isinstance(actor, Actor):
                name = actor.texture
                shape = actor.shape
                b = actor.body
                color = actor.color
                if name == rm.Texture_Name.Circle:
                    pygame.draw.circle(self._screen, color,
                                       self.transform_coord(b.position, (0, 0)),
                                       int(shape.radius))

    def transform_coord(self, pos, x, y=None):
        if y is None:
            coord = numpy.array([0] * len(x))
            for num in range(len(x) // 2):
                coord[2 * num], coord[2 * num + 1] = self.transform_coord(pos, x[2 * num], x[2 * num + 1])
            return coord
        else:
            x += int(pos[0])
            y += int(pos[1])
            return x, y


class Camera:

    def __init__(self, w: float, h: float):
        self._w = w
        self._h = h
        self.pos = Vec2d(0, 0)
        self._zoom = 0.5

    def transform_coord(self, x, y=None):
        if y is None:
            if isinstance(x, list):
                for num in range(len(x) // 2):
                    x[2 * num], x[2 * num + 1] = self.transform_coord(x[2 * num], x[2 * num + 1])
                return x
        else:
            x -= self.pos.x
            y -= self.pos.y
            x, y = self._zooms(x, y)
            return x, y

    def _zooms(self, x, y):
        x -= self._w / 2
        x *= self._zoom
        x += self._w / 2
        y -= self._h / 2
        y *= self._zoom
        y += self._h / 2
        return x, y
