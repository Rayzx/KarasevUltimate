import pygame

from game.render.drawable import Drawable
from game.world.world import World
from resources.resource_manager import Resource_Manager, Resource_Type


class Loader:
    """
        загрузчик текстур
    """
    _texture = {}

    @classmethod
    def load(cls):
        for k in Resource_Manager.id.keys():
            Loader._texture[k] = pygame.image.load(Resource_Manager.id[k])

    @classmethod
    def get(cls, t):
        return cls._texture[t]


class Render:
    pass


def draw_world(w: World):
    """
    :param w: экзепляр класса World
    """
    actors = w.get_all_actors()
    screen = pygame.display.get_surface()
    for actor in actors:
        if isinstance(actor, Drawable):

            screen.blit(Loader.get(actor.get_type()), actor.get_rect())

#            a = actor.get_rect()
 #           pygame.draw.rect(screen, (100, 100, 100), (a.x, a.y, a.w, a.h))
