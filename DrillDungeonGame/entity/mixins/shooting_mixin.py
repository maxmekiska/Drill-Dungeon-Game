from __future__ import annotations
import math

import arcade

from enum import Enum

from typing import Union, List, Type

from ..bullet import Bullet
from ..entity import Entity
from ...inventory import Inventory

from typing import Callable


class ShotType(Enum):
    SINGLE = 1
    BUCKSHOT = 2
    # Idea. Maybe 2 or 3 round burst shot?


class ShootingMixin:
    sprite_list: arcade.SpriteList
    center_x: float
    center_y: float
    speed = Union[float, int]
    has_line_of_sight_with: Callable[[Entity, arcade.SpriteList], bool]
    remove_from_sprite_lists: Callable[[None], None]
    inventory: Inventory
    angle: float
    bullet_type: Type[Bullet]
    parent: Entity
    children: List[Entity]
    firing_mode: ShotType

    def __init__(self) -> None:
        self._last_shoot_time = 0
        self._bullets_to_shoot = []  # type: List[ShotType]

    def aim(self, dest_x: float, dest_y: float) -> None:
        # Note that all of the trig functions convert between an angle and the ratio of two sides of a triangle.
        # cos, sin, and tan take an angle in radians as input and return the ratio; acos, asin, and atan take a ratio
        # as input and return an angle in radians. You only convert the angles, never the ratios.
        start_x, start_y = self.center_x, self.center_y
        x_diff, y_diff = dest_x - start_x, dest_y - start_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.angle = angle

    def shoot(self) -> None:
        self._bullets_to_shoot.append(self.firing_mode)

    # noinspection PyArgumentList
    def _shoot(self, shot_type: ShotType, sprites) -> None:
        """Shoots a bullet from the turret location. Returns the bullet that was creates so it can be appended
        to the sprite list."""
        if self.inventory is not None:
            if shot_type == ShotType.SINGLE:
                if self.inventory.ammunition > 0:
                    self.inventory.ammunition -= 1
                elif self.inventory.ammunition == -1:
                    pass
                else:
                    return

            elif shot_type == ShotType.BUCKSHOT:
                if self.inventory.ammunition > 2:
                    self.inventory.ammunition -= 3
                elif self.inventory.ammunition == -1:
                    pass
                else:
                    return

        if shot_type == ShotType.SINGLE:
            bullet = self.bullet_type(self, angle=self.angle)
            self.children.append(bullet)
            x_component = math.cos(math.radians(self.angle)) * bullet.speed
            y_component = math.sin(math.radians(self.angle)) * bullet.speed
            bullet.set_velocity((x_component, y_component))
            sprites.bullet_list.append(bullet)

        elif shot_type == ShotType.BUCKSHOT:
            bullet_middle = self.bullet_type(self, angle=self.angle)
            bullet_left = self.bullet_type(self, angle=self.angle - 10)
            bullet_right = self.bullet_type(self, angle=self.angle + 10)
            self.children.append(bullet_middle)
            self.children.append(bullet_left)
            self.children.append(bullet_right)
            # Middle
            x_component = math.cos(math.radians(self.angle)) * bullet_middle.speed
            y_component = math.sin(math.radians(self.angle)) * bullet_middle.speed
            bullet_middle.set_velocity((x_component, y_component))
            sprites.bullet_list.append(bullet_middle)
            # Left
            x_component = math.cos(math.radians(self.angle - 10)) * bullet_left.speed
            y_component = math.sin(math.radians(self.angle - 10)) * bullet_left.speed
            bullet_left.set_velocity((x_component, y_component))
            sprites.bullet_list.append(bullet_left)
            # Right
            x_component = math.cos(math.radians(self.angle + 10)) * bullet_right.speed
            y_component = math.sin(math.radians(self.angle + 10)) * bullet_right.speed
            bullet_right.set_velocity((x_component, y_component))
            sprites.bullet_list.append(bullet_right)

    def update(self, time: float, sprites) -> None:
        if len(self._bullets_to_shoot) > 0:
            shot_type = self._bullets_to_shoot.pop(0)
            self._shoot(shot_type, sprites)
