import math

import pymunk

from game.world.actor.actors import Dynamic, Actor
from game.world.actor.data_actor import Structure, collision_type, CollisionType
from game.world.actor.gun import TripleGun
from game.world.actor.bullet import Bullet


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

        # self.body.velocity_func = Dynamic.speed_update_body
        self.body.velocity = (0, 0)  # начальная скорость
        self.body.angular_velocity = 0  # угловая скорость
        self._direction_move = 0  # направление движения (для управления игроком)
        self._old_velocity = (0, 0)  # запись предыдущей добавки к скорости для адекватного перерасчета

        self._shot = False  # флаг для управления выстрелами
        self._gun = TripleGun()  # тип оружия
        self._gun.set_collision_type(
            collision_type[CollisionType.PlayerBullet])  # тип коллизий пуль (не сталуиваются с игроком)
        self._gun.set_color('white')  # цвет пуль
        self.life = 100  # количество жизней
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
        speed = 200
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
            v[0] /= 1.41
            v[1] /= 1.41
        # если движется быстрее чем ему положено, то замедляется
        ll = len(self.body.velocity)
        if ll > speed or self._direction_move == 0:
            k = [-self.body.velocity[0] / ll, -self.body.velocity[1] / ll]
            self.body.velocity += k
        # вычитает предыдущую скорость и добовляет текушую
        self.body.velocity += v
        if ll == 0:
            self._old_velocity = [0, 0]
        else:
            self.body.velocity -= self._old_velocity
            self._old_velocity = v

    def update(self, delta: float):
        """
        обновляет состояние игрока
        :param delta: временной шаг
        """
        self._gun.update(delta)
        if self._shot:
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            self._gun.shot([self.pos[0] + 20 * dx, self.pos[1] + 20 * dy],
                           [dx * 500, dy * 500])
        self._update_velocity()

    def dealDamage(self, damage):
        """
        :param damage: урон
        """
        if self.life - damage > 0:
            self.life = self.life - damage
        else:
            self.life = 0

    def collision(self, actor=None):
        """
        :param actor: актер с которым сталкивается текущий
        """
        if isinstance(actor, Bullet):
            self.dealDamage(10)
        return True


max_velocity = 800
min_velocity = 1
coefficient_of_friction = 3


def speed_update_player(body, gravity, damping, dt):
    if isinstance(body, pymunk.Body) and isinstance(body.velocity, pymunk.Vec2d):
        ll = body.velocity.length
        if ll == 0:
            return
        v = -body.velocity / ll
        v *= body.mass * body.shapes.pop().friction * Dynamic.coefficient_of_friction
        v += gravity
        pymunk.Body.update_velocity(body, v, damping, dt)

        if ll < 1:
            body.velocity = body.velocity * 0
