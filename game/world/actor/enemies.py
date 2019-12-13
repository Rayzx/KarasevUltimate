import math

from game.world.actor.actors import Dynamic
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import collision_type, Structure, CollisionType
from game.world.actor.player import Player
from game.world.actor.gun import DefaultGun
from game.world.tools.ray import RayManager
from game.world.game_manager import GameManager


class StupidEnemy(Dynamic):

    def __init__(self, x=0, y=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Circle,
                         vertices=10,
                         color='grey')

        self.shape.elasticity = 1
        self.shape.friction = 5
        self.shape.collision_type = collision_type[CollisionType.Enemy]

        self.body.velocity_func = Dynamic.speed_update_body
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0
        self._direction_move = 0
        self._shot = False
        self._gun = DefaultGun()
        self._gun.set_collision_type(collision_type[CollisionType.EnemyBullet])
        self._gun.set_color('red')
        self._visible_player = False

    def update(self, delta: float):
        self._gun.update(delta)
        # пускает луч от себя к игроку, чтобы проверить виден ли игрок
        RayManager.instance().ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
        if self._visible_player:
            v = GameManager.instance().get_player_pos()
            v = [v[0] - self.pos[0], v[1] - self.pos[1]]
            self.body.angle = math.atan2(v[1], v[0])
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            self._gun.shot([self.pos[0] + 30 * dx, self.pos[1] + 30 * dy],
                           [dx * 500, dy * 500])
            self._visible_player = False
        if self.life <= 0:
            GameManager.instance().remove_actor(self)

    def call_back(self, actor):
        # проверят если луч столкнулся с игроком, то игрок виден
        if isinstance(actor, Player):
            self._visible_player = True
        if actor == self or isinstance(actor, Bullet):
            return True
        return False

    def collision(self, actor=None):
        if isinstance(actor, Bullet):
            self.life -= 1
        return True
