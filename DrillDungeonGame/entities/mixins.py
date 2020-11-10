from __future__ import annotations
import typing
import arcade
import math

from .entity import Entity


# TODO MOVE THIS TO utility.py
def is_near(a_x, a_y, b_x, b_y):
    """Function used in pathfinding. Returns True if entity is in range of a certain point. Else False"""
    distance = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2))
    return True if distance < 15 else False


class PathFindingMixin:
    body: arcade.Sprite
    position: typing.Tuple[float, float]
    pos_x: float
    pos_y: float
    speed: float
    path: typing.List[typing.Tuple[float, float]] = []
    path_index: int = 0
    sprite_list: arcade.SpriteList
    update_velocity: typing.Callable[[typing.Tuple[float, float]], None]
    vision: typing.Union[float, int]

    def has_line_of_sight_with(self, entity: Entity, blocking_sprites: arcade.SpriteList):
        return arcade.has_line_of_sight(self.position, entity.position, blocking_sprites)

    def path_to_entity(self, entity: Entity, blocking_sprites: arcade.SpriteList,
                       diagonal_movement: bool = True) -> None:
        return self.path_to_position(entity.pos_x, entity.pos_y, blocking_sprites, diagonal_movement)

    def path_to_position(self, x: float, y: float, blocking_sprites: arcade.SpriteList,
                         diagonal_movement: bool = True) -> None:
        sprite_size_estimate = int((self.body.height + self.body.width) / 2)
        barrier_list = arcade.AStarBarrierList(self.body, blocking_sprites, sprite_size_estimate,
                                               int(self.pos_x - self.vision), int(self.pos_x + self.vision),
                                               int(self.pos_y - self.vision), int(self.pos_y + self.vision))
        path = arcade.astar_calculate_path((self.pos_x, self.pos_y), (x, y), barrier_list,
                                           diagonal_movement=diagonal_movement)

        self.path = path if path is not None else []
        self.path_index = 0

    def look_at(self, x: float, y: float) -> None:
        """Sets the entities to face towards a certain position."""
        x_diff, y_diff = x - self.pos_x, y - self.pos_y
        self.body.angle = math.degrees(math.atan2(y_diff, x_diff)) - 90

    def _move_towards(self, x: typing.Union[float, int], y: typing.Union[float, int]) -> None:
        """Moves towards the position specified"""
        x_diff, y_diff = x - self.pos_x, y - self.pos_y
        component = math.degrees(math.atan2(y_diff, x_diff)) - 90
        x_vector = self.speed * math.cos(component)
        y_vector = self.speed * math.sin(component)
        self.update_velocity((x_vector, y_vector))

    def update(self) -> None:
        """If there is an element in the path, work on moving towards it"""
        while len(self.path) > self.path_index and \
                is_near(self.pos_x, self.pos_y, self.path[self.path_index][0], self.path[self.path_index][1]) is True:
            self.path_index += 1

        if len(self.path) > self.path_index:
            destination_x, destination_y = self.path[self.path_index][0], self.path[self.path_index][1]
            self.look_at(destination_x, destination_y)
            self._move_towards(destination_x, destination_y)
        # else do nothing. Don't move
