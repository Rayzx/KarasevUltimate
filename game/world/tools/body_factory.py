from game.world.actor.actors import Actor
from game.world.actor.data_actor import Structure
from game.world.actor.items import Heal, Boost
from game.world.actor.player import Player
from game.world.actor.enemies import StupidEnemy
from game.world.actor.environment import Wall


class Factory:

    def __init__(self, world):
        self._world = world

    def create(self):
        pass

    def create_player(self) -> Player:
        return Player(1000, 10000)


class BodyFactory(Factory):

    def __init__(self, world):
        super().__init__(world)
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


class DebugFactory(Factory):

    def __init__(self, world, walls_debug=False):
        super().__init__(world)
        self._walls_debug = walls_debug
        self._world = world

    def _create_environment(self):
        h = [[-1000, -5], [1000, -5], [1000, 5], [-1000, 5]]
        v = [[-5, -1000], [-5, 1000], [5, 1000], [5, -1000]]
        h2 = [[-2000, -5], [2000, -5], [2000, 5], [-2000, 5]]
        v2 = [[-5, -2000], [-5, 2000], [5, 2000], [5, -2000]]

        t = Structure.Polygon

        environments = [
            Wall(-1000, 0, t=t, vertices=v),
            Wall(0, -1000, t=t, vertices=h),
            Wall(0, 1000, t=t, vertices=h),
            Wall(1000, 0, t=t, vertices=v),
            Wall(-2000, 0, t=t, vertices=v2),
            Wall(0, -2000, t=t, vertices=h2),
            Wall(0, 2000, t=t, vertices=h2),
            Wall(2000, 0, t=t, vertices=v2),
            Wall(-690.0, 700.0, Structure.Polygon,
                 Actor.center([[-295.0, -5.0], [-295.0, 5.0], [295.0, 5.0], [295.0, -5.0]])),
            Wall(-380.0, 760.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(-130.0, 840.0, Structure.Polygon,
                 Actor.center([[-255.0, -5.0], [-255.0, 5.0], [255.0, 5.0], [255.0, -5.0]])),
            Wall(120.0, 760.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(450.0, 700.0, Structure.Polygon,
                 Actor.center([[-315.0, -5.0], [-315.0, 5.0], [315.0, 5.0], [315.0, -5.0]])),
            Wall(760.0, 400.0, Structure.Polygon,
                 Actor.center([[-5.0, -285.0], [5.0, -285.0], [5.0, 285.0], [-5.0, 285.0]])),
            Wall(820.0, 120.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(260.0, 840.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(320.0, 890.0, Structure.Polygon,
                 Actor.center([[-5.0, -35.0], [5.0, -35.0], [5.0, 35.0], [-5.0, 35.0]])),
            Wall(860.0, 220.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(620.0, -80.0, Structure.Polygon,
                 Actor.center([[-5.0, -285.0], [5.0, -285.0], [5.0, 285.0], [-5.0, 285.0]])),
            Wall(810.0, -240.0, Structure.Polygon,
                 Actor.center([[-115.0, -5.0], [-115.0, 5.0], [115.0, 5.0], [115.0, -5.0]])),
            Wall(630.0, 300.0, Structure.Polygon,
                 Actor.center([[-115.0, -5.0], [-115.0, 5.0], [115.0, 5.0], [115.0, -5.0]])),
            Wall(500.0, 180.0, Structure.Polygon,
                 Actor.center([[-5.0, -105.0], [5.0, -105.0], [5.0, 105.0], [-5.0, 105.0]])),
            Wall(720.0, -490.0, Structure.Polygon,
                 Actor.center([[-5.0, -135.0], [5.0, -135.0], [5.0, 135.0], [-5.0, 135.0]])),
            Wall(720.0, -640.0, Structure.Polygon,
                 Actor.center([[-105.0, -5.0], [-105.0, 5.0], [105.0, 5.0], [105.0, -5.0]])),
            Wall(-120.0, 580.0, Structure.Polygon,
                 Actor.center([[-305.0, -5.0], [-305.0, 5.0], [305.0, 5.0], [305.0, -5.0]])),
            Wall(260.0, 460.0, Structure.Polygon,
                 Actor.center([[-5.0, -185.0], [5.0, -185.0], [5.0, 185.0], [-5.0, 185.0]])),
            Wall(-510.0, 440.0, Structure.Polygon,
                 Actor.center([[-95.0, -5.0], [-95.0, 5.0], [95.0, 5.0], [95.0, -5.0]])),
            Wall(540.0, -540.0, Structure.Polygon,
                 Actor.center([[-5.0, -225.0], [5.0, -225.0], [5.0, 225.0], [-5.0, 225.0]])),
            Wall(-420.0, 40.0, Structure.Polygon,
                 Actor.center([[-565.0, -5.0], [-565.0, 5.0], [565.0, 5.0], [565.0, -5.0]])),
            Wall(490.0, -780.0, Structure.Polygon,
                 Actor.center([[-35.0, -5.0], [-35.0, 5.0], [35.0, 5.0], [35.0, -5.0]])),
            Wall(220.0, 20.0, Structure.Polygon,
                 Actor.center([[-5.0, -105.0], [5.0, -105.0], [5.0, 105.0], [-5.0, 105.0]])),
            Wall(150.0, 120.0, Structure.Polygon,
                 Actor.center([[-55.0, -5.0], [-55.0, 5.0], [55.0, 5.0], [55.0, -5.0]])),
            Wall(220.0, -100.0, Structure.Polygon,
                 Actor.center([[-85.0, -5.0], [-85.0, 5.0], [85.0, 5.0], [85.0, -5.0]])),
            Wall(-460.0, 140.0, Structure.Polygon,
                 Actor.center([[-5.0, -45.0], [5.0, -45.0], [5.0, 45.0], [-5.0, 45.0]])),
            Wall(-40.0, -550.0, Structure.Polygon,
                 Actor.center([[-5.0, -455.0], [5.0, -455.0], [5.0, 455.0], [-5.0, 455.0]])),
            Wall(80.0, -810.0, Structure.Polygon,
                 Actor.center([[-5.0, -95.0], [5.0, -95.0], [5.0, 95.0], [-5.0, 95.0]])),
            Wall(180.0, -700.0, Structure.Polygon,
                 Actor.center([[-145.0, -5.0], [-145.0, 5.0], [145.0, 5.0], [145.0, -5.0]])),
            Wall(260.0, -810.0, Structure.Polygon,
                 Actor.center([[-5.0, -95.0], [5.0, -95.0], [5.0, 95.0], [-5.0, 95.0]])),
            Wall(210.0, -320.0, Structure.Polygon,
                 Actor.center([[-175.0, -5.0], [-175.0, 5.0], [175.0, 5.0], [175.0, -5.0]])),
            Wall(60.0, 280.0, Structure.Polygon,
                 Actor.center([[-185.0, -5.0], [-185.0, 5.0], [185.0, 5.0], [185.0, -5.0]])),
            Wall(-120.0, 190.0, Structure.Polygon,
                 Actor.center([[-5.0, -75.0], [5.0, -75.0], [5.0, 75.0], [-5.0, 75.0]])),
            Wall(340.0, -680.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(-620.0, 480.0, Structure.Polygon,
                 Actor.center([[-5.0, -85.0], [5.0, -85.0], [5.0, 85.0], [-5.0, 85.0]])),
            Wall(-690.0, 360.0, Structure.Polygon,
                 Actor.center([[-95.0, -5.0], [-95.0, 5.0], [95.0, 5.0], [95.0, -5.0]])),
            Wall(-120.0, 670.0, Structure.Polygon,
                 Actor.center([[-5.0, -75.0], [5.0, -75.0], [5.0, 75.0], [-5.0, 75.0]])),
            Wall(10.0, -100.0, Structure.Polygon,
                 Actor.center([[-35.0, -5.0], [-35.0, 5.0], [35.0, 5.0], [35.0, -5.0]])),
        ]

        self._world.add_actor(environments)
        v = [[-5, 5], [5, 5], [5, -5], [-5, -5]]
        environments = []

        if self._walls_debug:
            for i in range(-50, 50):
                for u in range(-50, 50):
                    environments.append(Wall(20 * i, 20 * u, t=t, vertices=v))
        for w in environments:
            self._world.add_actor(w)

    def create(self):
        self._create_environment()


class DemoFactory(Factory):

    def __init__(self, world):
        super().__init__(world)
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
        environments = [
            Wall(-690.0, 700.0, Structure.Polygon,
                 Actor.center([[-295.0, -5.0], [-295.0, 5.0], [295.0, 5.0], [295.0, -5.0]])),
            Wall(-380.0, 760.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(-130.0, 840.0, Structure.Polygon,
                 Actor.center([[-255.0, -5.0], [-255.0, 5.0], [255.0, 5.0], [255.0, -5.0]])),
            Wall(120.0, 760.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(450.0, 700.0, Structure.Polygon,
                 Actor.center([[-315.0, -5.0], [-315.0, 5.0], [315.0, 5.0], [315.0, -5.0]])),
            Wall(760.0, 400.0, Structure.Polygon,
                 Actor.center([[-5.0, -285.0], [5.0, -285.0], [5.0, 285.0], [-5.0, 285.0]])),
            Wall(820.0, 120.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(260.0, 840.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(320.0, 890.0, Structure.Polygon,
                 Actor.center([[-5.0, -35.0], [5.0, -35.0], [5.0, 35.0], [-5.0, 35.0]])),
            Wall(860.0, 220.0, Structure.Polygon,
                 Actor.center([[-45.0, -5.0], [-45.0, 5.0], [45.0, 5.0], [45.0, -5.0]])),
            Wall(620.0, -80.0, Structure.Polygon,
                 Actor.center([[-5.0, -285.0], [5.0, -285.0], [5.0, 285.0], [-5.0, 285.0]])),
            Wall(810.0, -240.0, Structure.Polygon,
                 Actor.center([[-115.0, -5.0], [-115.0, 5.0], [115.0, 5.0], [115.0, -5.0]])),
            Wall(630.0, 300.0, Structure.Polygon,
                 Actor.center([[-115.0, -5.0], [-115.0, 5.0], [115.0, 5.0], [115.0, -5.0]])),
            Wall(500.0, 180.0, Structure.Polygon,
                 Actor.center([[-5.0, -105.0], [5.0, -105.0], [5.0, 105.0], [-5.0, 105.0]])),
            Wall(720.0, -490.0, Structure.Polygon,
                 Actor.center([[-5.0, -135.0], [5.0, -135.0], [5.0, 135.0], [-5.0, 135.0]])),
            Wall(720.0, -640.0, Structure.Polygon,
                 Actor.center([[-105.0, -5.0], [-105.0, 5.0], [105.0, 5.0], [105.0, -5.0]])),
            Wall(-120.0, 580.0, Structure.Polygon,
                 Actor.center([[-305.0, -5.0], [-305.0, 5.0], [305.0, 5.0], [305.0, -5.0]])),
            Wall(260.0, 460.0, Structure.Polygon,
                 Actor.center([[-5.0, -185.0], [5.0, -185.0], [5.0, 185.0], [-5.0, 185.0]])),
            Wall(-510.0, 440.0, Structure.Polygon,
                 Actor.center([[-95.0, -5.0], [-95.0, 5.0], [95.0, 5.0], [95.0, -5.0]])),
            Wall(540.0, -540.0, Structure.Polygon,
                 Actor.center([[-5.0, -225.0], [5.0, -225.0], [5.0, 225.0], [-5.0, 225.0]])),
            Wall(-420.0, 40.0, Structure.Polygon,
                 Actor.center([[-565.0, -5.0], [-565.0, 5.0], [565.0, 5.0], [565.0, -5.0]])),
            Wall(490.0, -780.0, Structure.Polygon,
                 Actor.center([[-35.0, -5.0], [-35.0, 5.0], [35.0, 5.0], [35.0, -5.0]])),
            Wall(220.0, 20.0, Structure.Polygon,
                 Actor.center([[-5.0, -105.0], [5.0, -105.0], [5.0, 105.0], [-5.0, 105.0]])),
            Wall(150.0, 120.0, Structure.Polygon,
                 Actor.center([[-55.0, -5.0], [-55.0, 5.0], [55.0, 5.0], [55.0, -5.0]])),
            Wall(220.0, -100.0, Structure.Polygon,
                 Actor.center([[-85.0, -5.0], [-85.0, 5.0], [85.0, 5.0], [85.0, -5.0]])),
            Wall(-460.0, 140.0, Structure.Polygon,
                 Actor.center([[-5.0, -45.0], [5.0, -45.0], [5.0, 45.0], [-5.0, 45.0]])),
            Wall(-40.0, -550.0, Structure.Polygon,
                 Actor.center([[-5.0, -455.0], [5.0, -455.0], [5.0, 455.0], [-5.0, 455.0]])),
            Wall(80.0, -810.0, Structure.Polygon,
                 Actor.center([[-5.0, -95.0], [5.0, -95.0], [5.0, 95.0], [-5.0, 95.0]])),
            Wall(180.0, -700.0, Structure.Polygon,
                 Actor.center([[-145.0, -5.0], [-145.0, 5.0], [145.0, 5.0], [145.0, -5.0]])),
            Wall(260.0, -810.0, Structure.Polygon,
                 Actor.center([[-5.0, -95.0], [5.0, -95.0], [5.0, 95.0], [-5.0, 95.0]])),
            Wall(210.0, -320.0, Structure.Polygon,
                 Actor.center([[-175.0, -5.0], [-175.0, 5.0], [175.0, 5.0], [175.0, -5.0]])),
            Wall(60.0, 280.0, Structure.Polygon,
                 Actor.center([[-185.0, -5.0], [-185.0, 5.0], [185.0, 5.0], [185.0, -5.0]])),
            Wall(-120.0, 190.0, Structure.Polygon,
                 Actor.center([[-5.0, -75.0], [5.0, -75.0], [5.0, 75.0], [-5.0, 75.0]])),
            Wall(340.0, -680.0, Structure.Polygon,
                 Actor.center([[-5.0, -65.0], [5.0, -65.0], [5.0, 65.0], [-5.0, 65.0]])),
            Wall(-620.0, 480.0, Structure.Polygon,
                 Actor.center([[-5.0, -85.0], [5.0, -85.0], [5.0, 85.0], [-5.0, 85.0]])),
            Wall(-690.0, 360.0, Structure.Polygon,
                 Actor.center([[-95.0, -5.0], [-95.0, 5.0], [95.0, 5.0], [95.0, -5.0]])),
            Wall(-120.0, 670.0, Structure.Polygon,
                 Actor.center([[-5.0, -75.0], [5.0, -75.0], [5.0, 75.0], [-5.0, 75.0]])),
            Wall(10.0, -100.0, Structure.Polygon,
                 Actor.center([[-35.0, -5.0], [-35.0, 5.0], [35.0, 5.0], [35.0, -5.0]])),
        ]
        self._world.add_actor(environments)

    def _create_actors(self):
        actors = [StupidEnemy(162.0, 760.0),
                  StupidEnemy(366.0, 900.0),
                  StupidEnemy(680.0, 592.0),
                  StupidEnemy(862.0, 176.0),
                  StupidEnemy(812.0, 620.0),
                  StupidEnemy(902.0, 604.0),
                  StupidEnemy(-576.0, 488.0),
                  StupidEnemy(-578.0, 408.0),
                  StupidEnemy(-672.0, 400.0),
                  StupidEnemy(176.0, 78.0),
                  StupidEnemy(180.0, -64.0),
                  StupidEnemy(258.0, -76.0),
                  StupidEnemy(542.0, 258.0),
                  StupidEnemy(684.0, 248.0),
                  StupidEnemy(32.0, 796.0),
                  StupidEnemy(-36.0, 778.0),
                  StupidEnemy(-58.0, 710.0),
                  StupidEnemy(-58.0, 664.0),
                  StupidEnemy(-308.0, 756.0),
                  StupidEnemy(-272.0, 736.0),
                  StupidEnemy(-248.0, 688.0),
                  StupidEnemy(-248.0, 644.0),
                  StupidEnemy(116.0, -866.0),
                  StupidEnemy(224.0, -866.0),
                  StupidEnemy(546.0, -788.0),
                  StupidEnemy(750.0, -622.0),
                  StupidEnemy(766.0, -550.0),
                  StupidEnemy(816.0, -608.0),
                  StupidEnemy(878.0, -274.0),
                  StupidEnemy(794.0, -274.0),
                  StupidEnemy(724.0, -274.0),
                  StupidEnemy(576.0, -336.0),
                  StupidEnemy(326.0, -352.0),
                  StupidEnemy(268.0, -352.0),
                  StupidEnemy(308.0, -676.0),
                  StupidEnemy(308.0, -624.0),
                  StupidEnemy(308.0, -732.0),
                  StupidEnemy(230.0, 314.0),
                  StupidEnemy(180.0, 314.0),
                  StupidEnemy(-80.0, 244.0),
                  StupidEnemy(-80.0, 192.0),
                  StupidEnemy(670.0, -86.0),
                  StupidEnemy(718.0, -124.0),
                  StupidEnemy(766.0, -170.0),
                  StupidEnemy(822.0, -196.0),
                  StupidEnemy(-502.0, 108.0),
                  StupidEnemy(-508.0, 192.0)]
        for a in actors:
            self._world.add_actor(a)

    def create(self):
        self._create_environment()
        self._create_actors()

    def create_player(self) -> Player:
        player = Player(-950, 950)
        self._world.add_actor(player)
        return player
