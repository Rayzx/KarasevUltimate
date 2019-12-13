from enum import Enum

import pymunk


class MyBody(pymunk.Body):
    def __init__(self, mass=0, moment=0, body_type=pymunk.Body.DYNAMIC):
        super().__init__(mass, moment, body_type)
        self._data = None

    def _set_data(self, data):
        self._data = data

    def _get_data(self):
        return self._data

    def _del_data(self):
        self._data = None

    data = property(_get_data, _set_data, _del_data)


class CollisionType(Enum):
    NoCollision = 0
    Player = 1
    PlayerBullet = 2
    Enemy = 3
    EnemyBullet = 4
    Environment = 5
    Bullet = 6


class Structure(Enum):
    Circle = 0
    Polygon = 1


class Actor:
    """
        Hello! Greetings
    """

    # имена коллизия для pymunk
    collision_type = {
        CollisionType.NoCollision: int('0', 2),

        CollisionType.Player: int('000001', 2),
        CollisionType.PlayerBullet: int('111110', 2),

        CollisionType.Enemy: int('000010', 2),
        CollisionType.EnemyBullet: int('111101', 2),

        CollisionType.Environment: int('111111', 2),
        CollisionType.Bullet: int('111111', 2)
    }

    def __init__(self, t=None, color=None):
        self._body = None
        self._shape = None
        self._structure = t
        self._color = color
        self._isVisible = True
        self._live = 1

    def update(self, delta: float):
        pass

    def collision(self, actor=None):
        return True

    def _create_body(self, position, body_type, image_type, vertices, mass=0):
        if body_type == pymunk.Body.STATIC:
            self.body = MyBody(body_type=pymunk.Body.STATIC)
        elif body_type == pymunk.Body.DYNAMIC:
            if image_type == Structure.Polygon:
                self.body = MyBody(mass, pymunk.moment_for_poly(mass, vertices, (0, 0)),
                                   body_type=pymunk.Body.DYNAMIC)
            elif image_type == Structure.Circle:
                self.body = MyBody(mass, pymunk.moment_for_circle(mass, vertices, 0, (0, 0)),
                                   body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.Vec2d(position)
        self.body.data = self

        if image_type == Structure.Polygon:
            self.shape = pymunk.Poly(self.body, vertices)
        elif image_type == Structure.Circle:
            self.shape = pymunk.Circle(self.body, vertices)

    def _get_structure(self):
        return self._structure

    def _set_structure(self, value):
        self._structure = value

    def _get_color(self):
        return self._color

    def _set_color(self, value):
        self._color = value

    def _get_body(self):
        return self._body

    def _set_body(self, value):
        self._body = value

    def _get_shape(self):
        return self._shape

    def _set_shape(self, value):
        self._shape = value

    def _get_isVisible(self):
        return self._isVisible

    def _set_isVisible(self, value):
        self._isVisible = value

    def _get_pos(self):
        return self.body.position

    def _get_life(self):
        return self._live

    def _set_life(self, value):
        self._live = value

    structure = property(_get_structure, _set_structure, doc="возращает тип изображения, которое надо отрисовать")
    body = property(_get_body, _set_body, doc="возращает pymunk тело актера")
    shape = property(_get_shape, _set_shape, doc="возращает pymunk форму актера")
    color = property(_get_color, _set_color, doc="возращает цвет")
    visible = property(_get_isVisible, _set_isVisible, doc="good thing!")
    pos = property(_get_pos)
    life = property(_get_life, _set_life)

    @staticmethod
    def center(vertices):
        if isinstance(vertices, int):
            return vertices
        x, y = 0.0, 0.0
        for v in vertices:
            x += v[0]
            y += v[1]
        x /= len(vertices)
        y /= len(vertices)
        for v in vertices:
            v[0] -= x
            v[1] -= y
        return vertices


class Static(Actor):
    def __init__(self, x, y, t, vertices, color):
        """
        :param x:
        :param y:
        :param t: тип формы
        :param vertices: масив вершин/радиус
        :param color:
        """
        super().__init__(t, color)
        # self.rect = pygame.Rect(500, 450.0, 50, 50)
        self._create_body((x, y), pymunk.Body.STATIC, t, vertices)


class Dynamic(Actor):
    max_velocity = 2000
    min_velocity = 1
    coefficient_of_friction = 3

    def __init__(self, x, y, t, vertices, color, mass=100):
        super().__init__(t, color)
        self._create_body((x, y), pymunk.Body.DYNAMIC, t, vertices, mass)
        self._stats = {
            "HP": self.life,  # health points
            "Speed": 200,  # скорость
        }

    @staticmethod
    def speed_update_body(body, gravity, damping, dt):
        if isinstance(body, pymunk.Body) and isinstance(body.velocity, pymunk.Vec2d):
            ll = body.velocity.length
            if ll == 0:
                return
            v = -body.velocity / ll
            v *= body.mass * body.shapes.pop().friction * Dynamic.coefficient_of_friction
            v += gravity
            pymunk.Body.update_velocity(body, v, damping, dt)

            if ll > Dynamic.max_velocity:
                scale = Dynamic.max_velocity / ll
                body.velocity = body.velocity * scale
            if ll < 1:
                body.velocity = body.velocity * 0


class Item(Actor):
    pass
