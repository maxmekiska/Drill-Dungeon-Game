from __future__ import annotations

from .entity import Entity


class Enemy(Entity):
    """Enemy class.
    Currently doesn't do much but will be useful to do isinstance(Enemy) to tell if the enemy is hostile."""
    def __init__(self, base_sprite: str, sprite_scale: float, pos_x: int, pos_y: int, speed: int = 1) -> None:
        super().__init__(base_sprite, sprite_scale, pos_x, pos_y, speed)
