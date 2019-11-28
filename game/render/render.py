import pygame
import pymunk

from game.core.core import Core
from game.world.actor.actors import Actor
from game.world.world import World
import resources.resource_manager as rm


# todo перенести лоадер куда-нибудь чтобы core мог его импортить

class Loader:
    """
        загрузчик текстур
    """
    _image = {}

    @classmethod
    def load(cls):
        for k in rm.names.keys():
            Loader._image[k] = pygame.image.load(rm.names[k])

    @classmethod
    def get(cls, t):
        return cls._image[t]


class Render:
    def __init__(self):
        self._screen = pygame.display.get_surface()
        self._h = Core.instance().info().current_h
        self._camera = None

    def draw_world(self, w: World):
        """
        :param w: экзепляр класса World
        """
        actors = w.get_all_actors()
        for actor in actors:
            if isinstance(actor, Actor):
                if actor.visible:
                    name = actor.image
                    shape = actor.shape
                    body = actor.body
                    color = pygame.color.THECOLORS[actor.color]
                    if name == rm.Image_Name.Circle:
                        pygame.draw.circle(self._screen, color, self._transform_coord(body, 0, 0),
                                           int(self._transform_segment(shape.radius)))
                    if name == rm.Image_Name.Polygon:
                        pygame.draw.polygon(self._screen, color,
                                            self._transform_coord(body, shape.get_vertices()))

    def set_camera(self, camera):
        self._camera = camera

    def _transform_coord(self, body, x, y=None):
        if y is None:
            coord = []
            pos = body.position
            angle = body.angle
            for vertex in x:
                a, b = vertex.rotated(angle) + pos
                if self._camera:
                    a, b = self._camera.transform_coord(a, b)
                coord.append((a, self._h - b))
            return coord
        else:
            x += body.position[0]
            y += body.position[1]
            if self._camera:
                x, y = self._camera.transform_coord(x, y)
            return int(x), self._h - int(y)

    def _transform_segment(self, l):
        if self._camera:
            return self._camera.transform_segment(l)
        else:
            return l


class Camera:

    def __init__(self, w: float, h: float):
        self._w = w
        self._h = h
        self._pos = pymunk.Vec2d(0, 0)
        self._zoom = 0.7

    def transform_coord(self, x, y):
        x = x - self._pos[0]
        y = y - self._pos[1]
        x, y = self._zooms(x, y)
        x += self._w / 2
        y += self._h / 2
        return x, y

    def transform_segment(self, l):
        return l * self._zoom

    def _zooms(self, x, y):
        x *= self._zoom
        y *= self._zoom
        return x, y

    def _get_pos(self):
        return self._pos

    def _set_pos(self, value):
        self._pos = value

    pos = property(_get_pos, _set_pos)
