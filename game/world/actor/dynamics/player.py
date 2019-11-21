from game.world.actor.actors import Dynamic


class Player(Dynamic):

    def __init__(self):
        super().__init__()

    def set_direction(self, angle: float):
        pass

    def move(self):
        pass
