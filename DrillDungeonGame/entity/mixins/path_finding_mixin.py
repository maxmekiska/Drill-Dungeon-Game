from __future__ import annotations
import math
from typing import Tuple, List, Union, Callable

import arcade

from ..entity import Entity
from DrillDungeonGame.utility import is_near

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...sprite_container import SpriteContainer


class PathFindingMixin:
    position: Tuple[float, float]
    center_x: float
    center_y: float
    height: int
    width: int
    speed: float
    angle: float
    path: List[Tuple[float, float]] = []
    path_index: int = 0
    sprite_list: arcade.SpriteList
    set_velocity: Callable[[Tuple[float, float]], None]
    look_at: Callable[[float, float], None]
    stop_moving: Callable[[None], None]

    def __init__(self, vision: Union[float, int]) -> None:
        self.vision = vision  # How far the path finding can see.

    def path_to_entity(self, entity: Entity, blocking_sprites: arcade.SpriteList,
                       diagonal_movement: bool = True) -> None:
        """Used as a shortcut to path_to_position. Automatically unpacks entity coordinates."""
        return self.path_to_position(entity.center_x, entity.center_y, blocking_sprites, diagonal_movement)

    def path_to_position(self, x: float, y: float, blocking_sprites: arcade.SpriteList,
                         diagonal_movement: bool = True) -> None:
        """Returns a list of tuples[float, float], consisting of x, y coordinates to path find to the position."""
        sprite_size_estimate = int((self.height + self.width) / 2)
        barrier_list = arcade.AStarBarrierList(self, blocking_sprites, sprite_size_estimate,
                                               int(self.center_x - self.vision), int(self.center_x + self.vision),
                                               int(self.center_y - self.vision), int(self.center_y + self.vision))
        path = arcade.astar_calculate_path((self.center_x, self.center_y), (x, y), barrier_list,
                                           diagonal_movement=diagonal_movement)

        self.path = path if path is not None else []
        self.path_index = 0

    def move_towards(self, x: Union[float, int], y: Union[float, int], use_angle: bool = False) -> None:
        """Moves towards the position specified. If use_angle is true, it saves some computation of having to
        recalculate the vector component."""
        if use_angle:
            component = math.radians(self.angle)
        else:
            x_diff, y_diff = x - self.center_x, y - self.center_y
            component = math.atan2(y_diff, x_diff)
        x_vector = self.speed * math.cos(component)
        y_vector = self.speed * math.sin(component)
        self.set_velocity((x_vector, y_vector))

    def update(self, time: float, sprites: SpriteContainer) -> None:
        """If there is an element in the path, work on moving towards it"""
        while len(self.path) > self.path_index and \
                (is_near(self.center_x, self.center_y, self.path[self.path_index][0],
                         self.path[self.path_index][1], distance=20) is True):
            self.path_index += 1

        if len(self.path) > self.path_index:
            destination_x, destination_y = self.path[self.path_index][0], self.path[self.path_index][1]
            self.move_towards(destination_x, destination_y)
            self.look_at(destination_x, destination_y)
        else:
            self.stop_moving()
        # else do nothing. Don't move
