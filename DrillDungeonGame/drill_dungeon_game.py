from typing import List

import arcade

from DrillDungeonGame.entity.mixins.controllable_mixin import ControllableMixin
from DrillDungeonGame.entity.mixins.path_finding_mixin import PathFindingMixin
from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.entity.entities.spaceship_enemy import SpaceshipEnemy
from DrillDungeonGame.in_game_menus import *
from DrillDungeonGame.map.dungeon_generator import MapLayer
from DrillDungeonGame.map.dungeon_generator import MapLayer, MAP_WIDTH, MAP_HEIGHT
from DrillDungeonGame.sprite_container import SpriteContainer
from DrillDungeonGame.map.chunk_manager import Chunk, ChunkManager
from DrillDungeonGame.utility import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Welcome to the Drill Dungeon"
VIEWPOINT_MARGIN = 120


class View:
    def __init__(self) -> None:
        self.left_offset = 0
        self.bottom_offset = 0
        self._centre_sprite = None
        # TODO store the width/height of the screen. This can then be passed to the Entity.update() function

    def update(self, centre_sprite: arcade.Sprite) -> None:
        # Check if the drill has reached the edge of the box
        self._centre_sprite = centre_sprite
        changed = any((self._check_for_scroll_left(), self._check_for_scroll_right(),
                      self._check_for_scroll_up(), self._check_for_scroll_down()))

        self.left_offset = int(self.left_offset)
        self.bottom_offset = int(self.bottom_offset)

        if changed:
            arcade.set_viewport(self.left_offset, SCREEN_WIDTH + self.left_offset,
                                self.bottom_offset, SCREEN_HEIGHT + self.bottom_offset)

    def _check_for_scroll_left(self) -> bool:
        left_boundary = self.left_offset + VIEWPOINT_MARGIN
        if self._centre_sprite.left < left_boundary:
            self.left_offset -= left_boundary - self._centre_sprite.left
            return True
        return False

    def _check_for_scroll_right(self) -> bool:
        right_boundary = self.left_offset + SCREEN_WIDTH - VIEWPOINT_MARGIN
        if self._centre_sprite.right > right_boundary:
            self.left_offset += self._centre_sprite.right - right_boundary
            return True
        return False

    def _check_for_scroll_up(self) -> bool:
        top_boundary = self.bottom_offset + SCREEN_HEIGHT - VIEWPOINT_MARGIN
        if self._centre_sprite.top > top_boundary:
            self.bottom_offset += self._centre_sprite.top - top_boundary
            return True
        return False

    def _check_for_scroll_down(self) -> bool:
        bottom_boundary = self.bottom_offset + VIEWPOINT_MARGIN
        if self._centre_sprite.bottom < bottom_boundary:
            self.bottom_offset -= bottom_boundary - self._centre_sprite.bottom
            return True
        return False


