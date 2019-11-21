import random as rnd


class Texture_Name:
    Circle = 0
    Rectangle = 1


class Colors:
    _colors = (
        (255, 0, 0),
        (254, 221, 0)
    )

    red = _colors[0]
    yellow = _colors[1]

    @classmethod
    def rand_color(cls):
        i = rnd.randint(0, len(cls._colors)-1)
        return cls._colors[i]


names = {
    # Texture_Name.Circle: 'resources/circle.png'
}
