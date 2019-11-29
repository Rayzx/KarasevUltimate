import time

import pygame

from game.ui_manager.screen_interface import Screen
from game.ui_manager.ui_manager import Manager


class Core:
    """
    """

    _instance = None

    def __init__(self, settings: dict):
        Core._instance = self
        pygame.mixer.init(buffer=512)
        # инициализирует pygame
        pygame.init()

        # загружает текстуры
        # Loader.load()

        # класс часов pygame
        self._clock = pygame.time.Clock()

        # экран на котором происходит отрисовка
        self._flags =  pygame.DOUBLEBUF
        self._window = pygame.display.set_mode((settings['width'], settings['height']), self._flags)
        self._window.fill((0, 0, 0))
        self._window.set_alpha(None)
        self._info = pygame.display.Info()

        if settings['fps']:
            self.fps_counter = Fps()
        else:
            self.fps_counter = None

    def start(self, screen: Screen):
        """
            начало main_loop
            :param screen: начальный экран приложения
        """

        Manager.instance().set_screen(screen)  # start game

        # время в секундах
        delta = 1 / 60
        done = True
        delta_time = -1
        while done:

            t = time.clock()

            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    done = False
                else:
                    Manager.instance().get_screen().call(event)

            Manager.instance().update(delta)
            Manager.instance().render()

            if self.fps_counter and delta_time != -1:
                self.fps_counter.add_delta(delta_time)
                self.fps_counter.draw(self._window)

            self._clock.tick(60)
            pygame.display.flip()
            self._window.fill((0, 0, 0))
            delta_time = time.clock() - t
        pygame.quit()

    def update_settings(self, settings: dict):
        self._window = pygame.display.set_mode((settings['width'], settings['height']), self._flags)
        self._info = pygame.display.Info()
        if not settings['fps']:
            self.fps_counter = None
        elif not self.fps_counter:
            self.fps_counter = Fps()

    def info(self):
        return self._info

    @classmethod
    def instance(cls):
        return cls._instance


class Fps:
    """
        счетчик fps
        каждую интерацию добавляется время этой итерации (add_delta)
        каждые update_num операции fps пересчитывается
    """

    def __init__(self, update_num=10):
        self.font = pygame.font.SysFont("courier", 24)
        self.delta = 0.0
        self.num_delta = 0
        self.update_num = update_num
        self.fps = str(60)
        self.color = pygame.color.THECOLORS['yellow']
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
