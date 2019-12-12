import resources.resource_manager as rm
from game.world.actor.player import Player
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall


class BodyFactory:

    def __init__(self, world):
        self._world = world

    def _create_environment(self):
        h = [[-1000, -5], [1000, -5], [1000, 5], [-1000, 5]]
        v = [[-5, -1000], [-5, 1000], [5, 1000], [5, -1000]]
        t = rm.Image_Name.Polygon
        walls = [Wall(-1000, 0, t=t, vertices=v),
                 Wall(0, -1000, t=t, vertices=h),
                 Wall(0, 1000, t=t, vertices=h),
                 Wall(1000, 0, t=t, vertices=v),
                 Wall(10, 0, t=t, vertices=[[-10, 10], [10, 10], [10, -10], [-10, -10]])
                 ]

        for w in walls:
            self._world.add_actor(w)

        h = [[-2000, -5], [2000, -5], [2000, 5], [-2000, 5]]
        v = [[-5, -2000], [-5, 2000], [5, 2000], [5, -2000]]
        walls = [Wall(-2000, 0, t=t, vertices=v),
                 Wall(0, -2000, t=t, vertices=h),
                 Wall(0, 2000, t=t, vertices=h),
                 Wall(2000, 0, t=t, vertices=v)
                 # Box(400, 400, t=rm.Image_Name.Circle, vertices=10, color='red')
                 ]

        for w in walls:
            self._world.add_actor(w)

    def _create_actors(self):
        actors = [StupidEnemy(30, 30)]
        for i in range(2):
            for u in range(2):
                actors.append(
                    StupidEnemy(400 * (i - 2.5)+50, 200 * (u - 2.5) + 50 + 10 * i+50))
                #  actors.append(Barrel(400 * (i - 2.5), 200 * (u - 2.5) + 50 + 10 * i, rm.Image_Name.Circle, i + u + 10, 'blue'))
        for a in actors:
            self._world.add_actor(a)

    def create(self):
        self._create_actors()
        self._create_environment()

    def create_player(self) -> Player:
        player = Player(-20, -20)
        self._world.add_actor(player)
        return player
