import arcade

from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.entity.entities.necromancer_enemy import NecromancerEnemy
from DrillDungeonGame.map.block_grid import BlockGrid
from DrillDungeonGame.map.dungeon_generator import MapLayer
from DrillDungeonGame.sprite_container import SpriteContainer


class Level:
    def __init__(self, drill: Drill,
                 number_of_coal_patches: int = 20,
                 number_of_gold_patches: int = 20,
                 number_of_dungeons: int = 3,
                 number_of_shops: int = 20) -> None:
        """

        Set up game and initialize variables.

        Parameters
        ----------
        drill                   : Drill
            The drill instance to keep constant between levels.
        number_of_coal_patches  : int
            Number of coal patches to be created.
        number_of_gold_patches  : int
            Number of gold patches to be created.
        number_of_dungeons      : int
            Number of dungeon rooms to be created.

        """
        dirt_list = arcade.SpriteList()
        border_wall_list = arcade.SpriteList()
        shop_list = arcade.SpriteList()
        coal_list = arcade.SpriteList()
        gold_list = arcade.SpriteList()
        explosion_list = arcade.SpriteList()
        entity_list = arcade.SpriteList()
        drill_list = arcade.SpriteList()
        enemy_list = arcade.SpriteList()
        bullet_list = arcade.SpriteList()

        all_blocks_list = arcade.SpriteList()
        destructible_blocks_list = arcade.SpriteList()
        indestructible_blocks_list = arcade.SpriteList()
        self.sprites = SpriteContainer(drill=drill, dirt_list=dirt_list, border_wall_list=border_wall_list,
                                       shop_list=shop_list, coal_list=coal_list, gold_list=gold_list,
                                       explosion_list=explosion_list, entity_list=entity_list,
                                       drill_list=drill_list,
                                       enemy_list=enemy_list,
                                       bullet_list=bullet_list,
                                       all_blocks_list=all_blocks_list,
                                       destructible_blocks_list=destructible_blocks_list,
                                       indestructible_blocks_list=indestructible_blocks_list)

        # Initialize the map layer with some dungeon
        map_layer = MapLayer()
        map_layer_configuration = map_layer.get_full_map_layer_configuration(number_of_dungeons,
                                                                             number_of_coal_patches,
                                                                             number_of_gold_patches,
                                                                             number_of_shops,
                                                                             drill.center_x, drill.center_y)
        print(map_layer)
        self.block_grid = BlockGrid(map_layer_configuration, self.sprites)

        self._populate_level_with_enemies()
        # Set viewpoint boundaries - where the drill currently has scrolled to

    def _populate_level_with_enemies(self) -> None:
        enemy_one = NecromancerEnemy(300, 300, vision=200, speed=0.7)
        enemy_two = NecromancerEnemy(500, 400, vision=200, speed=0.7)
        enemy_three = NecromancerEnemy(300, 50, vision=200, speed=0.7)

        self.sprites.entity_list.append(enemy_one)
        self.sprites.entity_list.append(enemy_two)
        self.sprites.entity_list.append(enemy_three)
        self.sprites.drill_list.append(self.sprites.drill)

        self.sprites.enemy_list.append(enemy_one)
        self.sprites.enemy_list.append(enemy_two)
        self.sprites.enemy_list.append(enemy_three)

        for entity in self.sprites.entity_list:
            entity.setup_collision_engine([self.sprites.indestructible_blocks_list])

    def draw(self) -> None:
        arcade.start_render()
        self.block_grid.air_blocks.draw()
        self.sprites.dirt_list.draw()
        self.sprites.coal_list.draw()
        self.sprites.gold_list.draw()
        self.sprites.border_wall_list.draw()
        self.sprites.shop_list.draw()
        self.sprites.explosion_list.draw()

        for entity in (*self.sprites.entity_list, *self.sprites.bullet_list, self.sprites.drill):
            entity.draw()

        # for entity in self.sprites.entity_list:
        #     if entity.path:
        #         arcade.draw_line_strip(entity.path, arcade.color.BLUE, 2)

    def update(self):
        pass  # TODO currently this is all done in class: DrillDungeonGame
