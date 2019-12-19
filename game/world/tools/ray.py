import math

import pymunk

from game.world.game_manager import GameManager


class RayManager:

    @staticmethod
    def ray_cast(start, end, callback):
        """
        :param start: начальная точка отрезка
        :param end: конец отрезка
        :param callback: метод обратного вызова, если возвращает True, то продолжает луч, иначе обрывает его
        """
        s = GameManager.instance().get_space().segment_query(start, end, 0,
                                                             pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS))
        for shape in s:
            if not callback(shape[0].body.data):
                return
