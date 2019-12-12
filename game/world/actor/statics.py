from game.world.actor.actors import Static, CollisionType
import resources.resource_manager as rm


class Wall(Static):

    def __init__(self, x, y, t=rm.Image_Name.Circle, vertices=10, color='orange4'):
        super().__init__(x, y, t, vertices, color)
        self.shape.elasticity = 1
        self.shape.friction = 100
        self.shape.collision_type = self.collision_type[CollisionType.Environment]

    def set_friction(self, value):
        self.shape.friction = value
        return self

    def set_elasticity(self, value):
        self.shape.elasticity = value
        return self
