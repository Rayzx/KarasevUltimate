import time

import pygame

from game.render.render import Loader
from game.ui_manager.ui_manager import Manager


class Core:

    def __init__(self):
        # инициализирует pygame
        pygame.init()

        # загружает текстуры
        Loader.load()

        # класс часов pygame
        self.clock = pygame.time.Clock()

        # экран на котором происходит отрисовка
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.window = pygame.display.set_mode((0, 0), flags)
        self.window.fill((0, 0, 0))
        self.window.set_alpha(None)

    def start(self, screen):
        """
        начало main_loop
        :param screen: начальный экран приложения
        """
        Manager.instance().set_screen(screen)

        # время в секундах и милисекундах
        delta = 1 / 60
        delta_mls = int(1000 * delta)
        done = True
        while done:
            pygame.display.get_surface().fill((0, 0, 0))

            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    done = False
            #t = time.clock()
            Manager.instance().update(delta)
            Manager.instance().render()
            #print(time.clock() - t)
            self.clock.tick(delta_mls)
            pygame.display.flip()
        pygame.quit()
