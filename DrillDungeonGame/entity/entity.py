from __future__ import annotations

from typing import Tuple, Union, List, Type, Iterator

from itertools import chain
import arcade
import math

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..sprite_container import SpriteContainer


class Entity(arcade.Sprite):
    def __init__(self, base_sprite: str, sprite_scale: float, center_x: Union[float, int], center_y: Union[float, int],
                 speed: Union[float, int] = 1, angle: float = 0.0, health: float = -1) -> None:
        super().__init__(base_sprite, sprite_scale, center_x=center_x, center_y=center_y)
        self.angle = angle
        self.speed = speed

        # Likewise if this entity has multiple sub-components. Multiple sprites making one bigger entity.
        self.children = arcade.SpriteList()

        # The enemies can be moved by appending a tuple of two floats (x, y) coordinates.
        # When arriving at the first tuple, the position will be popped off the list and it will move to the next.
        self.path = []
        self.distance_moved = 0.0  # The distance moved
        self.collision_engine = []  # Any Physics engine. One for each sprite list in sprite container.
        self.health = health  # The health of this entity. -1 means invincible.

    @property
    def parents(self) -> List[Entity]:
        """If an entity is a child to another class. And that class is a child to another. Example: Such as a bullet
        is a child to the turret, and the turret is a child to the drill. Returns all parent instances to this child."""
        parents = []
        klass = self
        while hasattr(klass, 'parent') and klass.parent is not None:
            parents.append(klass.parent)
            klass = klass.parent
        return parents

    def get_all_children(self) -> List[Entity]:
        children = []
        klass = self
        for child in klass.children:
            children.append(child)
            if hasattr(child, 'get_all_children'):
                children.extend(child.get_all_children())
        return children

    def hurt(self, damage) -> None:
        """Calling this function deals damage to the entity."""
        if self.health != -1:
            self.health -= damage
            if self.health <= 0:
                for child in self.get_all_children():
                    child.remove_from_sprite_lists()
                self.remove_from_sprite_lists()

    def has_line_of_sight_with(self, entity: Entity, blocking_sprites: arcade.SpriteList) -> bool:
        """Returns True is this class has line of site with another given entity, given a list of obstacles."""
        return arcade.has_line_of_sight(self.position, entity.position, blocking_sprites)

    def look_at(self, x: float, y: float) -> None:
        """Sets the entity to face towards a certain position."""
        x_diff, y_diff = x - self.center_x, y - self.center_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.angle = angle

    def set_velocity(self, vector: Tuple[float, float]) -> None:
        """Sets the velocity of this entity to the corresponding vector."""
        self.change_x = vector[0]
        self.change_y = vector[1]

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        """Override this method in subclasses to handle what entities should do when colliding."""
        pass

    def update_collision_engine(self, time: float, sprites: SpriteContainer) -> None:
        """This is called from the entity.update() function. It handles all collisions for this entity
        in each iteration. If there is a collision, update() returns a list of collisions. Override this function
        in any entity subclass to implement any logic."""
        if len(self.collision_engine) == 0:
            super().update()

        for engine in self.collision_engine:
            collision_list = engine.update()  # Above line just iterates over parent physics engine and children.

            for sprite in collision_list:
                self.on_collision(sprite, time, sprites)

        for child in self.children:  # type: Entity
            # Recursively updates collision engines of all children sprites.
            child.update_collision_engine(time, sprites)

    def setup_collision_engine(self, collidables: List[arcade.SpriteList]) -> None:
        """If there is any collision which needs to take place with this entity. We need to setup a physics engine
        for it. The physics engine will return a list containing other sprites it collided with when you call the
        update() function on it. We call this in the update_physics_engine() function."""
        for collidable_list in collidables:
            self.collision_engine.append(arcade.PhysicsEngineSimple(self, collidable_list))
            for child in self.children:
                self.collision_engine.append(arcade.PhysicsEngineSimple(child, collidable_list))

    def stop_moving(self) -> None:
        """Call this to change the velocity of the entity to 0. (Stops moving)"""
        self.set_velocity((0.0, 0.0))

    def draw(self) -> None:
        """
        This may seem difficult to understand.. Let me explain. Given the Mixin programming structure I've used for
        entity, you are never going to be using the <Entity> class directly. It will ALWAYS be subclassed.
        The idea is that additional functionalities that entity will have will be written in MixinClasses.
        Why? Mixins and inheritance save repeating the same chunk of code a silly amount of times.
        Now, __mro__ stands for method resolution order. If a class inherits from multiple parent classes,
        __mro__ provides a method for Python to figure out which have priority. Example: Lets say in the following:
        `class Foo(A, B, C): pass`, all parent classes have a draw function implemented. How does Python know which
        draw functions gets called when you do self.draw() within Foo? Usually this would call whichever
        is first in the inheritance list. In this case, that would be A.draw() that would get priority.
        In our case, we could have multiple Mixins extending class functionality. One for Shooting,
        and maybe maybe having a pet following the enemy. We need to call the draw method to draw the bullet and the
        pet, but in two different classes with a single method available in any subclass of Entity. This normal
        order isn't suited for our needs and this code here provides means to call the draw method in ALL parent
        classes of any given subclass of this (Entity) class. That's what this does.
        Also note: The `not issubclass(parent, arcade.Sprite)` prevents recursion.
        TLDR: If you override this method in a subclass of Entity, MAKE SURE TO CALL super().update()
        """
        super().draw()

        for mixin in self.__class__.__mro__:
            if hasattr(mixin, 'draw') and not issubclass(mixin, arcade.Sprite):
                mixin.draw(self)

        for child in self.children:
            child.draw()

    # noinspection PyMethodOverriding
    def update(self, time: float, sprites: SpriteContainer) -> None:
        """Read above note in draw function. Same applies"""
        self.update_collision_engine(time, sprites)

        for mixin in self.__class__.__mro__:
            # Used to be issubclass(mixin, Entity), but entity inherits from arcade.Sprite now. So we also don't want
            # to pass the sprite list to the update function of arcade.Sprite as this doesn't take args. We use
            # super().update() at the end instead and now do issubclass(mixin, arcade.Sprite)
            if hasattr(mixin, 'update') and not issubclass(mixin, arcade.Sprite):
                mixin.update(self, time, sprites)

        for child in self.children:
            child.update(time, sprites)


