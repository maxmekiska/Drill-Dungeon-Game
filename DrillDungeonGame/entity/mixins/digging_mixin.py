from __future__ import annotations

import arcade

from typing import TYPE_CHECKING, Dict

from ..entity import Entity

if TYPE_CHECKING:
    from ...sprite_container import SpriteContainer


class DiggingMixin:
    sprite_list: arcade.SpriteList
    children: Dict[str, Entity]

    def update(self, time: float, sprites: SpriteContainer) -> None:
        """This function is called every game loop iteration for each entity which implements this Mixin. Checks if this
        entity collides with any destructible block, and if so destroys it, incrementing the inventory accordingly.

        Parameters
        ----------
        time: float
            The time that the game has been running for. We can store this to do something every x amount of time.
        sprites: SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
        blocks_to_remove = []
        destructible_blocks = sprites.destructible_blocks_list
        for sprite in (self, *self.children):
            blocks_to_remove.extend(arcade.check_for_collision_with_list(sprite, destructible_blocks))

        for block in blocks_to_remove:
            if hasattr(self, 'inventory'):
                if block in sprites.coal_list:
                    self.inventory.coal += 1  # We found coal!

                elif block in sprites.gold_list:
                    self.inventory.gold += 1  # We found gold!

            block.remove_from_sprite_lists()
