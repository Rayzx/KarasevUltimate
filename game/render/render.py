import threading
from multiprocessing.pool import ThreadPool

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

    def __init__(self):
        self._screen = pygame.display.get_surface()
        self._pool = ThreadPool(1)

    def _draw_actor(self, actor: Drawable):
        #self._screen.blit(Loader.get(actor.get_type()), actor.get_rect())
        #print(threading.current_thread().name)
        a = actor.get_rect()
        pygame.draw.rect(self._screen, (10, 100, 100), (a.x, a.y, a.w, a.h))

    def draw_world(self, w: World):
        """
        :param w: экзепляр класса World
        """
        actors = w.get_all_actors()
        self._pool.map(self._draw_actor, actors)
        # pool.close()
