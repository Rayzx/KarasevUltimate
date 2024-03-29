from game.core.data_manager import FileManager
from game.world.actor.items import *
from game.world.actor.player import Player
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall, Box, Barrel


class Factory:

    def __init__(self, world, level_name):
        self._world = world
        self._level_name = level_name

    def create(self):
        self.create_wall()
        items = {0: Nothing,
                 1: DefaultGunItem,
                 2: TripleGunItem,
                 3: ExpBulletItem,
                 4: Heal,
                 5: Boost
                 }
        for inf in FileManager.instance().get(self._level_name, 'Walls'):
            self._world.add_actor(Wall(inf[0], inf[1], Structure.Polygon, inf[2]))
        for inf in FileManager.instance().get(self._level_name, 'Box'):
            self._world.add_actor(Box(inf[0], inf[1]))
        for inf in FileManager.instance().get(self._level_name, 'Barrel'):
            self._world.add_actor(Barrel(inf[0], inf[1]))
        for inf in FileManager.instance().get(self._level_name, 'Enemy'):
            self._world.add_actor(StupidEnemy(inf[0], inf[1]))
        for inf in FileManager.instance().get(self._level_name, 'Items'):
            self._world.add_actor(items[inf[2]](inf[0], inf[1]))

        

    def create_player(self) -> Player:
        player = Player(0, 0)
        self._world.add_actor(player)
        return player

    def create_wall(self):
        """
            создате крайние стены
        """
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


class DebugFactory(Factory):

    def __init__(self, world, level_name, walls_debug=False):
        super().__init__(world, level_name)
        self._walls_debug = walls_debug

    def _create_environment(self):

        t = Structure.Polygon
        v = [[-5, 5], [5, 5], [5, -5], [-5, -5]]
        environments = []

        if self._walls_debug:
            for i in range(-50, 50):
                for u in range(-50, 50):
                    b = Box(20 * i, 20 * u, t=t, vertices=v)
                    b.shape.sensor = True
                    environments.append(b)
        for w in environments:
            self._world.add_actor(w)

    def create(self):
        self._create_environment()
        super().create()


class DemoFactory(Factory):

    def __init__(self, world, level_name):
        super().__init__(world, level_name)
