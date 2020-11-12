from __future__ import annotations

from typing import List

import arcade


class DiggingMixin:
    sprite_list: arcade.SpriteList

    def dig(self, blocks_list: arcade.SpriteList):
        """dirt_wall_list, the list of mineable blocks."""
        blocks_to_remove = []
        for entity_sprite in self.sprite_list:
            blocks_to_remove.extend(arcade.check_for_collision_with_list(entity_sprite, blocks_list))

        for block in blocks_to_remove:
            block.remove_from_sprite_lists()
