import math

import pygame
from pygame.sprite import DirtySprite

from game.world.world import World


class Core:
#this fucking shit!!!!!!!!!
    def __init__(self):
        pygame.init()
        self.sprite = DirtySprite()
        self.image = pygame.image.load('resources/circle.png')
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)
        self.world = World()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def start(self):
        delta = 1 / 60
        done = True
        x = 0.1
        while done:
            x += 0.1
            x %= 255
            for event in pygame.event.get():  # User did something
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    done = False

            y = round(120 * (math.sin(x) + 1))
            self.screen.fill((25, y, 255 - y))
            self.screen.blit(self.image, self.rect)
            self.world.step(delta)
            self.clock.tick(int(1000 * delta))
            pygame.display.flip()
        pygame.quit()
