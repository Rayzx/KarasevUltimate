import math

import pygame
import pymunk

from game.core.core import Core
from game.core.data_manager import FileManager, FileName
from game.render.render import WorldRender, Camera
from game.ui_manager.widgets import Button
from game.ui_manager.mode_interface import Mode
from game.ui_manager.ui_manager import UIManager
from game.world.actor.actors import Actor
from game.world.actor.data_actor import Structure
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall, Barrel, Box
from game.world.actor.items import Heal, Boost
from game.world.actor.player import Player
from game.world.tools.body_factory import DebugFactory, DemoFactory
from game.world.game_manager import GameManager
from game.world.world import World
from game.ui_manager.player_ui import PlayerUI


class MenuMode(Mode):
    def __init__(self):
        self._screen_h = Core.instance().info().current_h
        self._screen_w = Core.instance().info().current_w
        self._buttons = [
            Button(int(self._screen_w / 3), int(self._screen_h / 8), int(self._screen_w / 3), int(self._screen_h / 8),
                   'Новая игра',
                   lambda: UIManager.instance().set_screen((lambda: DebugMode() if FileManager.instance().get(
                       FileName.Setting, 'debug') else GameMode())())),
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
        self._factory = DemoFactory(self._world, FileName.Level_999)
        self._player = self._factory.create_player()
        GameManager.instance().create(self._world, self._player)
        self._factory.create()

        self._screen_h = pygame.display.Info().current_h
        self._render = WorldRender()
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
                if event.key == pygame.K_r:
                    self.reset()
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

    def reset(self):
        self.destroy()
        UIManager.instance().set_screen(GameMode())


class DebugMode(Mode):

    def __init__(self):
        self._debug = FileManager.instance().get(FileName.Setting, 'debug')
        self._walls_debug = FileManager.instance().get(FileName.Setting, 'wall_debug')
        self._start = None
        self._world = World(debug=True)

        self._factory = DebugFactory(self._world, FileName.Level_999, self._walls_debug)
        GameManager.instance().create(self._world, self._factory.create_player())
        self._factory.create()

        self._screen_w = pygame.display.Info().current_w
        self._screen_h = pygame.display.Info().current_h

        self._render = WorldRender()
        self._camera = Camera(self._screen_w, self._screen_h)
        self._render.set_camera(self._camera)
        self._direction = 0
        self._class = StupidEnemy
        self._target = None

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

    def get_point(self):
        x = pygame.mouse.get_pos()[0] - self._screen_w / 2
        y = self._screen_h - pygame.mouse.get_pos()[1] - self._screen_h / 2
        x /= self._camera.zoom
        y /= self._camera.zoom
        x = self._camera.pos[0] + x
        y = self._camera.pos[1] + y
        return x, y

    def _key(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                UIManager.instance().set_screen(MenuMode())
            else:
                if event.key == pygame.K_f:
                    self.save()
                if event.key == pygame.K_1:
                    self._class = StupidEnemy
                elif event.key == pygame.K_2:
                    self._class = Heal
                elif event.key == pygame.K_3:
                    self._class = Boost
                elif event.key == pygame.K_4:
                    self._class = Barrel
                elif event.key == pygame.K_5:
                    self._class = Box
                elif event.key == pygame.K_6:
                    self._class = Player
                elif event.key == pygame.K_w:
                    self._direction |= 1
                elif event.key == pygame.K_d:
                    self._direction |= 2
                elif event.key == pygame.K_s:
                    self._direction |= 4
                elif event.key == pygame.K_a:
                    self._direction |= 8
                elif event.key == pygame.K_MINUS:
                    if self._camera.zoom > 0.1:
                        self._camera.zoom -= 0.1
                elif event.key == pygame.K_EQUALS:
                    if self._camera.zoom < 4:
                        self._camera.zoom += 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._direction &= ~1
            if event.key == pygame.K_d:
                self._direction &= ~2
            if event.key == pygame.K_s:
                self._direction &= ~4
            if event.key == pygame.K_a:
                self._direction &= ~8

    def _mouse(self, event):
        if event.type == pygame.MOUSEMOTION and not self._walls_debug and self._target is not None:
            mouse_pos = self.get_point()
            self._target.body.angle = math.atan2(mouse_pos[1] - self._target.pos[1], mouse_pos[0] - self._target.pos[0])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and self._walls_debug:
                s = self._world.get_space().point_query(self.get_point(), 10,
                                                        pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
                if len(s) > 0:
                    s = s[-1][0].body.data
                    if isinstance(s, Wall):
                        self._world.remove_actor(s)
            if event.button == 1:
                if self._walls_debug:
                    s = self._world.get_space().point_query(self.get_point(), 10,
                                                            pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
                    if len(s) == 0:
                        return
                    if self._start is None:
                        self._start = s[0][0]
                    else:
                        end = s[0][0]
                        x1 = min(self._start.body.position[0], end.body.position[0])
                        y1 = min(self._start.body.position[1], end.body.position[1])
                        x2 = max(self._start.body.position[0], end.body.position[0])
                        y2 = max(self._start.body.position[1], end.body.position[1])
                        v = ((x1 - 5, y1 - 5), (x1 - 5, y2 + 5), (x2 + 5, y2 + 5), (x2 + 5, y1 - 5))
                        GameManager.instance().add_actor(
                            Wall((x1 + x2) / 2, (y1 + y2) / 2, Structure.Polygon, Actor.center(v)))
                        self._start = None
                else:
                    x, y = self.get_point()
                    s = self._world.get_space().point_query(self.get_point(), 10,
                                                            pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
                    if len(s) > 0:
                        s = s[0][0].body.data
                        if not isinstance(s, Wall):
                            self._world.remove_actor(s)
                    else:
                        GameManager.instance().add_actor(self._class(x, y))

    def call(self, event):
        self._key(event)
        self._mouse(event)

    @staticmethod
    def _list_vertex(vertex):
        ll = []
        for i in vertex:
            ll.append((i[0], i[1]))
        return tuple(ll)

    def save(self):
        actors = self._world.get_all_actors()
        if self._walls_debug:
            FileManager.instance().set(FileName.Level_999, 'Walls', [])
        else:
            FileManager.instance().set(FileName.Level_999, 'StupidEnemy', [])
            FileManager.instance().set(FileName.Level_999, 'Box', [])
            FileManager.instance().set(FileName.Level_999, 'Heal', [])
            FileManager.instance().set(FileName.Level_999, 'Barrel', [])
            FileManager.instance().set(FileName.Level_999, 'Player', [])
            FileManager.instance().set(FileName.Level_999, 'Item', [])

        for actor in actors:
            if self._walls_debug:
                if isinstance(actor, Wall):
                    inf = (actor.pos[0], actor.pos[1], self._list_vertex(actor.shape.get_vertices()))
                    FileManager.instance().get(FileName.Level_999, 'Walls').append(inf)
            else:
                if isinstance(actor, StupidEnemy):
                    inf = (actor.pos[0], actor.pos[1])
                    FileManager.instance().get(FileName.Level_999, 'StupidEnemy').append(inf)
                if isinstance(actor, Box):
                    inf = (actor.pos[0], actor.pos[1])
                    FileManager.instance().get(FileName.Level_999, 'Box').append(inf)
                if isinstance(actor, Heal):
                    inf = (actor.pos[0], actor.pos[1])
                    FileManager.instance().get(FileName.Level_999, 'Heal').append(inf)
                if isinstance(actor, Barrel):
                    inf = (actor.pos[0], actor.pos[1])
                    FileManager.instance().get(FileName.Level_999, 'Barrel').append(inf)
                if isinstance(actor, Boost):
                    inf = (actor.pos[0], actor.pos[1], 0)
                    FileManager.instance().get(FileName.Level_999, 'Item').append(inf)
                if isinstance(actor, Player):
                    inf = (actor.pos[0], actor.pos[1])
                    FileManager.instance().get(FileName.Level_999, 'Player').append(inf)
