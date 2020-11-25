from __future__ import annotations
import math
from typing import Tuple, List, Union, Callable

import arcade

from ..entity import Entity
from DrillDungeonGame.utility import is_near


class PathFindingMixin:
    """
    Class that enables enemies to find/attack the drill (player) if in sight.

    Methods
    -------
    path_to_entity(entity: Entity, blocking_sprites: arcade.SpriteList, diagonal_movement: bool = True)
        Automatically unpacks entity coordinates.
    path_to_position(x: float, y: float, blocking_sprites: arcade.SpriteList, diagonal_movement: bool = True)
        Stores a list of tuples[float, float] in the path attribute.
    move_towards(x: Union[float, int], y: Union[float, int], use_angle: bool = False)
        Moves towards the position specified.
    update(self, time: float, delta_time: float, sprites, block_grid)
        Checks if there exists an element in the path.
    """
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
        """
        A mixin for implementing primitive pathfinding to both an entity or position.

        Notes
        -----
        This class can't be used independently. Must be mixed in to an Entity subclass.

        Parameters
        ----------
        vision: Union[float, int]
            The distance that this entity can see.
        """
        self.vision = vision  # How far the path finding can see.

    def path_to_entity(self, entity: Entity, blocking_sprites: arcade.SpriteList,
                       diagonal_movement: bool = True) -> None:
        """
        Used as a shortcut to path_to_position. Automatically unpacks entity coordinates.

        Notes
        --------
        See also: path_to_position

        Parameters
        ----------
        entity: Entity
            The entity to path towards.
        blocking_sprites: arcade.SpriteList
            A list of sprites to avoid colliding with when calculating the path.
        diagonal_movement: bool
            Whether or not the path can include diagonal movement. Defaults to True.

        """
        return self.path_to_position(entity.center_x, entity.center_y, blocking_sprites, diagonal_movement)

    def path_to_position(self, x: float, y: float, blocking_sprites: arcade.SpriteList,
                         diagonal_movement: bool = True) -> None:
        """
        Stores a list of tuples[float, float] in the path attribute, consisting of x, y coordinates of the path
        required to pathfind to the position specified.

        Parameters
        ----------
        x: float
            The x position on the map to try to pathfind to.
        y: float
            The y position on the map to try to pathfind to.
        blocking_sprites: arcade.SpriteList
            A list of sprites to avoid colliding with when calculating the path.
        diagonal_movement: bool
            Whether or not the path can include diagonal movement. Defaults to True.
        """
        sprite_size_estimate = int((self.height + self.width) / 2)
        barrier_list = arcade.AStarBarrierList(self, blocking_sprites, sprite_size_estimate,
                                               int(self.center_x - self.vision), int(self.center_x + self.vision),
                                               int(self.center_y - self.vision), int(self.center_y + self.vision))
        path = arcade.astar_calculate_path((self.center_x, self.center_y), (x, y), barrier_list,
                                           diagonal_movement=diagonal_movement)

        self.path = path if path is not None else []
        self.path_index = 0

    def move_towards(self, x: Union[float, int], y: Union[float, int], use_angle: bool = False) -> None:
        """
        Moves towards the position specified. If use_angle is true, it saves some computation of having to
        recalculate the vector component.

        Parameters
        ----------
        x: Union[float, int]
            The x position on the map to set the vector component to work towards moving.
        y: Union[float, int]
            The y position on the map to set the vector component to work towards moving.
        use_angle: bool
            Whether or not to recalculate the angle to use when working out the vector component. If True, it will
            just use the angle stored in the angle attribute.
        """
        if use_angle:
            component = math.radians(self.angle)
        else:
            x_diff, y_diff = x - self.center_x, y - self.center_y
            component = math.atan2(y_diff, x_diff)
        x_vector = self.speed * math.cos(component)
        y_vector = self.speed * math.sin(component)
        self.set_velocity((x_vector, y_vector))

    def update(self, time: float, delta_time: float, sprites, block_grid) -> None:
        """
        This function is called every game loop iteration for each entity which implements this Mixin. Checks if
        there exists an element in the path, and if so works on moving towards it.

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
