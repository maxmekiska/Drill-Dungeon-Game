from __future__ import annotations
import math
import typing

import arcade

from ..entities.bullet import Bullet


class ShootingMixin:
    sprite_list: arcade.SpriteList
    center_x: float
    center_y: float
    speed = typing.Union[float, int]

    def __init__(self, turret_sprite: str, turret_sprite_scale: typing.Union[float, int],
                 center_x: int, center_y: int, ammunition: int = -1) -> None:
        self.turret = arcade.Sprite(turret_sprite, turret_sprite_scale, center_x=center_x, center_y=center_y)
        self.bullet_list = arcade.SpriteList()
        self.ammunition = ammunition

    def aim(self, dest_x: float, dest_y: float) -> None:
        # Note that all of the trig functions convert between an angle and the ratio of two sides of a triangle.
        # cos, sin, and tan take an angle in radians as input and return the ratio; acos, asin, and atan take a ratio
        # as input and return an angle in radians. You only convert the angles, never the ratios.
        start_x, start_y = self.turret.center_x, self.turret.center_y
        x_diff, y_diff = dest_x - start_x, dest_y - start_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.turret.angle = angle

    def shoot(self) -> None:
        if self.ammunition != 0:
            if self.ammunition > 0:
                self.ammunition -= 1
            bullet = Bullet(self.turret.center_x, self.turret.center_y, self.turret.angle)
            x_component = math.cos(math.radians(self.turret.angle)) * bullet.speed
            y_component = math.sin(math.radians(self.turret.angle)) * bullet.speed
            bullet.set_velocity((x_component, y_component))
            self.bullet_list.append(bullet)

    def draw(self) -> None:
        self.bullet_list.draw()
        self.turret.draw()

    def update(self) -> None:
        self.bullet_list.update()
        self.turret.center_x, self.turret.center_y = self.center_x, self.center_y
