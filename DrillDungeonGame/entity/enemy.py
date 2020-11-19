from __future__ import annotations

from typing import Union

from .entity import Entity


class Enemy(Entity):
    """Enemy class.
    Currently doesn't do much but will be useful to do isinstance(Enemy) to tell if the enemy is hostile."""
    def __init__(self, base_sprite: str, sprite_scale: float, center_x: int, center_y: int,
                 speed: Union[float, int] = 1, angle: float = 0.0, health: Union[float, int] = -1) -> None:
        super().__init__(base_sprite=base_sprite, sprite_scale=sprite_scale, center_x=center_x, center_y=center_y,
                         speed=speed, angle=angle, health=health)
