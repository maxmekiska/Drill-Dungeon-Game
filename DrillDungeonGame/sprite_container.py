from typing import List

import arcade

from .entity.entities import Drill


class SpriteContainer:
    """

    This class is used as a storage class for all sprites in our game.

    Notes
    -----
    Don't add them in DrillDungeonGame class.
    Furthermore, it allows getting all sprites of a certain category through the property methods.

    Methods
    -------
    extend(other)
        Defines additional behaviour of the class.
    all()
        Returns a list containing all SpriteLists.

    """
    def __init__(self, drill: Drill, border_wall_list: arcade.SpriteList, shop_list: arcade.SpriteList,
                 explosion_list: arcade.SpriteList, entity_list: arcade.SpriteList, drill_list: arcade.SpriteList,
                 enemy_list: arcade.SpriteList, bullet_list: arcade.SpriteList,
                 all_blocks_list: arcade.SpriteList, destructible_blocks_list: arcade.SpriteList,
                 indestructible_blocks_list: arcade.SpriteList) -> None:
        """

        Parameters
        ----------
        drill                       : Entity
            The drill (player).
        border_wall_list            : arcade.SpriteList
            List containing all border blocks.
        shop_list                   : arcade.SpriteList
            List containing all shops on the map.
        explosion_list              : arcade.SpriteList
            List containing all explosion elements.
        entity_list                 : arcade.SpriteList
            List containing all entities on map.
        drill_list                  : arcade.SpriteList
            List containing drill on map.
        enemy_list                  : arcade.SpriteList
            List containing all enemies on the map.
        bullet_list                 : arcade.SpriteList
            List containing all bullets on map.
        all_blocks_list             : arcade.SpriteList
            List containing all blocks on the map.
        destructible_blocks_list    : arcade.SpriteList
            List containing all objects that are destructible on the map.
        indestructible_blocks_list  : arcade.SpriteList
            List containing all objects that cannot be destructed on the map.

        """
        self.border_wall_list = border_wall_list
        self.shop_list = shop_list
        self.explosion_list = explosion_list
        self.entity_list = entity_list

        # the drill_list only contains the base_sprite and the turret_sprite. It was used in collide with bullet
        self.drill_list = drill_list
        # the enemy_list contains all enemies. It was also used in collide with bullet.
        self.enemy_list = enemy_list

        self.bullet_list = bullet_list
        self.drill = drill

        # NOTE: The following sprite lists contain duplicates of sprites that will exist in sprite lists detailed above.
        self.all_blocks_list = all_blocks_list
        self.destructible_blocks_list = destructible_blocks_list
        self.indestructible_blocks_list = indestructible_blocks_list

    def extend(self, other):
        """

        Defines addition behaviour of the class.

        Notes
        -----
        Should return new instance of SpriteContainer
        with the two sprite lists added up basically

        Parameters
        ----------
        other: entity

        Returns
        -------
        entity
            New instance of sprite container.

        """
        self.border_wall_list.extend(other.border_wall_list)
        self.explosion_list.extend(other.explosion_list)
        self.entity_list.extend(other.entity_list)
        self.bullet_list.extend(other.bullet_list)

        self.all_blocks_list.extend(other.all_blocks_list)
        self.destructible_blocks_list.extend(other.destructible_blocks_list)
        self.indestructible_blocks_list.extend(other.indestructible_blocks_list)

    @property
    def all(self) -> List[arcade.SpriteList]:
        """

        Returns a list containing all SpriteLists.

        Notes
        -----
        This doesn't include sprite_lists which contain duplicated
        sprites from other sprite lists.

        Returns
        -------
        List[arcade.SpriteList]
            Returns all sprite lists.

        """
        return [self.drill, self.all_blocks_list, self.explosion_list, self.entity_list, self.bullet_list]
