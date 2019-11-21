import pygame
import pygame.gfxdraw
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

    def draw_world(self, w: World):
        """
        :param w: экзепляр класса World
        """
        actors = w.get_all_actors()
        for actor in actors:
            if isinstance(actor, Actor):
                name = actor.texture
                r = actor.rect
                color = actor.color
                if name == rm.Texture_Name.Circle:
                    pygame.draw.circle(self._screen, color, [r.x, r.y], r.w)
                if name == rm.Texture_Name.Rectangle:
                    pygame.draw.rect(self._screen, color, r)
