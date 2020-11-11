from __future__ import annotations
import typing

from ..enemy import Enemy
from ..mixins import PathFindingMixin, ShootingMixin, DiggingMixin


class SpaceshipEnemy(Enemy, ShootingMixin, PathFindingMixin, DiggingMixin):
    def __init__(self, center_x: int, center_y: int, vision: typing.Union[float, int],
                 speed: typing.Union[float, int] = 1) -> None:
        base_sprite: str = "resources/images/enemy/enemy.png"
        sprite_scale: float = 0.3
        turret_sprite = "resources/images/weapons/turret1.png"
        turret_sprite_scale = 0.3
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed)
        PathFindingMixin.__init__(self, vision)
        ShootingMixin.__init__(self, turret_sprite, turret_sprite_scale, center_x, center_y)
