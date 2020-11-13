from __future__ import annotations
import math

import arcade

from enum import Enum

from typing import Union, List

from ..entities.bullet import Bullet
from ..entity import Entity

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from ...sprite_container import SpriteContainer


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

    def __init__(self, turret_sprite: str, turret_sprite_scale: Union[float, int],
                 center_x: int, center_y: int, ammunition: int = -1) -> None:
        self.turret = arcade.Sprite(turret_sprite, turret_sprite_scale, center_x=center_x, center_y=center_y)
        self.ammunition = ammunition

        self._last_shoot_time = 0
        self._bullets_to_shoot = []  # type: List[ShotType]

    def aim(self, dest_x: float, dest_y: float) -> None:
        # Note that all of the trig functions convert between an angle and the ratio of two sides of a triangle.
        # cos, sin, and tan take an angle in radians as input and return the ratio; acos, asin, and atan take a ratio
        # as input and return an angle in radians. You only convert the angles, never the ratios.
        start_x, start_y = self.turret.center_x, self.turret.center_y
        x_diff, y_diff = dest_x - start_x, dest_y - start_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.turret.angle = angle

    def shoot(self, shot_type: ShotType) -> None:
        self._bullets_to_shoot.append(shot_type)

    def _shoot(self, shot_type: ShotType, sprites: SpriteContainer) -> None:
        """Shoots a bullet from the turret location. Returns the bullet that was creates so it can be appended
        to the sprite list."""
        if shot_type == ShotType.SINGLE and self.ammunition != 0:
            self.ammunition -= 1
            bullet = Bullet(self.turret.center_x, self.turret.center_y, self.turret.angle)
            x_component = math.cos(math.radians(self.turret.angle)) * bullet.speed
            y_component = math.sin(math.radians(self.turret.angle)) * bullet.speed
            bullet.set_velocity((x_component, y_component))
            sprites.entity_list.append(bullet)
            bullet.physics_engine_setup(sprites.all_blocks_list)

        elif shot_type == ShotType.BUCKSHOT and (self.ammunition == -1 or self.ammunition > 2):
            self.ammunition -= 3
            bullet_middle = Bullet(self.turret.center_x, self.turret.center_y, self.turret.angle)
            bullet_left = Bullet(self.turret.center_x, self.turret.center_y, self.turret.angle - 10)
            bullet_right = Bullet(self.turret.center_x, self.turret.center_y, self.turret.angle + 10)
            # Middle
            x_component = math.cos(math.radians(self.turret.angle)) * bullet_middle.speed
            y_component = math.sin(math.radians(self.turret.angle)) * bullet_middle.speed
            bullet_middle.set_velocity((x_component, y_component))
            sprites.entity_list.append(bullet_middle)
            # Left
            x_component = math.cos(math.radians(self.turret.angle - 10)) * bullet_left.speed
            y_component = math.sin(math.radians(self.turret.angle - 10)) * bullet_left.speed
            bullet_left.set_velocity((x_component, y_component))
            sprites.entity_list.append(bullet_left)
            # Right
            x_component = math.cos(math.radians(self.turret.angle + 10)) * bullet_right.speed
            y_component = math.sin(math.radians(self.turret.angle + 10)) * bullet_right.speed
            bullet_right.set_velocity((x_component, y_component))
            sprites.entity_list.append(bullet_right)
            for bullet in [bullet_left, bullet_middle, bullet_right]:
                bullet.physics_engine_setup(sprites.all_blocks_list)

    def draw(self) -> None:
        self.turret.draw()

    def update(self, time: float, sprites: SpriteContainer) -> None:
        self.turret.center_x, self.turret.center_y = self.center_x, self.center_y

        if self != sprites.drill and self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
            self.aim(*sprites.drill.position)

        if len(self._bullets_to_shoot) > 0:
            shot_type = self._bullets_to_shoot.pop(0)
            self._shoot(shot_type, sprites)
