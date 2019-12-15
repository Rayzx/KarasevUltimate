import math

import pymunk

from game.world.game_manager import GameManager


class RayManager:

    @staticmethod
    def ray_cast(start, end, callback):
        s = GameManager.instance().get_space().segment_query(start, end, 0,
                                                             pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
        for shape in s:
            if not callback(shape[0].body.data):
                return
