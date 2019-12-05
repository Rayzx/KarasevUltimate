from game.world.actor.dynamics import Barrel, Player
from game.world.actor.statics import Wall
import resources.resource_manager as rm


class BodyFactory:

    def __init__(self, world):
        self._world = world

    def _create_environment(self):
        h = [(-1000, -5), (1000, -5), (1000, 5), (-1000, 5)]
        v = [(-5, -1000), (-5, 1000), (5, 1000), (5, -1000)]
        t = rm.Image_Name.Polygon
        walls = [Wall(-1000, 0, t=t, vertices=v),
                 Wall(0, -1000, t=t, vertices=h),
                 Wall(0, 1000, t=t, vertices=h),
                 Wall(1000, 0, t=t, vertices=v),
                 ]

        for w in walls:
            self._world.add_actor(w)

        h = [(-2000, -5), (2000, -5), (2000, 5), (-2000, 5)]
        v = [(-5, -2000), (-5, 2000), (5, 2000), (5, -2000)]
        walls = [Wall(-2000, 0, t=t, vertices=v),
                 Wall(0, -2000, t=t, vertices=h),
                 Wall(0, 2000, t=t, vertices=h),
                 Wall(2000, 0, t=t, vertices=v),
                 ]

        for w in walls:
            self._world.add_actor(w)

    def _create_actors(self):
        actors=[]
        for i in range(5):
            for u in range(5):
                actors.append(Barrel(200*(i-2.5), 200*(u-2.5)+50+10*i, rm.Image_Name.Circle, i+u+10, 'blue'))
        for a in actors:
            self._world.add_actor(a)

    def create(self):
        self._create_actors()
        self._create_environment()

    def create_player(self) -> Player:
        player = Player(0, 0)
        self._world.add_actor(player)
        return player
