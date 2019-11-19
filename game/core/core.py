import time

import pygame

from game.render.render import Loader
from game.ui_manager.screens import Screen
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

    def start(self, screen: Screen):
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
            #print('t1='+str(time.clock() - t))
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    done = False

            #print('t2=' + str(time.clock() - t))
            Manager.instance().update(delta)

            t = time.clock()
            print('t3=' + str(time.clock() - t))
            Manager.instance().render()

            #print('t4=' + str(time.clock() - t))
            pygame.display.flip()
            pygame.display.get_surface().fill((0, 0, 0))
            """
            # clear/erase the last drawn sprites
                all.clear(screen, background)

        #update all the sprites
        all.update()dirty = all.draw(screen)
            pygame.display.update(dirty)
            """
            print('t5='+str(time.clock() - t))
            self.clock.tick(delta_mls)
        pygame.quit()
