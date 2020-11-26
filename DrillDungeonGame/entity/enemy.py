from __future__ import annotations

from typing import Union

import arcade

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

    def draw_health_bar(self):
        """Draws a simple health bar below the enemy."""
        position_x = self.center_x  # Slightly above the sprite.
        position_y = self.center_y - 20
        width = self.width
        height = 5
        arcade.draw_rectangle_filled(
            position_x, position_y, width, height, arcade.color.WHITE
        )
        status_width = (self.current_health / self.max_health) * width
        arcade.draw_rectangle_filled(
            position_x - (width / 2 - status_width / 2),
            position_y,
            status_width,
            height,
            arcade.color.GREEN,
        )
        arcade.draw_rectangle_outline(
            position_x,
            position_y,
            width,
            height,
            arcade.color.BLACK,
            border_width=1.5
        )

    def draw(self) -> None:
        """Draws a health bar if current and max health are not infinite."""
        if self.current_health != -1 and self.max_health != -1:
            self.draw_health_bar()

        super().draw()
