import math
import random

from game.world.actor.actors import Dynamic
from game.world.actor.bullet import Bullet
from game.world.actor.data_actor import collision_type, Structure, CollisionType
from game.world.actor.player import Player
from game.world.actor.gun import DefaultGun, TripleGun, Explosion
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
        self._gun = DefaultGun(0)
        self._gun.set_collision_type(collision_type[CollisionType.EnemyBullet])
        self._gun.set_color('red')
        self._visible_player = False

        self._gun.reload_time = 0.3

    def update(self, delta: float):
        self._gun.update(delta)
        # пускает луч от себя к игроку, чтобы проверить виден ли игрок
        RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
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


class LevelBoss0(Dynamic):

    def __init__(self, x=0, y=0):
        super().__init__(x=x,
                         y=y,
                         t=Structure.Circle,
                         vertices=50,
                         color='grey')

        self._time = 0

        self.shape.elasticity = 1
        self.shape.friction = 5
        self.shape.collision_type = collision_type[CollisionType.Enemy]

        self.body.velocity_func = Dynamic.speed_update_body
        self.body.velocity = (0, 0)
        self.body.angular_velocity = 0

        self._gun = None
        self._set_gun(DefaultGun(1))
        self._visible_player = False
        self._num_shot = 0
        self._reload_time = 0
        self._num_task = 0
        self.life = 1000

        self._logic = [self._logic1, self._logic2, self._logic3]

    def _set_gun(self, gun):
        self._gun = gun
        self._gun.set_collision_type(collision_type[CollisionType.EnemyBullet])
        self._gun.set_color('red')
        self._gun.reload_time = 0.3
        return gun

    def _logic1(self, delta):
        self._gun.update(delta)
        if self._num_shot >= 5:
            self._reload_time += delta
            if self._reload_time > 2:
                self._num_shot = 0
                self._reload_time = 0
            else:
                RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
                if self._visible_player:
                    v = self.pos - GameManager.instance().get_player_pos()
                    self.move(-v.normalized())
                    self._visible_player = False
                return
        # пускает луч от себя к игроку, чтобы проверить виден ли игрок
        RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
        if self._visible_player:
            v = GameManager.instance().get_player_pos()
            v = [v[0] - self.pos[0], v[1] - self.pos[1]]
            self.body.angle = math.atan2(v[1], v[0])
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            if self._gun.shot([self.pos[0] + 30 * dx, self.pos[1] + 30 * dy],
                              [dx * 500, dy * 500]):
                self._visible_player = False
                self._num_shot += 1

    def _logic2(self, delta):
        self._gun.update(delta)
        if self._num_shot >= 3:
            self._reload_time += delta
            if self._reload_time > 2:
                self._num_shot = 0
                self._reload_time = 0
            else:
                RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
                if self._visible_player:
                    v = self.pos - GameManager.instance().get_player_pos()
                    self.move(-v.normalized())
                    self._visible_player = False
                return
        # пускает луч от себя к игроку, чтобы проверить виден ли игрок
        RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
        if self._visible_player:
            v = GameManager.instance().get_player_pos()
            v = [v[0] - self.pos[0], v[1] - self.pos[1]]
            self.body.angle = math.atan2(v[1], v[0])
            dx = math.cos(self.body.angle)
            dy = math.sin(self.body.angle)
            if self._gun.shot([self.pos[0] + 30 * dx, self.pos[1] + 30 * dy],
                              [dx * 500, dy * 500]):
                self._visible_player = False
                self._num_shot += 1

    def _logic3(self, delta):
        self._gun.update(delta)
        if self._num_shot >= 20:
            self._reload_time += delta
            if self._reload_time > 4:
                self._num_shot = 0
                self._reload_time = 0
            else:
                return
        RayManager.ray_cast(self.pos, GameManager.instance().get_player_pos(), self.call_back)
        if self._visible_player:
            if self._gun.shot([self.pos[0], self.pos[1]],
                              [math.cos(self._num_shot / 10) * 500, math.sin(self._num_shot / 10) * 500]):
                self._num_shot += 1
            self._visible_player = False

    def update(self, delta: float):
        self._time += delta
        if self._time >= 5:
            self._time = 0
            self._num_task = random.randint(0, 2)
            if self._num_task == 0:
                self._set_gun(DefaultGun(random.randint(0, 1)))
            if self._num_task == 1:
                self._set_gun(TripleGun(random.randint(0, 1)))
                self._gun.reload_time = 0.5
            if self._num_task == 2:
                self._set_gun(Explosion(ct=collision_type[CollisionType.EnemyBullet]))
                self._gun.reload_time = 0.1
        self._logic[self._num_task](delta)
        if self.life <= 0:
            GameManager.instance().remove_boss(self)

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

    def move(self, direction):
        self.body.velocity = 50 * direction
