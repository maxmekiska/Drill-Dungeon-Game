"""
Module to create drill and control its specifications
such as speed.
"""
from __future__ import annotations
import typing

import arcade


class Entity:
    """
    Parameters
    ----------
    base_sprite: str
        The file path to the sprite image to load the entities with.
    sprite_scale: float
        The scale to draw the sprite at.
    pos_x: int
        The starting x position of the entities.
    pos_y: int
        The starting y position of the entities.
    speed: int
        The speed to move the entities at.
    """
    def __init__(self, base_sprite: str, sprite_scale: float, pos_x: int, pos_y: int,
                 speed: typing.Union[float, int] = 1) -> None:
        # TODO Make drill class extend from this.
        self.body = arcade.Sprite(base_sprite, sprite_scale)
        self.body.center_x = pos_x
        self.body.center_y = pos_y

        self.sprite_list = arcade.SpriteList()  # The components making up this entity. Could use multiple sprites..
        self.sprite_list.append(self.body)

        self.speed = speed
        self.physics_engines = []

        # The enemies can be moved by appending a tuple of two floats (x, y) coordinates.
        # When arriving at the first tuple, the position will be popped off the list and it will move to the next.
        self.path = []

    @property
    def position(self) -> typing.Tuple[float, float]:
        return self.body.position

    @property
    def pos_x(self) -> float:
        return self.body.center_x

    @pos_x.setter
    def pos_x(self, x: float) -> None:
        self.body.center_x = x

    @property
    def pos_y(self) -> float:
        return self.body.center_y

    @pos_y.setter
    def pos_y(self, y: float) -> None:
        self.body.center_y = y

    @property
    def x_velocity(self) -> float:
        return self.body.change_x

    @x_velocity.setter
    def x_velocity(self, x_velocity: float) -> None:
        for sprite in self.sprite_list:
            sprite.change_x = x_velocity

    @property
    def y_velocity(self) -> float:
        return self.body.change_x

    @y_velocity.setter
    def y_velocity(self, y_velocity: float) -> None:
        for sprite in self.sprite_list:
            sprite.change_x = y_velocity

    def update_velocity(self, vector: typing.Tuple[float, float]) -> None:
        for sprite in self.sprite_list:
            sprite.center_x += vector[0]
            sprite.center_y += vector[1]

    @property
    def angle(self) -> float:
        return self.body.angle

    @angle.setter
    def angle(self, angle: float) -> None:
        for sprite in self.sprite_list:
            sprite.angle = angle % 360

    @property
    def top(self):
        return max(sprite.top for sprite in self.sprite_list)

    @property
    def bottom(self):
        return min(sprite.bottom for sprite in self.sprite_list)

    @property
    def left(self):
        return min(sprite.left for sprite in self.sprite_list)

    @property
    def right(self):
        return max(sprite.right for sprite in self.sprite_list)

    def update_physics_engine(self):
        for engine in self.physics_engines:
            engine.update()

    def physics_engine_setup(self, engine_wall):
        for sprite in self.sprite_list:
            self.physics_engines.append(arcade.PhysicsEngineSimple(sprite, engine_wall))

    def clear_dirt(self, dirt_wall_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, dirt_wall_list)
            for dirt in drill_hole_list:
                dirt.remove_from_sprite_lists()

    def stop_moving(self):
        for sprite in self.sprite_list:
            sprite.change_x = 0
            sprite.change_y = 0

    def draw(self):
        for item in self.sprite_list:
            item.draw()
