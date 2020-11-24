from __future__ import annotations

from typing import Union

from ..enemy import Enemy
from ..mixins import PathFindingMixin, ShootingMixin


class GreenAlienEnemy(Enemy, PathFindingMixin):
    """

    Represents a green alien (the enemy) attacking the player.

    """
    def __init__(self, center_x: int, center_y: int, vision: Union[float, int],
                 speed: Union[float, int] = 1) -> None:
        """

        Parameters
        ----------
        center_x    :   int
            The starting x position in the map for this entity.
        center_y    :   int
            The starting y position in the map for this entity.
        vision      :   Union[float, int]
            The vision/detection field of the enemy.
        speed       :   Union[float, int]
            The movement speed of the enemy.

        """
        base_sprite: str = "resources/images/enemy/enemy.png"
        sprite_scale: float = 0.3
        turret_sprite = "resources/images/weapons/turret1.png"
        turret_sprite_scale = 0.3
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed)
        PathFindingMixin.__init__(self, vision)

