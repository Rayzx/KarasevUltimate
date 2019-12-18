import math

import pymunk
from pymunk import ContactPoint

from game.world.actor.actors import Dynamic, Actor
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure, collision_type, CollisionType
from game.world.actor.environment import Wall
from game.world.actor.gun import TripleGun
from game.world.actor.gun import DefaultGun
from game.ui_manager.ui_manager import UIManager

class Player(Dynamic):
    """
        класс игрока
    """

    def __init__(self, x=0, y=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=Actor.center([[-10, 10], [30, 0], [-10, -10], [-20, 0]]),
                         color='blue')

        self.shape.elasticity = 0  # упругость
        self.shape.friction = 1  # трение
        self.shape.collision_type = collision_type[CollisionType.Player]  # тип коллизии

        self.body.velocity = (0, 0)  # начальная скорость
        self.body.angular_velocity = 0  # угловая скорость
        self._direction_move = 0  # направление движения (для управления игроком)
        self._old_velocity = (0, 0)  # запись предыдущей добавки к скорости для адекватного перерасчета
        self.no_collision = False
        self._shot = False  # флаг для управления выстрелами
        self._gun = DefaultGun(0)  # тип оружия
        self._gun.set_collision_type(
            collision_type[CollisionType.PlayerBullet])  # тип коллизий пуль (не сталуиваются с игроком)
        self._gun.set_color('aquamarine2')  # цвет пуль
        self.life = 5  # количество жизней
        self.maxLife = 5
        self.shield = 100  # какая-то хрень
        # self.health = 100 еще одна непонятная зрень))

    def set_direction(self, angle: float):
        """
        :param angle: устанавливает угол поворота тела
        """
        self.body.angle = angle

    def shot(self, flag):
        """
        :param flag: флаг для выстрела
        """
        self._shot = flag

    def move(self, d):
        """
        :param d: направление в битовой маске (1,2,4,8 по часовой стрелке)
        """
        self._direction_move = d

    def _update_velocity(self):
        """
            метод перерасчета скорости
        """
        v = [0, 0]
        speed = self.speed
        self.body.angular_velocity = 0
        # определение нового направления скорости
        if self._direction_move & 1 != 0:
            v[1] += speed
        if self._direction_move & 2 != 0:
            v[0] += speed
        if self._direction_move & 4 != 0:
            v[1] -= speed
        if self._direction_move & 8 != 0:
            v[0] -= speed
        if self._direction_move == 3 or self._direction_move == 6 or self._direction_move == 12 or self._direction_move == 9:
            v[0] /= 1.42
            v[1] /= 1.42
        if not len(self.body.velocity)>self.speed:
            self.body.velocity = v

    def update(self, delta: float):
        """
        обновляет состояние игрока
        :param delta: временной шаг
        """
        if self.no_collision:
            self.body.position = self._old_velocity
        self.no_collision = False
        self.update_effects(delta)
        self._gun.update(delta)
        if self._shot:
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            self._gun.shot([self.pos[0] + 20 * dx, self.pos[1] + 20 * dy],
                           [dx * 500, dy * 500])
        self._update_velocity()



    def collision(self, actor=None):
        """
        :param actor: актер с которым сталкивается текущий
        """
        if isinstance(actor, Bullet):
            self.dealDamage(1)
        if isinstance(actor, Wall):
            s = self.shape.shapes_collide(actor.shape)
            if isinstance(s, pymunk.contact_point_set.ContactPointSet):
                q = s.points[0]
                if isinstance(q, ContactPoint):
                    self.body.position += s.normal * q.distance
        return True
