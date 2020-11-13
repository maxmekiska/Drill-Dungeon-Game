from __future__ import annotations

import arcade

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...sprite_container import SpriteContainer


class DiggingMixin:
    sprite_list: arcade.SpriteList

    def update(self, time: float, sprites: SpriteContainer):
        """dirt_wall_list, the list of mineable blocks."""
        blocks_to_remove = []
        destructible_blocks = sprites.destructible_blocks_list
        for entity_sprite in self.sprite_list:
            blocks_to_remove.extend(arcade.check_for_collision_with_list(entity_sprite, destructible_blocks))

        for block in blocks_to_remove:
            if hasattr(self, 'inventory'):
                if block in sprites.coal_list:
                    block.remove_from_sprite_lists()
                    self.inventory.coal += 1  # We found coal!

                elif block in sprites.gold_list:
                    block.remove_from_sprite_lists()
                    self.inventory.gold += 1  # We found gold!

                elif block in sprites.destructible_blocks_list:
                    block.remove_from_sprite_lists()

            block.remove_from_sprite_lists()
