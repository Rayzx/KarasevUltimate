from enum import Enum
from typing import Dict


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
# имена коллизия для pymunk
collision_type: Dict[CollisionType, int] = {
    CollisionType.NoCollision: int('0', 2),

    CollisionType.Player: int('000001', 2),
    CollisionType.PlayerBullet: int('111110', 2),

    CollisionType.Enemy: int('000010', 2),
    CollisionType.EnemyBullet: int('111101', 2),

    CollisionType.Environment: int('111111', 2),
    CollisionType.Bullet: int('111111', 2)
}
