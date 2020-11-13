from typing import List, TYPE_CHECKING

import arcade

from DrillDungeonGame.entity.entities.drill import Drill


class SpriteContainer:
    """This class is used as a storage class for all sprites in our game. Don't add them in DrillDungeonGame class.
    Furthermore, it allows getting all sprites of a certain category through the property methods."""
    def __init__(self, drill: Drill, dirt_list: arcade.SpriteList, border_wall_list: arcade.SpriteList,
                 coal_list: arcade.SpriteList, gold_list: arcade.SpriteList, explosion_list: arcade.SpriteList,
                 entity_list: arcade.SpriteList, bullet_list: arcade.SpriteList, all_blocks_list: arcade.SpriteList,
                 destructible_blocks_list: arcade.SpriteList, indestructible_blocks_list: arcade.SpriteList) -> None:
        self.dirt_list = dirt_list
        self.border_wall_list = border_wall_list
        self.coal_list = coal_list
        self.gold_list = gold_list
        self.explosion_list = explosion_list
        self.entity_list = entity_list
        self.bullet_list = bullet_list

        # NOTE: The following sprite lists contain duplicates of sprites that will exist in sprite lists detailed above.
        self.drill = drill
        self.all_blocks_list = all_blocks_list
        self.destructible_blocks_list = destructible_blocks_list
        self.indestructible_blocks_list = indestructible_blocks_list

    @property
    def all(self) -> List[arcade.SpriteList]:
        """Returns a list containing all SpriteLists. This doesn't include sprite_lists which contain duplicated
        sprites from other sprite lists."""
        return [self.drill, self.dirt_list, self.border_wall_list, self.coal_list,
                self.gold_list, self.explosion_list, self.entity_list, self.bullet_list]
