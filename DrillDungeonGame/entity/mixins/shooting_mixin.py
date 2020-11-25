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
    """
    Class to change shot type.
    """
    SINGLE = 1
    BUCKSHOT = 2
    # Idea. Maybe 2 or 3 round burst shot?


class ShootingMixin:
    """
    Handles the logic related to aiming and shooting.

    Methods
    -------
    aim(dest_x: float, dest_y: float)
        Cause entity to aim at certain position.
    pull_trigger()
        Start shooting, set turret to fire at certain position.
    release_trigger()
        Stops shooting.
    shoot(shot_type: ShotType, sprites)
        Shoots bullet of certain type.
    update(time: float, delta_time: float, sprites, block_grid)
        Checks if there are bullets pending to be shot.
    """
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
    firing_rate: Union[float, int]

    def __init__(self) -> None:
        self._last_shoot_time = 0
        self._trigger_pulled = False

    def aim(self, dest_x: float, dest_y: float) -> None:
        """
        Causes the entity to aim towards a certain position.

        Parameters
        ----------
        dest_x: float
            The x position to aim at.
        dest_y: float
            The y position to aim at.
        """
        # Note that all of the trig functions convert between an angle and the ratio of two sides of a triangle.
        # cos, sin, and tan take an angle in radians as input and return the ratio; acos, asin, and atan take a ratio
        # as input and return an angle in radians. You only convert the angles, never the ratios.
        start_x, start_y = self.center_x, self.center_y
        x_diff, y_diff = dest_x - start_x, dest_y - start_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.angle = angle

    def pull_trigger(self) -> None:
        """
        Pulls the trigger and sets the turret to start shooting at the firing rate.

        Parameter
        ---------
        None
        """
        self._trigger_pulled = True

    def release_trigger(self) -> None:
        """
        Releases the trigger and the turret stops shooting.

        Parameter
        ---------
        None
        """
        self._trigger_pulled = False

    # noinspection PyArgumentList
    def shoot(self, shot_type: ShotType, sprites) -> None:
        """
        Shoots a bullet of a certain type. This does not limit how fast the turret fires according to firing rate!

        Notes
        -----
        This should only be called from the update function. Use shoot in other cases instead.

        Parameters
        ----------
        shot_type: ShotType
            The type of shooting mode to shoot the bullets in. Ie Single or buckshot.
        sprites: SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.
        """
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

    def update(self, time: float, delta_time: float, sprites, block_grid) -> None:
        """
        Checks to see if there are any bullets pending to be shot and does so.

        Notes
        -----
        Called in each game loop iteration.
         
        Parameters
        ----------
        time       : float
            The time that the game has been running for. We can store this to do something every x amount of time.
        delta_time : float
            The time in seconds since the last game loop iteration.
        sprites    : SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.
        block_grid : BlockGrid
            Reference to all blocks in the game.
        """
        if self._trigger_pulled and (time - self._last_shoot_time) > self.firing_rate:
            self._last_shoot_time = time
            self.shoot(self.firing_mode, sprites)
