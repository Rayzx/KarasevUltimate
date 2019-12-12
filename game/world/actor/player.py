import math

from game.world.actor.actors import Dynamic, Actor, CollisionType, Structure
from game.world.actor.gun import TripleGun


class Player(Dynamic):
    """
    """

    def __init__(self, x=0, y=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Polygon,
                         vertices=Actor.center([[-10, 10], [30, 0], [-10, -10], [-20, 0]]),
                         color='red')

        self.shape.elasticity = 1
        self.shape.friction = 5
        self.shape.collision_type = Actor.collision_type[CollisionType.Player]

        self.body.velocity_func = Dynamic.speed_update_body
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        self._direction_move = 0
        self._shot = False
        self._gun = TripleGun()
        self._gun.set_collision_type(Actor.collision_type[CollisionType.PlayerBullet])
        self._gun.set_color('green')

    def set_direction(self, angle: float):
        """

        :param angle:
        :return:
        """
        self.body.angle = angle

    def shot(self, flag):
        self._shot = flag

    def move(self, d):
        self._direction_move = d

    def update(self, delta: float):
        self._gun.update(delta)
        if self._shot:
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            self._gun.shot([self.pos[0] + 20 * dx, self.pos[1] + 20 * dy],
                           [dx * 500, dy * 500])

        v = [0, 0]
        speed = 200
        self.body.angular_velocity = 0
        if self._direction_move != 0:
            if self._direction_move & 1 != 0:
                v[1] += speed
            elif self.body.velocity[1] > 0 and self._direction_move & 4 == 0:
                v[1] = self.body.velocity[1]
            if self._direction_move & 2 != 0:
                v[0] += speed
            elif self.body.velocity[0] > 0 and self._direction_move & 8 == 0:
                v[0] = self.body.velocity[0]
            if self._direction_move & 4 != 0:
                v[1] -= speed
            elif self.body.velocity[1] < 0 and self._direction_move & 1 == 0:
                v[1] = self.body.velocity[1]
            if self._direction_move & 8 != 0:
                v[0] -= speed
            elif self.body.velocity[0] < 0 and self._direction_move & 2 == 0:
                v[0] = self.body.velocity[0]
            if self._direction_move == 3 or self._direction_move == 6 or self._direction_move == 12 or self._direction_move == 9:
                v[0] /= 1.41
                v[1] /= 1.41
            self.body.velocity = v

