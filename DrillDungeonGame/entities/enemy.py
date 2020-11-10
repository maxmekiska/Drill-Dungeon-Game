from __future__ import annotations

from .entity import Entity


class Enemy(Entity):
    def __init__(self, sprite_image: str, sprite_scale: float, pos_x: int, pos_y: int, speed: int = 1) -> None:
        super().__init__(sprite_image, sprite_scale, pos_x, pos_y, speed)
