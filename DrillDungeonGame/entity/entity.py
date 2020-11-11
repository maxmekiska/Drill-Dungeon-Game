"""
Module to create drill and control its specifications
such as speed.
"""
from __future__ import annotations
import typing

import arcade
import math

from ..utility import protect


class Entity(arcade.Sprite, metaclass=protect("draw", "update")):
    def __init__(self, base_sprite: str, sprite_scale: float, center_x: int, center_y: int,
                 speed: typing.Union[float, int] = 1, angle: float = 0.0) -> None:
        super().__init__(base_sprite, sprite_scale, center_x=center_x, center_y=center_y)
        self.angle = angle
        self.speed = speed

        self.sprite_list = arcade.SpriteList()  # The components making up this entity. Could use multiple sprites..
        self.sprite_list.append(self)

        # The enemies can be moved by appending a tuple of two floats (x, y) coordinates.
        # When arriving at the first tuple, the position will be popped off the list and it will move to the next.
        self.path = []

    def has_line_of_sight_with(self, entity: Entity, blocking_sprites: arcade.SpriteList):
        """Returns True is this class has line of site with another given entity."""
        return arcade.has_line_of_sight(self.position, entity.position, blocking_sprites)

    def look_at(self, x: float, y: float) -> None:
        """Sets the entity to face towards a certain position."""
        x_diff, y_diff = x - self.center_x, y - self.center_y
        for sprite in self.sprite_list:
            sprite.angle = math.degrees(math.atan2(y_diff, x_diff))

    def set_velocity(self, vector: typing.Tuple[float, float]) -> None:
        for sprite in self.sprite_list:
            sprite.change_x = vector[0]
            sprite.change_y = vector[1]

    def update_physics_engine(self):
        for engine in self.physics_engines:
            engine.update()

    def physics_engine_setup(self, engine_wall):
        for sprite in self.sprite_list:
            self.physics_engines.append(arcade.PhysicsEngineSimple(sprite, engine_wall))

    def stop_moving(self):
        for sprite in self.sprite_list:
            sprite.change_x = 0
            sprite.change_y = 0

    def draw(self) -> None:
        """
        This may seem difficult to understand.. Let me explain. Given the Mixin programming structure I've used for
        entity, you are never going to be using the <Entity> class directly. It will ALWAYS be subclassed.
        The idea is that additional functionalities that entity will have will be written in MixinClasses.
        Why? Mixins and inheritance save repeating the same chunk of code a silly amount of times. This is hugely
        beneficial! Now, __mro__ stands for method resolution order. If a class inherits from multiple parent classes,
        __mro__ provides a method for Python to figure out which have priority. Example: Lets say in the following:
        `class Foo(A, B, C): pass`, all parent classes have a draw function implemented. How does Python know which
        draw functions gets called when you do self.draw() within Foo? Usually this would call whichever
        is first in the inheritance list. In this case, that would be A.draw() that would get priority.
        In our case, we could have multiple Mixins extending class functionality. One for Shooting,
        and maybe maybe having a pet following the enemy. We need to call the draw method to draw the bullet and the
        pet, but in two different classes and with a single method available in any subclass of Entity. This normal
        order isn't suited for our needs and provides means to call the draw method in ALL parent classes of any
        given subclass of this (Entity) class. That's what this does...
        Also: The `not issubclass(parent, Entity)` prevents recursion.
        TLDR: Don't override this method in any subclass
        """
        self.sprite_list.draw()

        for parent in self.__class__.__mro__:
            if hasattr(parent, 'draw') and not issubclass(parent, Entity):
                parent.draw(self)

        super().draw()

    def update(self) -> None:
        """Read above note in draw function. Same applies"""
        for parent in self.__class__.__mro__:
            if hasattr(parent, 'update') and not issubclass(parent, Entity):
                parent.update(self)

        super().update()
