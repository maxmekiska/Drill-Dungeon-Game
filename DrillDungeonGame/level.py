import arcade
import random
import numpy as np

from .entity.entities import Drill, NecromancerEnemy, FlyingEnemy, TankBoss, WizardBoss, SpaceshipEnemy, GoblinEnemy, FireEnemy
from .map import BlockGrid, MapLayer
from .sprite_container import SpriteContainer


potential_enemies = (NecromancerEnemy, FlyingEnemy, SpaceshipEnemy, GoblinEnemy, FireEnemy)
potential_bosses = (WizardBoss, TankBoss)


class Level:
    def __init__(self, drill: Drill,
                 current_level: int,
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
        border_wall_list = arcade.SpriteList()
        shop_list = arcade.SpriteList()
        explosion_list = arcade.SpriteList()
        entity_list = arcade.SpriteList()
        drill_list = arcade.SpriteList()
        enemy_list = arcade.SpriteList()
        bullet_list = arcade.SpriteList()

        all_blocks_list = arcade.SpriteList()
        destructible_blocks_list = arcade.SpriteList()
        indestructible_blocks_list = arcade.SpriteList()
        drill_down_list = arcade.SpriteList()
        self.sprites = SpriteContainer(drill=drill, border_wall_list=border_wall_list, shop_list=shop_list,
                                       explosion_list=explosion_list, entity_list=entity_list,
                                       drill_list=drill_list,
                                       enemy_list=enemy_list,
                                       bullet_list=bullet_list,
                                       all_blocks_list=all_blocks_list,
                                       destructible_blocks_list=destructible_blocks_list,
                                       indestructible_blocks_list=indestructible_blocks_list,
                                       drill_down_list = drill_down_list)

        # Initialize the map layer with some dungeon
        map_layer = MapLayer()
        map_layer_configuration = map_layer.get_full_map_layer_configuration(number_of_dungeons,
                                                                             number_of_coal_patches,
                                                                             number_of_gold_patches,
                                                                             number_of_shops,
                                                                             drill.center_x, drill.center_y)
        self.block_grid = BlockGrid(map_layer_configuration, self.sprites)
        self.current_level = current_level

        self._populate_level_with_enemies(map_layer_configuration)
        # Set viewpoint boundaries - where the drill currently has scrolled to
        self.time = 0
        self.frame = 0

    def _populate_level_with_enemies(self,
                                     map_layer_configuration,
                                     base_enemy_chance_cave: float = 0.006,
                                     base_enemy_chance_dungeon: float = 0.006,
                                     base_boss_chance: float = 0.003) -> None:
        """
        Spawns enemies into caves and dungeons.

        Parameters
        ----------
        enemy_chance_cave      :   float
            Probability of an enemy spawning in an empty cave block
        enemy_chance_dungeon   :   float
            Probability of an enemy spawning in an empty dungeon floor block
        """
        enemy_chance_cave = self.generate_enemy_chance(base_enemy_chance_cave)
        enemy_chance_dungeon = self.generate_enemy_chance(base_enemy_chance_dungeon)
        boss_chance = self.generate_enemy_chance(base_boss_chance)
        for row in map_layer_configuration:
            for block in row:
                if block[0] == ' ':
                    if np.random.rand() > (1 - enemy_chance_cave):
                        enemy_to_add = random.choice(potential_enemies)
                        enemy_to_append = enemy_to_add(block[1], block[2], vision=200)
                        self.sprites.entity_list.append(enemy_to_append)
                        self.sprites.enemy_list.append(enemy_to_append)
                elif block[0] == 'F':
                    if np.random.rand() > (1 - enemy_chance_dungeon):
                        enemy_to_add = random.choice(potential_enemies)
                        enemy_to_append = enemy_to_add(block[1], block[2], vision=200)
                        self.sprites.entity_list.append(enemy_to_append)
                        self.sprites.enemy_list.append(enemy_to_append)
                    elif np.random.rand() > (1 - boss_chance):
                        enemy_to_add = random.choice(potential_bosses)
                        enemy_to_append = enemy_to_add(block[1], block[2], vision=200, speed=0.7)
                        self.sprites.entity_list.append(enemy_to_append)
                        self.sprites.enemy_list.append(enemy_to_append)
        self.sprites.drill_list.append(self.sprites.drill)

        for entity in self.sprites.entity_list:
            entity.setup_collision_engine([self.sprites.indestructible_blocks_list])

    def generate_enemy_chance(self, base_enemy_chance: float):
        """
        Generates the odds of an enemy spawning in a given spot.
        Enemy chance increases by a natural logarithmic scale.

        Parameters
        ----------
        base_enemy_chance   :   float
            The minimum chance of this type of enemy

        Returns
        -------
        enemy_chance   :   float
            The chance of this type of enemy on the current layer
        """
        enemy_chance = base_enemy_chance * (1 + np.log(self.current_level + 1))
        return enemy_chance

    def draw(self) -> None:
        arcade.start_render()
        self.block_grid.air_blocks.draw()
        self.sprites.all_blocks_list.draw()
        self.sprites.explosion_list.draw()

        for entity in (*self.sprites.entity_list, self.sprites.drill):
            entity.draw()

    def update(self, time: float, delta_time: float, sprites, block_grid: BlockGrid):
        pass  # TODO currently this is all done in class: DrillDungeonGame
