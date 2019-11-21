import time

import pygame

from game.render.render import Loader
from game.ui_manager.ui_manager import Manager
from resources.resource_manager import Colors


class Core:
    """

    """

    def __init__(self, fps=False):
        # инициализирует pygame
        pygame.init()

        # загружает текстуры
        Loader.load()

        # класс часов pygame
        self.clock = pygame.time.Clock()

        # экран на котором происходит отрисовка
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.window = pygame.display.set_mode(flags=flags)
        self.window.fill((0, 0, 0))
        self.window.set_alpha(None)

        if fps:
            self.fps_counter = Fps()
        else:
            self.fps_counter = None

    def start(self, screen):
        """
            начало main_loop
            :param screen: начальный экран приложения
        """

        Manager.instance().set_screen(screen)

        # время в секундах и милисекундах
        delta = 1 / 60
        done = True
        while done:

            t = time.clock()

            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    done = False

            Manager.instance().update(delta)
            Manager.instance().render()

            self.clock.tick(60)
            pygame.display.flip()
            self.window.fill((0, 0, 0))

            if self.fps_counter:
                self.fps_counter.add_delta(time.clock() - t)
                self.fps_counter.draw(self.window)

        pygame.quit()


class Fps:

    def __init__(self, update_num=10):
        self.font = pygame.font.SysFont("courier", 24)
        self.delta = 0.0
        self.num_delta = 0
        self.update_num = update_num
        self.fps = str(60)
        self.color = Colors.yellow
        self.pos = (0, 0)

    def add_delta(self, delta):
        self.num_delta += 1
        self.delta += delta
        if self.num_delta == self.update_num:
            self.num_delta = 0
            self.fps = str(self.update_num / self.delta)[0:4]
            self.delta = 0

    def draw(self, screen):
        screen.blit(self.font.render(self.fps, True, self.color), self.pos)
