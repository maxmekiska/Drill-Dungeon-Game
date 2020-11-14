from __future__ import annotations

from typing import Union

from ..enemy import Enemy
from ..mixins.path_finding_mixin import PathFindingMixin
from ..mixins.shooting_mixin import ShootingMixin
from ..mixins.digging_mixin import DiggingMixin


class SpaceshipEnemy(Enemy, ShootingMixin, PathFindingMixin, DiggingMixin):
    def __init__(self, center_x: int, center_y: int, vision: Union[float, int],
                 speed: Union[float, int] = 1) -> None:
        base_sprite: str = "resources/images/enemy/enemy.png"
        sprite_scale: float = 0.3
        turret_sprite = "resources/images/weapons/turret1.png"
        turret_sprite_scale = 0.2
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed)  # Init Enemy
        PathFindingMixin.__init__(self, vision)  # Init PathfindingMixin.
        ShootingMixin.__init__(self, turret_sprite, turret_sprite_scale, center_x, center_y)  # Init ShootingMixin
