from __future__ import annotations

from typing import Union

import arcade

from DrillDungeonGame.entity.entity import ChildEntity, Entity


class Bullet(ChildEntity):
    """

    A base class for different bullet types to subclass.

    Methods
    -------
    update(self, time: float, sprites)
        Update logic specific for Bullet.

    """
    def __init__(self, base_sprite: str, sprite_scale: Union[float, int], parent: Entity,
                 relative_x: Union[float, int], relative_y: Union[float, int], speed: Union[float, int],
                 angle: float = 0.0, damage: Union[float, int] = 0):
        """

        Parameters
        ----------
        base_sprite     :   str
            The path to the file containing the sprite for this entity.
        sprite_scale    :   float
            The scale to draw the sprite for this entity
        parent          :   Entity
            The entity that created fired this bullet.
        relative_x      :   Union[float, int]
            The x position, relative to the parent to spawn the bullet at.
        relative_y      :   Union[float, int]
            The y position, relative to the parent to spawn the bullet at.
        speed           :   Union[float, int]
            The speed that the bullet will travel at.
        angle           :   float
            The starting angle that the bullet should be facing when shot.
        damage          :   Union[float, int]
            The amount of that this bullet will inflict when hitting another entity with a health attribute.

        Returns
        -------
        None

        """
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, maintain_parent_angle=False, maintain_relative_position=False)
        self.damage = damage

    def update(self, time: float, sprites) -> None:
        """

        A subclass of Entity.update to implement logic specific to bullet classes.

        Notes
        -----
        Currently this involves checking for collisions with other entities and blocks and calling the on_collision
        method. We do this instead of using arcade.SimplePhysicsEngine because the engine also corrects the position
        of the entity so it doesn't collide with any other sprites. This is an issue as when a bullet is fired, it
        is already colliding with the parent entity and a potential block. The bullet would appear to phase through
        walls.

        Parameters
        ----------
        time    :   float
            The time that the game has been running for. We can store this to do something every x amount of time.
        sprites :   SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        Returns
        -------
        None

        """
        for sprite_list in (sprites.all_blocks_list, sprites.entity_list, sprites.drill_list):
            collisions = arcade.check_for_collision_with_list(self, sprite_list)

            # We might want to change this behaviour to instead loop over all collisions. The reason we only use the
            # first collision is because otherwise at the end of a gameloop, a bullet could be overlapping with up to
            # 4 (usually at most 3) blocks. One bullet could remove many blocks. We only want 1 bullet to remove 1 block
            if len(collisions) > 0:
                self.on_collision(collisions[0], time, sprites)

        super().update(time, sprites)
