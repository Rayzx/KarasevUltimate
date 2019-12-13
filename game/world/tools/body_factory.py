from game.world.actor.data_actor import Structure
from game.world.actor.items import Heal, Boost
from game.world.actor.player import Player
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall


class BodyFactory:

    def __init__(self, world):
        self._world = world

    def _create_environment(self):
        h = [[-1000, -5], [1000, -5], [1000, 5], [-1000, 5]]
        v = [[-5, -1000], [-5, 1000], [5, 1000], [5, -1000]]
        h2 = [[-2000, -5], [2000, -5], [2000, 5], [-2000, 5]]
        v2 = [[-5, -2000], [-5, 2000], [5, 2000], [5, -2000]]

        t = Structure.Polygon
        environments = [Wall(-1000, 0, t=t, vertices=v),
                        Wall(0, -1000, t=t, vertices=h),
                        Wall(0, 1000, t=t, vertices=h),
                        Wall(1000, 0, t=t, vertices=v),
                        Wall(-2000, 0, t=t, vertices=v2),
                        Wall(0, -2000, t=t, vertices=h2),
                        Wall(0, 2000, t=t, vertices=h2),
                        Wall(2000, 0, t=t, vertices=v2)
                        ]

        self._world.add_actor(environments)
        h = [[-50, 5], [50, 5], [50, -5], [-50, -5]]
        v = [[-5, 50], [5, 50], [5, -50], [-5, -50]]
        environments = [Wall(10, 0, t=t, vertices=h),
                        Wall(0, 80, t=t, vertices=v),
                        Wall(120, -40, t=t, vertices=v),
                        Wall(10, 0, t=t, vertices=h),
                        Wall(10, -120, t=t, vertices=h)
                        ]

        for w in environments:
            self._world.add_actor(w)

    def _create_actors(self):
        actors = [Heal(-20, 10), Heal(-20, 40),
                  Boost(40, -40, 0),
                  Boost(80, -40, 0),
                  Boost(120, -40, 0),
                  Boost(40, -60, 0),
                  Boost(80, -60, 0),
                  Boost(120, -60, 0)]
        for i in range(2):
            for u in range(2):
                actors.append(
                    StupidEnemy(400 * (i - 2.5) + 50, 200 * (u - 2.5) + 50 + 10 * i + 50))
                #  actors.append(Barrel(400 * (i - 2.5), 200 * (u - 2.5) + 50 + 10 * i, rm.Image_Name.Circle, i + u + 10, 'blue'))
        for a in actors:
            self._world.add_actor(a)

    def create(self):
        self._create_environment()
        self._create_actors()

    def create_player(self) -> Player:
        player = Player(-20, -20)
        self._world.add_actor(player)
        return player
