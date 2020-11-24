from __future__ import annotations

from typing import Union

from .entity import Entity


class Enemy(Entity):
    """

    A subclass of Entity to represent all enemy entities. Useful for isinstance checks.

    """
    def __init__(self, base_sprite: str, sprite_scale: float,
                 center_x: int, center_y: int,
                 speed: Union[float, int] = 1, angle: float = 0.0,
                 current_health: Union[float, int] = -1, max_health: Union[float, int] = -1) -> None:
        """

        Parameters
        ----------
        base_sprite     :   str
            The path to the file containing the sprite for this entity.
        sprite_scale    :   float
            The scale to draw the sprite for this entity
        center_x        :   Union[float, int]
            The starting x position in the map for this entity.
        center_y        :   Union[float, int]
            The starting y position in the map for this entity.
        speed           :   Union[float, int]
            The speed that entity can move at.
        angle           :   float
            The starting angle for this entity.
        current_health  :   Union[float, int]
            The starting health for this entity. -1 means invincible.
        max_health      :   Union[float, int]
            The maximum amount of health this entity can have. -1 means unlimited.


        """
        super().__init__(base_sprite=base_sprite, sprite_scale=sprite_scale, center_x=center_x, center_y=center_y,
                         speed=speed, angle=angle, current_health=current_health, max_health=max_health)