class ChildEntity(Entity):
    def __init__(self, base_sprite: str, sprite_scale: float, parent: Entity,
                 relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 maintain_relative_position: bool = True, speed: float = 1.0,
                 angle: float = 0.0, maintain_parent_angle: bool = True, health: Union[float, int] = -1) -> None:
        super().__init__(base_sprite=base_sprite, sprite_scale=sprite_scale, center_x=parent.center_x + relative_x,
                         center_y=parent.center_y + relative_y, angle=angle, speed=speed, health=health)
        self.parent = parent
        self.relative_x = relative_x
        self.relative_y = relative_y

        # Whether or not the ChildEntity will match the angle or position relative to the parent.
        self._maintain_relative_position = maintain_relative_position
        self._maintain_parent_angle = maintain_parent_angle

    @property
    def parents(self) -> List[Entity]:
        """If an entity is a child to another class. And that class is a child to another. Example: Such as a bullet
        is a child to the turret, and the turret is a child to the drill. Returns all parent instances to this child."""
        parents = []
        parent_class = self
        while hasattr(parent_class, 'parent') and parent_class.parent is not None:
            parents.append(parent_class.parent)
            parent_class = parent_class.parent
        return parents

    def draw(self) -> None:
        super().draw()

        for mixin in self.__class__.__mro__:
            if hasattr(mixin, 'draw') and not issubclass(mixin, arcade.Sprite):
                mixin.draw(self)

    def update(self, time: float, sprites: SpriteContainer) -> None:
        if self._maintain_relative_position:
            self.center_x = self.parent.center_x + self.relative_x
            self.center_y = self.parent.center_y + self.relative_y

        if self._maintain_parent_angle:
            self.angle = self.parent.angle

        super().update(time, sprites)
