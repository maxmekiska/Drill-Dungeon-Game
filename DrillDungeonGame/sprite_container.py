from typing import List, TYPE_CHECKING

import arcade

from DrillDungeonGame.entity.entities.drill import * 


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

        self.drill = drill

        # NOTE: The following sprite lists contain duplicates of sprites that will exist in sprite lists detailed above.
        self.all_blocks_list = all_blocks_list
        self.destructible_blocks_list = destructible_blocks_list
        self.indestructible_blocks_list = indestructible_blocks_list

    def __add__(self, other):
        """
        Defines addition behaviour of the class. Should return new instance fo SpriteContainer
        with the two sprite lists added up basically
        """
        new_dirt_list = self.dirt_list.extend(other.dirt_list)
        new_border_wall_list = self.border_wall_list.extend(other.border_wall_list)
        new_coal_list = self.coal_list.extend(other.coal_list)
        new_gold_list = self.gold_list.extend(other.gold_list)
        new_explosion_list = self.explosion_list.extend(other.explosion_list)
        new_entity_list = self.entity_list.extend(other.entity_list)
        new_bullet_list = self.bullet_list.extend(other.bullet_list)

        new_drill = self.drill #unchanged

        new_all_blocks_list = self.all_blocks_list.extend(other.all_blocks_list)
        new_destructible_blocks_list = self.destructible_blocks_list.extend(other.destructible_blocks_list)
        new_indestructible_blocks_list = self.indestructible_blocks_list.extend(other.indestructible_blocks_list)
        return SpriteContainer(new_drill, new_dir_list, new_border_wall_list, new_coal_list, new_gold_list, new_explosion_list, new_entity_list, new_bullet_list, new_all_blocks_list, new_destructible_blocks_list, new_indestructible_blocks_list)



    @property
    def all(self) -> List[arcade.SpriteList]:
        """Returns a list containing all SpriteLists. This doesn't include sprite_lists which contain duplicated
        sprites from other sprite lists."""
        return [self.drill, self.dirt_list, self.border_wall_list, self.coal_list,
                self.gold_list, self.explosion_list, self.entity_list, self.bullet_list]