class DrillDungeonGame(arcade.View):
    # This builds a dictionary of all possible keys that arcade can register as 'pressed'.
    # They unfortunately don't have another method to get this, and populating it before init is not taxing.
    possible_keys = {value: key for key, value in arcade.key.__dict__.items() if not key.startswith('_')}

    def __init__(self, window) -> None:
        super().__init__()
        self.game_window = window
        self.keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        self.sprites = None
        self.upwards_layer = None
        self.downwards_layer = None
        # Initialize scrolling variables
        self.view = View()

        self.drill_up = False
        self.drill_down = False
        self.current_layer = 0

        self.gold_per_layer = 20
        self.coal_per_layer = 20
        self.dungeons_per_layer = 3

        self.frame = 0
        self.time = 0
        arcade.set_background_color(arcade.color.BROWN_NOSE)
        # self.firing_mode = ShotType.SINGLE
        self.mouse_position = (1, 1)

    def setup(self, number_of_coal_patches: int = 20, number_of_gold_patches: int = 20,
              number_of_dungeons: int = 3, center_x: int = 128, center_y: int = 128) -> None:
        """Set up game and initialize variables"""
        dirt_list = arcade.SpriteList(use_spatial_hash=True)  # spatial hash, makes collision detection faster
        border_wall_list = arcade.SpriteList(use_spatial_hash=True)
        shop_list = arcade.SpriteList(use_spatial_hash=True)
        coal_list = arcade.SpriteList(use_spatial_hash=True)  # coal/fuel
        gold_list = arcade.SpriteList(use_spatial_hash=True)  # gold increment
        explosion_list = arcade.SpriteList()  # explosion/smoke
        entity_list = arcade.SpriteList()  # ALL enemies
        drill_list = arcade.SpriteList()
        enemy_list = arcade.SpriteList()
        bullet_list = arcade.SpriteList()

        #TODO fix this so that stats arent reset on drill down
        drill = Drill(center_x=center_x, center_y=center_y, health=100, ammunition=400, coal=30, gold=0)
        all_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        destructible_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        indestructible_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprites = SpriteContainer(drill=drill, dirt_list=dirt_list, border_wall_list=border_wall_list,
                                       shop_list=shop_list, coal_list=coal_list, gold_list=gold_list,
                                       explosion_list=explosion_list, entity_list=entity_list,
                                       drill_list=drill_list,
                                       enemy_list=enemy_list,
                                       bullet_list=bullet_list,
                                       all_blocks_list=all_blocks_list,
                                       destructible_blocks_list=destructible_blocks_list,
                                       indestructible_blocks_list=indestructible_blocks_list)
        # generate one enemy
        enemy_one = SpaceshipEnemy(300, 300, vision=200, speed=0.7)
        enemy_two = SpaceshipEnemy(500, 400, vision=200, speed=0.7)
        enemy_three = SpaceshipEnemy(300, 50, vision=200, speed=0.7)
        self.sprites.entity_list.append(enemy_one)
        self.sprites.entity_list.append(enemy_two)
        self.sprites.entity_list.append(enemy_three)
        self.sprites.drill_list.append(self.sprites.drill)

        self.sprites.enemy_list.append(enemy_one)
        self.sprites.enemy_list.append(enemy_two)
        self.sprites.enemy_list.append(enemy_three)
        
        # Initialize the map layer with some dungeon
        map_layer = MapLayer()

        map_layer_configuration = map_layer.get_full_map_layer_configuration(number_of_dungeons, number_of_coal_patches, number_of_gold_patches)
        #Test out the chunk manager functionality
        
        self.cmanager = ChunkManager(map_layer_configuration)
        self.cmanager._update_chunks(center_x, center_y)
        for active_chunk in self.cmanager.active_chunks:
            self.sprites.extend(self.cmanager.chunks_dictionary[active_chunk].chunk_sprites)
        for entity in (*self.sprites.entity_list, self.sprites.drill):
            entity.setup_collision_engine([self.sprites.indestructible_blocks_list])


        # Set viewpoint boundaries - where the drill currently has scrolled to
        self.view.left_offset = 0
        self.view.bottom_offset = 0

    def draw_next_map_layer(self) -> None:
        """
        Generates and loads the next layer of the map when drilling down
        """
        self.upwards_layer = self.cmanager
        if self.downwards_layer == None:
            self.setup(self.coal_per_layer,
                       self.gold_per_layer,
                       self.dungeons_per_layer,
                       self.sprites.drill.center_x,
                       self.sprites.drill.center_y)

            self.update_map_configuration()


        else:
            self.cmanager = self.downwards_layer
            self.downwards_layer = None

        self.current_layer += 1
        self.reload_chunks()

        arcade.start_render()
        self.sprites.dirt_list.draw()
        self.sprites.border_wall_list.draw()
        self.sprites.coal_list.draw()
        self.sprites.gold_list.draw()
        self.sprites.drill.draw()
        self.sprites.explosion_list.draw()

    def draw_previous_layer(self) -> None:
        print(self.upwards_layer)
        self.current_layer -= 1
        self.downwards_layer = self.cmanager
        self.cmanager = self.upwards_layer
        self.reload_chunks()
        self.upwards_layer = None

        arcade.start_render()
        self.sprites.dirt_list.draw()
        self.sprites.border_wall_list.draw()
        self.sprites.shop_list.draw()
        self.sprites.coal_list.draw()
        self.sprites.gold_list.draw()
        self.sprites.drill.draw()
        self.sprites.explosion_list.draw()

    def update_map_configuration(self) -> None:
        """
        Updates the map's configuration specs for the next layer, allowing for
        increased difficulty
        """
        self.coal_per_layer = generate_next_layer_resource_patch_amount(self.current_layer)
        self.gold_per_layer = generate_next_layer_resource_patch_amount(self.current_layer)
        self.dungeons_per_layer = generate_next_layer_dungeon_amount(self.current_layer)

    def on_draw(self) -> None:
        """
        Draws the map
        """
        arcade.start_render()
        self.sprites.dirt_list.draw()
        self.sprites.coal_list.draw()
        self.sprites.gold_list.draw()
        self.sprites.border_wall_list.draw()
        self.sprites.shop_list.draw()
        self.sprites.explosion_list.draw()

        for entity in (*self.sprites.entity_list, *self.sprites.bullet_list, self.sprites.drill):
            entity.draw()

        for entity in self.sprites.entity_list:
            if entity.path:
                arcade.draw_line_strip(entity.path, arcade.color.BLUE, 2)

        hud = f"Ammunition: {self.sprites.drill.inventory.ammunition}\nCoal:{self.sprites.drill.inventory.coal}" \
              f"\nGold:{self.sprites.drill.inventory.gold}\nHealth:{self.sprites.drill.health}"
        # update hud with screen scroll
        arcade.draw_text(hud, self.view.left_offset + 10, self.view.bottom_offset + 20, arcade.color.BLACK, 20)

    def load_map_layer_from_matrix(self, map_layer_matrix: List) -> None:
        """
        Loads a map from a layer matrix
        list map_layer_matrix : A matrix containing the map configuration, as
        generated by the MapLayer class
        """
        map_layer_height = len(map_layer_matrix)
        map_layer_width = len(map_layer_matrix[0])
        block_height = MAP_HEIGHT / map_layer_height
        block_width = MAP_WIDTH / map_layer_width
        y_block_center = 0.5 * block_height
        for row in map_layer_matrix:
            self.fill_row_with_terrain(row, y_block_center, block_width, block_height)
            y_block_center += block_height

    def fill_row_with_terrain(self, map_row: list, y_block_center: Union[float, int], block_width: Union[float, int],
                              block_height: Union[float, int]) -> None:
        """
        Fills a row with terrain
        list map_row        : a row of the map matrix
        int y_block_center   : the y of the center of the blocks for the row
        int block_width     : width of the blocks to fill the terrain
        int block_height    : height of the blocks to fill the terrain
        """
        x_block_center = 0.5 * block_width
        for item in map_row:
            wall_sprite = None
            if item == 'X':  # Dirt
                wall_sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.18)
                # wall_sprite.width = blockWidth
                # wall_sprite.height = blockHeight
                wall_sprite.center_x = x_block_center
                wall_sprite.center_y = y_block_center
                self.sprites.dirt_list.append(wall_sprite)
                self.sprites.destructible_blocks_list.append(wall_sprite)
            if item == 'C':  # Coal
                wall_sprite = arcade.Sprite("resources/images/material/Coal_square.png", 0.03)
                # wall_sprite.width = blockWidth
                # wall_sprite.height = blockHeight
                wall_sprite.center_x = x_block_center
                wall_sprite.center_y = y_block_center
                self.sprites.coal_list.append(wall_sprite)
                self.sprites.destructible_blocks_list.append(wall_sprite)
            if item == 'G':  # Gold
                wall_sprite = arcade.Sprite("resources/images/material/Gold_square.png", 0.03)
                wall_sprite.center_x = x_block_center
                wall_sprite.center_y = y_block_center
                self.sprites.gold_list.append(wall_sprite)
                self.sprites.destructible_blocks_list.append(wall_sprite)
            if item == 'O':  # Border block.
                wall_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.18)
                wall_sprite.center_x = x_block_center
                wall_sprite.center_y = y_block_center
                self.sprites.border_wall_list.append(wall_sprite)
                self.sprites.indestructible_blocks_list.append(wall_sprite)
            if item == 'S':  # Shop.
                wall_sprite = arcade.Sprite("resources/images/shop/shop.png", 0.18)
                wall_sprite.center_x = x_block_center
                wall_sprite.center_y = y_block_center
                self.sprites.shop_list.append(wall_sprite)
                self.sprites.indestructible_blocks_list.append(wall_sprite)
            if wall_sprite is not None:
                self.sprites.all_blocks_list.append(wall_sprite)
            x_block_center += block_width

    def on_key_press(self, key: int, modifiers: int) -> None:
        """If a key is pressed, it sets that key in self.keys_pressed dict to True, and passes the dict onto
        every entity that requires this information. ie All that subclass ControllableMixin.
        This will probably just be the drill... but maybe we wan't controllable minions?"""
        key_stroke = self.possible_keys.get(key)
        if key_stroke is None:
            return

        self.keys_pressed[key_stroke] = True
        for entity in (*self.sprites.entity_list, self.sprites.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

        if self.keys_pressed['T']:
            # Drill down to the next layer.
            self.drill_down = True

        elif self.keys_pressed['ESCAPE']:
            # pause game
            self.keys_pressed = {key:False for key in self.keys_pressed}
            self.sprites.drill.stop_moving()
            pause_menu = PauseMenu(self, self.window, self.view)
            self.window.show_view(pause_menu)

        elif self.keys_pressed['U']:
            if not self.upwards_layer == None:
                self.drill_up = True
            else:
                print("No saved upwards layer")

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Same as above function, but it sets the value to False"""
        key_stroke = self.possible_keys.get(key)
        if key_stroke is None:
            return

        self.keys_pressed[key_stroke] = False
        for entity in (*self.sprites.entity_list, self.sprites.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

        if self.keys_pressed['T']:
            self.drill_down = False

        elif self.keys_pressed['U']:
            self.drill_up = False 

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """ Handle Mouse Motion """
        self.mouse_position = (x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for shop in self.sprites.shop_list:
            if shop.collides_with_point((self.view.left_offset+x,self.view.bottom_offset+y,)) and \
               (arcade.get_distance_between_sprites(shop, self.sprites.drill)<70):
                self.sprites.drill.stop_moving()
                self.keys_pressed = {key: False for key in self.keys_pressed}
                shop = ShopMenu(self, self.window, self.view)
                self.window.show_view(shop)

        for entity in (*self.sprites.entity_list, self.sprites.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_mouse_click(button)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        for entity in (*self.sprites.entity_list, self.sprites.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_mouse_release(button)

    def reload_chunks(self):
        """
        Loads up the fresh set of chunks for interaction
        """
        print("RELOADING CHUNKS")
        self.cmanager._update_chunks(self.sprites.drill.center_x, self.sprites.drill.center_y)
        self.sprites = SpriteContainer(drill = self.sprites.drill, 
                                        dirt_list = arcade.SpriteList(), 
                                        border_wall_list = arcade.SpriteList(), 
                                        shop_list = self.sprites.shop_list, 
                                        coal_list = arcade.SpriteList(), 
                                        gold_list = arcade.SpriteList(), 
                                        explosion_list = self.sprites.explosion_list, 
                                        entity_list = self.sprites.entity_list, 
                                        drill_list = self.sprites.drill_list, 
                                        enemy_list = self.sprites.enemy_list, 
                                        bullet_list = arcade.SpriteList(), 
                                        all_blocks_list = arcade.SpriteList(), 
                                        destructible_blocks_list = arcade.SpriteList(), 
                                        indestructible_blocks_list = arcade.SpriteList())
        #The above line may cause issues down the road with combat, will need to change what goes into the all_blocks_list
        self.sprites.all_blocks_list.extend(self.sprites.entity_list)
        self.sprites.all_blocks_list.extend(self.sprites.enemy_list)
        self.sprites.all_blocks_list.extend(self.sprites.explosion_list)
        self.sprites.all_blocks_list.extend(self.sprites.shop_list)
        self.sprites.all_blocks_list.extend(self.sprites.drill_list)
        for active_chunk in self.cmanager.active_chunks:
            self.sprites.extend(self.cmanager.chunks_dictionary[active_chunk].chunk_sprites)
        for entity in self.sprites.entity_list:
            entity.setup_collision_engine([self.sprites.border_wall_list])

    # moved on_update to the end of the main
    def on_update(self, delta_time: float) -> None:
        """This function is called by the arcade library every iteration (or frame).
        Delta time is the time since the last iteration. We can add these up each time this function is called
        to get the 'running time' of the game."""
        self.frame += 1
        self.time += delta_time

        # Check for side scrolling
        self.view.update(self.sprites.drill)

        # TODO move this into entities.Drill.update(). We need to pass view as a param to update()
        self.sprites.drill.children[0].aim(self.mouse_position[0] + self.view.left_offset,
                                           self.mouse_position[1] + self.view.bottom_offset)

        for entity in (*self.sprites.entity_list, *self.sprites.bullet_list, self.sprites.drill):
            # pass the sprite Container so update function can interact with other sprites.
            entity.update(self.time, delta_time, self.sprites)

        self.sprites.explosion_list.update()

        if self.drill_down:
            self.draw_next_map_layer()
            self.drill_down = False

        if self.drill_up:
            self.draw_previous_layer()
            self.drill_up = False

        for bullet in self.sprites.bullet_list:
            if bullet.center_x > self.game_window.width + self.view.left_offset or bullet.center_x < self.view.left_offset or \
                    bullet.center_y > self.game_window.width + self.view.bottom_offset or \
                    bullet.center_y < self.view.bottom_offset:
                bullet.remove_from_sprite_lists()

        # TODO don't use frame as measure of doing task every x loops. Store a variable in each entity class such
        # as last_updated. We can iterate over all entities and check when entity tasks were last updated.
        if self.frame % 300 == 0: #TODO Create better way of determining when to update
            self.reload_chunks()
        if self.frame % 30 == 0:  # Do something every 30 frames.
            for entity in self.sprites.entity_list:
                # When this gets moved to entity.update(), we won't need to do all this isinstance checks
                # We only have this code here now as it isn't abstracted yet.
                if isinstance(entity, (PathFindingMixin, ShootingMixin)) and \
                        entity.has_line_of_sight_with(self.sprites.drill, self.sprites.all_blocks_list):
                    if isinstance(entity, PathFindingMixin):
                        entity.path_to_position(*self.sprites.drill.position, self.sprites.destructible_blocks_list)
                    if isinstance(entity, ShootingMixin):
                        entity.shoot(ShotType.SINGLE)
