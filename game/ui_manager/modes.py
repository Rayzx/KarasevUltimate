import math

import pygame
import pymunk

from game.core.core import Core
from game.core.data_manager import FileManager, FileName
from game.render.render import Render, Camera
from game.ui_manager.widgets import Button
from game.ui_manager.mode_interface import Mode
from game.ui_manager.ui_manager import UIManager
from game.world.actor.actors import Actor
from game.world.actor.data_actor import Structure
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall
from game.world.tools.body_factory import BodyFactory, DebugFactory, DemoFactory
from game.world.game_manager import GameManager
from game.world.world import World
from game.ui_manager.player_ui import PlayerUI

debug = False


class MenuMode(Mode):
    def __init__(self):
        self._screen_h = Core.instance().info().current_h
        self._screen_w = Core.instance().info().current_w
        self._buttons = [
            Button(int(self._screen_w / 3), int(self._screen_h / 8), int(self._screen_w / 3), int(self._screen_h / 8),
                   'Новая игра',
                   lambda: UIManager.instance().set_screen((lambda: DebugMode() if debug else GameMode())())),
            Button(int(self._screen_w / 3), int(self._screen_h / 4) + int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), 'Выбрать разрешение',
                   lambda: UIManager.instance().set_screen(SettingsMode())),
            Button(int(self._screen_w / 3), int(3 * self._screen_h / 8) + 2 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8),
                   'Счетчик fps:{0}'.format(
                       (lambda x: "Вкл" if x else "Выкл")(FileManager.instance().get(FileName.Setting, "fps"))),
                   self.toggle)]

    def show(self):
        pass

    def update(self, delta: float):
        pass

    def render(self):
        for button in self._buttons:
            button.draw()

    def destroy(self):
        pass

    def call(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            UIManager.done = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self._buttons:
                button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for b in self._buttons:
                if b.contain(mouse_pos):
                    b.clicked()

    def toggle(self):
        fps = not FileManager.instance().get(FileName.Setting, 'fps')
        FileManager.instance().set(FileName.Setting, 'fps', fps)
        self._buttons[2].text = 'Счетчик fps:{0}'.format((lambda x: "Вкл" if x else "Выкл")(fps))
        Core.instance().update_settings()
        UIManager.instance().set_screen(MenuMode())


class SettingsMode(Mode):
    def __init__(self):
        self._resolutions = {0: [800, 600], 1: [1280, 720], 2: [1600, 900], 3: [1920, 1080]}
        self._screen_h = pygame.display.Info().current_h
        self._screen_w = pygame.display.Info().current_w
        self._buttons = [
            Button(int(self._screen_w / 3), int(self._screen_h / 10), int(self._screen_w / 3), int(self._screen_h / 8),
                   '800x600', self.reset),
            Button(int(self._screen_w / 3), int(self._screen_h / 5) + int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1280x720', self.reset),
            Button(int(self._screen_w / 3), int(3 * self._screen_h / 10) + 2 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1600x900', self.reset),
            Button(int(self._screen_w / 3), int(4 * self._screen_h / 10) + 3 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), '1920x1080', self.reset),
            Button(int(self._screen_w / 3), int(5 * self._screen_h / 10) + 4 * int(self._screen_h / 8 * 0.29),
                   int(self._screen_w / 3), int(self._screen_h / 8), 'Назад',
                   lambda x: UIManager.instance().set_screen(MenuMode()))]

    def show(self):
        pass

    def render(self):
        for button in self._buttons:
            button.draw()

    def update(self, delta: float):
        pass

    def destroy(self):
        pass

    def reset(self, i):
        if i in self._resolutions:
            FileManager.instance().set(FileName.Setting, "width", self._resolutions[i][0])
            FileManager.instance().set(FileName.Setting, "height", self._resolutions[i][1])
            Core.instance().update_settings()
            UIManager.instance().set_screen(SettingsMode())

    def call(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            UIManager.instance().set_screen(MenuMode())
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self._buttons:
                button.update(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(0, len(self._buttons)):
                if self._buttons[i].contain(mouse_pos):
                    self._buttons[i].clicked(i)
                    break


class GameMode(Mode):

    def __init__(self):
        self._world = World()
        self._factory = DemoFactory(self._world)
        self._player = self._factory.create_player()
        GameManager.instance().create(self._world, self._player)
        self._factory.create()

        self._screen_h = pygame.display.Info().current_h
        self._render = Render()
        self._camera = Camera(Core.instance().info().current_w, self._screen_h)
        self._render.set_camera(self._camera)
        self._direction = 0

        # test PlayerUI
        self._playerUI = PlayerUI(self._player)

    def show(self):
        pass

    def update(self, delta: float):
        self._player.move(self._direction)
        self._world.step(delta)
        self._camera.pos = self._player.body.position

        self._playerUI.update()

    def render(self):
        self._render.draw_world(self._world)
        self._playerUI.draw()

    def destroy(self):
        pass

    def call(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                UIManager.instance().set_screen(MenuMode())
            else:
                if event.key == pygame.K_w:
                    self._direction |= 1
                if event.key == pygame.K_d:
                    self._direction |= 2
                if event.key == pygame.K_s:
                    self._direction |= 4
                if event.key == pygame.K_a:
                    self._direction |= 8
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            p = self._camera.transform_coord(self._player.pos.x, self._player.pos.y)
            self._player.set_direction(-math.atan2(mouse_pos[1] - p[1], mouse_pos[0] - p[0]))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._player.shot(True)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._player.shot(False)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._direction &= ~1
            if event.key == pygame.K_d:
                self._direction &= ~2
            if event.key == pygame.K_s:
                self._direction &= ~4
            if event.key == pygame.K_a:
                self._direction &= ~8


class DebugMode(Mode):

    def __init__(self):
        self.size = 5
        self.start = None
        self.end = None
        self._world = World(debug=True)

        self._factory = DebugFactory(self._world)
        GameManager.instance().create(self._world, self._factory.create_player())
        self._factory.create()

        self._screen_w = pygame.display.Info().current_w
        self._screen_h = pygame.display.Info().current_h
        self._render = Render()
        self._camera = Camera(self._screen_w, self._screen_h)
        self._render.set_camera(self._camera)
        self._direction = 0

    def show(self):
        pass

    def update(self, delta: float):
        self._world.step(delta)
        if self._direction & 1 != 0:
            self._camera.pos[1] += 10
        if self._direction & 2 != 0:
            self._camera.pos[0] += 10
        if self._direction & 4 != 0:
            self._camera.pos[1] -= 10
        if self._direction & 8 != 0:
            self._camera.pos[0] -= 10

    def render(self):
        self._render.draw_world(self._world)

    def destroy(self):
        pass

    def call(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                UIManager.instance().set_screen(MenuMode())
            else:
                if event.key == pygame.K_w:
                    self._direction |= 1
                if event.key == pygame.K_d:
                    self._direction |= 2
                if event.key == pygame.K_s:
                    self._direction |= 4
                if event.key == pygame.K_a:
                    self._direction |= 8
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # p = self._camera.transform_coord(self._player.pos.x, self._player.pos.y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = pygame.mouse.get_pos()[0] - self._screen_w / 2
                y = self._screen_h - pygame.mouse.get_pos()[1] - self._screen_h / 2
                x /= self._camera.zoom
                y /= self._camera.zoom
                x = self._camera.pos[0] + x
                y = self._camera.pos[1] + y
                s = self._world.get_space().point_query((x, y), 10,
                                                        pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
                if len(s) == 0:
                    print('None')
                    return
                if self.start is None:
                    self.start = s[0][0]
                else:
                    self.end = s[0][0]
                    x1 = min(self.start.body.position[0], self.end.body.position[0])
                    y1 = min(self.start.body.position[1], self.end.body.position[1])
                    x2 = max(self.start.body.position[0], self.end.body.position[0])
                    y2 = max(self.start.body.position[1], self.end.body.position[1])
                    v = None
                    if y1 == y2:
                        v = [[x1 - 5, y1 - 5], [x1 - 5, y1 + 5], [x2 + 5, y2 + 5], [x2 + 5, y2 - 5]]
                    if x1 == x2:
                        v = [[x1 - 5, y1 - 5], [x1 + 5, y1 - 5], [x2 + 5, y2 + 5], [x2 - 5, y2 + 5]]
                    GameManager.instance().add_actor(
                        Wall((x1 + x2) / 2, (y1 + y2) / 2, Structure.Polygon, Actor.center(v)))
                    print('Wall(' + str((x1 + x2) / 2) + ',' + str(
                        (y1 + y2) / 2) + ',Structure.Polygon, Actor.center(' + str(v) + ')),')
                    self.start = None
            if event.button == 3:
                x = pygame.mouse.get_pos()[0] - self._screen_w / 2
                y = self._screen_h - pygame.mouse.get_pos()[1] - self._screen_h / 2
                x /= self._camera.zoom
                y /= self._camera.zoom
                x = self._camera.pos[0] + x
                y = self._camera.pos[1] + y
                GameManager.instance().add_actor(StupidEnemy(x, y))
                print(
                    'StupidEnemy(' + str(x) + ',' + str(y) + ')')

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._direction &= ~1
            if event.key == pygame.K_d:
                self._direction &= ~2
            if event.key == pygame.K_s:
                self._direction &= ~4
            if event.key == pygame.K_a:
                self._direction &= ~8
