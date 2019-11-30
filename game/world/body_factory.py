from game.world.actor.dynamics import Barrel, Player
from game.world.actor.statics import Wall
import resources.resource_manager as rm


class BodyFactory:

    def __init__(self, world):
        self._world = world

    def _create_environment(self):
        vertices = [(-100, -100), (-100, 100), (100, 100), (100, -100)]
        t = rm.Image_Name.Polygon
        walls = [Wall(200, 500, t=t, vertices=vertices),
                 Wall(0, 100, t=t, vertices=vertices),
                 Wall(0, 300, t=t, vertices=vertices),
                 Wall(400, 100, t=t, vertices=vertices),
                 Wall(400, 300, t=t, vertices=vertices),
                 Wall(200, -100, t=t, vertices=vertices),
                 ]
        for w in walls:
            self._world.add_actor(w)

    def _create_actors(self):
        actors = [
            Barrel(200, 100, rm.Image_Name.Circle, 10, 'blue'),
            Barrel(200, 200, rm.Image_Name.Circle, 20, 'blue'),
            Barrel(200, 300, rm.Image_Name.Circle, 30, 'blue')
        ]
        for a in actors:
            self._world.add_actor(a)

    def create(self):
        self._create_actors()
        self._create_environment()

    def create_player(self, x, y) -> Player:
        player = Player(x, y)
        self._world.add(player.body, player.shape)
        self._world.append(player)
        return player

