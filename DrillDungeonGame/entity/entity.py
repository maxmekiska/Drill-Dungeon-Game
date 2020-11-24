from __future__ import annotations

from typing import Tuple, Union, List, Type, Iterator

from itertools import chain
import arcade
import math

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..sprite_container import SpriteContainer


class Entity(arcade.Sprite):
    """

    Instantiates this Entity.

    Methods
    -------
    get_all_children()
        Returns all children.
    hurt(damage: Union[float, int])
        Deals damage to target.
    has_line_of_sight_with(entity: Entity, blocking_sprites: arcade.SpriteList)
        Returns TRUE if line of sight is established with other entity.
    look_at(x: float, y: float)
        Set entity to face a certain position.
    set_velocity(vector: Tuple[float, float])
        Setting velocity of entity to vector provided.
    on_collision(sprite: arcade.Sprite, time: float, sprites)
        Logic when collision is detected.
    update_collision_engine(time: float, sprites: SpriteContainer)
        Handles all collisions for this entity in each loop
    setup_collision_engine(collidables: List[arcade.SpriteList])
        Appends a list of collidable sprites to check for a collision.
    stop_moving()
        Change the velocity of the entity to 0.
    draw()
        Draws entity and all children entities.
    update(time: float, sprites: SpriteContainer)
        Called every game loop iteration for each entity and updates all collision engines.

    """
    def __init__(self, base_sprite: str, sprite_scale: float,
                 center_x: Union[float, int], center_y: Union[float, int],
                 speed: Union[float, int] = 1, angle: float = 0.0,
                 current_health: float = -1, max_health: float = -1) -> None:
        """

        Parameters
        ----------
        base_sprite     :   str
            The path to the file containing the sprite for this entity.
        sprite_scale    :   float
            The scale to draw the sprite for this entity
        center_x        :   Union[float, int]
            The starting x position in the map for this entity.
        center_y        :   Union[float, int]
            The starting y position in the map for this entity.
        speed           :   Union[float, int]
            The speed that entity can move at.
        angle           :   float
            The starting angle for this entity.
        current_health  :   float
            The starting health for this entity. -1 means invincibility.
        max_health      :   float
            The maximum amount of health this entity can have. -1 means unlimited.

        """
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
        self.current_health = current_health  # The health of this entity. -1 means invincible.
        self.max_health = max_health

    def get_all_children(self) -> List[Entity]:
        """

        Returns a list of all entities that are a child to this one.

        Notes
        -----
        This is recursive and all indirect children are also present in this list (ie children of children of ...).

        Returns
        -------
        List[Entity]
            A list of all Entities that are a child to this one.

        """
        children = []
        klass = self
        for child in klass.children:
            children.append(child)
            if hasattr(child, 'get_all_children'):
                children.extend(child.get_all_children())
        # noinspection PyTypeChecker
        return children

    def hurt(self, damage: Union[float, int]) -> None:
        """

        Calling this function deals damage to the entity.

        Notes
        -----
        If the health goes below or equal to 0, the Entity is also deleted along with all children Entities.

        Parameters
        ----------
        damage: Union[float, int]
            The amount of damage to deal to this entity.

        """
        if self.current_health == -1:  # invincible. Do nothing.
            return

        self.current_health -= damage
        if self.current_health <= 0:
            for child in self.get_all_children():
                child.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

    def heal(self, amount: Union[float, int]) -> None:
        """

        Heals the entity for the amount specified up to the max_health attribute.

        Parameters
        ----------
        amount: Union[float, int]
            The amount of health to heal this entity for.

        """
        if self.current_health == -1:  # Invincible. Do nothing.
            return

        if self.current_health < self.max_health:
            self.current_health = min(self.max_health, self.current_health + amount)

    def has_line_of_sight_with(self, entity: Entity, blocking_sprites: arcade.SpriteList) -> bool:
        """

        Returns True is this class has line of site with another given entity, given a list of obstacles.

        Parameters
        ----------
        entity: Entity
            The entity to check if if this entity has line of sight with.
        blocking_sprites: arcade.SpriteList
            The sprite list containing sprites which block line of sight.

        Returns
        -------
        bool
            True if there is line of sight, False otherwise.

        """
        return arcade.has_line_of_sight(self.position, entity.position, blocking_sprites)

    def look_at(self, x: float, y: float) -> None:
        """

        Sets the entity to face towards a certain position.

        Notes
        ----
        Children angle will also be updated if maintain_parent_angle is set to true in the child class.

        See Also
        --------
        ChildEntity.update: Where the child angle is updated to match the parent.

        Parameters
        ----------
        x: float
            The x position to look at.
        y: float
            The y position to look at.

        """
        x_diff, y_diff = x - self.center_x, y - self.center_y
        angle = math.degrees(math.atan2(y_diff, x_diff))
        self.angle = angle

    def set_velocity(self, vector: Tuple[float, float]) -> None:
        """

        Sets the velocity of this entity to the corresponding vector.

        Notes
        ----
        Children velocity will also be updated if maintain_relative_position is set to True in the child class.

        See Also
        --------
        ChildEntity.update: Where the child velocity is updated to match the parent.

        Parameters
        ----------
        vector: Tuple[float, float]
            The corresponding x, y vector that this entity's velocity will be set to.

        """
        self.change_x = vector[0]
        self.change_y = vector[1]

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        """

        Override this method in subclasses to handle what entities should do when colliding.

        Parameters
        ----------
        sprite: arcade.Sprite
            The sprite that the Entity collided with.
        time: float
            The time that the collision happened.
        sprites: SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
        pass

    def update_collision_engine(self, time: float, sprites: SpriteContainer) -> None:
        """

        This is called from the entity.update() function.
        It handles all collisions for this entity in each loop.

        See Also
        --------
        on_collision: a handler which can be subclassed to handle collisions with specific sprites.

        Parameters
        ----------
        time: float
            The time that the game has been running for. We can store this to do something every x amount of time.
        sprites: SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
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
        """

        Appends a list of collidable sprites to check for a collision with each game loop iteration to the
        collision_list.

        Parameters
        ----------
        collidables: List[arcade.SpriteList]
            A list of different sprite lists to check for collisions for.

        """
        for collidable_list in collidables:
            self.collision_engine.append(arcade.PhysicsEngineSimple(self, collidable_list))
            for child in self.children:
                self.collision_engine.append(arcade.PhysicsEngineSimple(child, collidable_list))

    def stop_moving(self) -> None:
        """

        Call this to change the velocity of the entity to 0. (Stops moving)

        """
        self.set_velocity((0.0, 0.0))

    def draw(self) -> None:
        """

        Draws this Entity and all entities which are children to this one.
        In addition to this, it draws any mixins which have a draw function implemented.

        Note
        ____
        If this function is overridden in a subclass, make sure to call super().draw() at the end so that
        all children classes are drawn too.

        """
        super().draw()

        for mixin in self.__class__.__mro__:
            if hasattr(mixin, 'draw') and not issubclass(mixin, arcade.Sprite):
                mixin.draw(self)

        for child in self.children:
            child.draw()

    # noinspection PyMethodOverriding
    def update(self, time: float, delta_time: float, sprites: SpriteContainer) -> None:
        """

        This function is called every game loop iteration for each entity so it can update all collision engines.
        Furthermore, it loops over and updates every child entity to this entity. For example: the Bullet class is a
        child to the Turret class and the Turret class is a child to the Drill class The SpriteContainer only has
        reference to the root parent, so we need to update all children here.
        In addition to this, it calls the update() function in all mixin classes.

        Note
        ----
        If this function is overridden in a subclass, make sure to call super().update(time, sprites) at the end so that
        all children classes are properly updated.

        Parameters
        ----------
        time       : float
            The time that the game has been running for. We can store this to do something every x amount of time.
        delta_time : float
            The time in seconds since the last game loop iteration.
        sprites    : SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
        self.update_collision_engine(time, sprites)

        for mixin in self.__class__.__mro__:
            # Used to be issubclass(mixin, Entity), but entity inherits from arcade.Sprite now. So we also don't want
            # to pass the sprite list to the update function of arcade.Sprite as this doesn't take args. We use
            # super().update() at the end instead and now do issubclass(mixin, arcade.Sprite)
            if hasattr(mixin, 'update') and not issubclass(mixin, arcade.Sprite):
                mixin.update(self, time, delta_time, sprites)

        for child in self.children:
            # noinspection PyArgumentList
            child.update(time, delta_time, sprites)


class ChildEntity(Entity):
    """

    Defines the child entity which inherits from the Entity class.

    Methods
    -------
    get_all_parents()
        Returns list containing all entities higher in the inheritance order.
    update(time: float, sprites: SpriteContainer)
        logic to the Entity.update function so that the child can maintain position/angle with
        respect to the parent.

    """
    def __init__(self, base_sprite: str, sprite_scale: float, parent: Entity,
                 relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 maintain_relative_position: bool = True, speed: float = 1.0,
                 angle: float = 0.0, maintain_parent_angle: bool = True,
                 current_health: Union[float, int] = -1, max_health: Union[float, int] = -1) -> None:
        """

        Parameters
        ----------
        base_sprite: str
            The path to the file containing the sprite for this entity.
        sprite_scale: float
            The scale to draw the sprite for this entity
        parent: Entity
            The entity.
        relative_x: Union[float, int]
            The starting x position in the map for this entity.
        relative_y: Union[float, int]
            The starting y position in the map for this entity.
        maintain_relative_position: bool
        speed: Union[float, int]
            The speed that entity can move at.
        angle: float
            The starting angle for this entity.
        maintain_parent_angle
            Angle of parent.
        current_health: Union[float, int]:
            The starting health for this entity. -1 means invincible.
        max_health: Union[float, int]
            The maximum amount of health that this entity can have. -1 means unlimited.

        """
        super().__init__(base_sprite=base_sprite, sprite_scale=sprite_scale, center_x=parent.center_x + relative_x,
                         center_y=parent.center_y + relative_y, angle=angle, speed=speed,
                         current_health=current_health, max_health=max_health)
        self.parent = parent
        self.relative_x = relative_x
        self.relative_y = relative_y

        # Whether or not the ChildEntity will match the angle or position relative to the parent.
        self._maintain_relative_position = maintain_relative_position
        self._maintain_parent_angle = maintain_parent_angle

    @property
    def get_all_parents(self) -> List[Entity]:
        """

        Returns a list containing the Entity that is a parent to this class, as well as the parent of that parent
        and so on.

        Notes
        -----
        This is recursive and all indirect parents are also present in this list.

        Returns
        -------
        List[Entity]
            A list of all Entities that are both a parent to this class and indirect parents (parents of that parent
            and so on)

        """
        parents = []
        klass = self
        while hasattr(klass, 'parent') and klass.parent is not None:
            parents.append(klass.parent)
            klass = klass.parent
        return parents

    def update(self, time: float, delta_time: float, sprites: SpriteContainer) -> None:
        """

        Adds additional logic to the Entity.update function so that the child can maintain position/angle with
        respect to the parent.

        See Also
        --------
        Entity.update: The parent class implementation of update.

        Parameters
        ----------
        time       : float
            The time that the game has been running for. We can store this to do something every x amount of time.
        delta_time : float
            The time in seconds since the last game loop iteration.
        sprites    : SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
        if self._maintain_relative_position:
            angle = math.radians(self.parent.angle)
            point_x = self.parent.center_x + self.relative_x
            point_y = self.parent.center_y + self.relative_y
            #  Transforms point to rotate about (parent center) to origin on the axis. Perform the rotation and then
            #  translate back to the parents position.
            self.center_x = (math.cos(angle) * (point_x - self.parent.center_x)) + \
                            (math.sin(angle) * (point_y - self.parent.center_y) + self.parent.center_x)
            self.center_y = (math.sin(angle) * (point_x - self.parent.center_x)) + \
                            (math.cos(angle) * (point_y - self.parent.center_y) + self.parent.center_y)

        if self._maintain_parent_angle:
            self.angle = self.parent.angle

        super().update(time, delta_time, sprites)
