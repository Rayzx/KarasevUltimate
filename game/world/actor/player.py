import math

import pymunk
from pymunk import ContactPoint

from game.world.actor.actors import Dynamic, Actor
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import Structure, collision_type, CollisionType
from game.world.actor.environment import Wall
from game.world.actor.gun import TripleGun
from game.world.actor.gun import DefaultGun


class Player(Dynamic):
    """
        класс игрока
    """

    def __init__(self, x=0, y=0, stats=None):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=Actor.center([[-10, 10], [30, 0], [-10, -10], [-20, 0]]),
                         color='blue')
        # информация об игроке
        self._stat = stats
        if stats is None:
            self._stat = Player.get_default_stats()

        self.shape.elasticity = 0  # упругость
        self.shape.friction = 1  # трение
        self.shape.collision_type = collision_type[CollisionType.Player]  # тип коллизии

        self.body.velocity = (0, 0)  # начальная скорость
        self.body.angular_velocity = 0  # угловая скорость
        self._direction_move = 0  # направление движения (для управления игроком)

        self._shot = False  # флаг для управления выстрелами
        if self._stat["Gun"] == 0:
            self._gun = DefaultGun(self._stat["Bullet"])  # тип оружия
        else:
            self._gun = TripleGun(self._stat["Bullet"])
        self._gun.set_collision_type(
            collision_type[CollisionType.PlayerBullet])  # тип коллизий пуль (не сталуиваются с игроком)
        self._gun.set_color('aquamarine2')  # цвет пуль
        self.type_gun = 0
        self.type_bul = 0
        self.life = self._stat["Heal"]  # количество жизней
        self.maxLife = self._stat["MaxHeal"]
        
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
        if not len(self.body.velocity) > self.speed:
            self.body.velocity = v

    def update(self, delta: float):
        """
        обновляет состояние игрока
        :param delta: временной шаг
        """
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

    def changeGun(self, gun=-1, bullet=-1):
        if gun == -1:
            gun = self.type_gun
        if bullet == -1:
            bullet = self.type_bul
        if gun == 0:
            self._gun = DefaultGun(bullet)
            self._gun.set_collision_type(collision_type[CollisionType.PlayerBullet])
            self._gun.set_color('aquamarine2')
        elif gun == 1:
            self._gun = TripleGun(bullet)
            self._gun.set_collision_type(collision_type[CollisionType.PlayerBullet])
            self._gun.set_color('aquamarine2')
        self.type_gun = gun
        self.type_bul = bullet

    @staticmethod
    def get_default_stats():
        return {"Heal": 10, "Gun": 0, "Bullet": 0, "MaxHeal": 10}
