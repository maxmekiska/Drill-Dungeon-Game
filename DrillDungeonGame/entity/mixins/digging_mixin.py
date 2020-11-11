from __future__ import annotations
import arcade


class DiggingMixin:
    sprite_list: arcade.SpriteList

    def dig(self, dirt_wall_list: arcade.SpriteList):
        """dirt_wall_list, the list of mineable blocks."""
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, dirt_wall_list)
            for dirt in drill_hole_list:
                dirt.remove_from_sprite_lists()
