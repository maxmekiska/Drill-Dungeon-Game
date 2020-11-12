from typing import List

import arcade

from DrillDungeonGame.entity.mixins import ShootingMixin, DiggingMixin, PathFindingMixin, ControllableMixin
from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.entity.entities.spaceship_enemy import SpaceshipEnemy
from DrillDungeonGame.map.dungeon_generator import MapLayer
from DrillDungeonGame.particles.explosion import PARTICLE_COUNT, ParticleDirt, ParticleCoal, Smoke, ParticleGold
from DrillDungeonGame.utility import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 2400
MAP_HEIGHT = 2400
SCREEN_TITLE = "Welcome to the Drill Dungeon"
VIEWPOINT_MARGIN = 40


class SpriteContainer:
    """This class is used as a storage class for all sprites in our game. Don't add them in DrillDungeonGame class.
    Furthermore, it allows getting all sprites of a certain category through the property methods."""
    def __init__(self, drill: Drill, dirt_list: arcade.SpriteList, border_wall_list: arcade.SpriteList,
                 coal_list: arcade.SpriteList, gold_list: arcade.SpriteList, bullet_list: arcade.SpriteList,
                 explosion_list: arcade.SpriteList, entity_list: arcade.SpriteList,
                 all_blocks_list: arcade.SpriteList, destructible_blocks_list: arcade.SpriteList,
                 indestructible_blocks_list: arcade.SpriteList) -> None:
        self.dirt_list = dirt_list
        self.border_wall_list = border_wall_list
        self.coal_list = coal_list
        self.gold_list = gold_list
        self.bullet_list = bullet_list
        self.explosion_list = explosion_list
        self.entity_list = entity_list

        # NOTE: The following sprite lists contain duplicates of sprites that will exist in sprite lists detailed above.
        # the drill is within the entity list. But would also be nice to have a direct reference to it.
        self.drill = drill
        self.all_blocks_list = all_blocks_list
        self.destructible_blocks_list = destructible_blocks_list
        self.indestructible_blocks_list = indestructible_blocks_list

    @property
    def all(self) -> List[arcade.SpriteList]:
        """Returns a list containing all SpriteLists. This doesn't include sprite_lists which contain duplicated
        sprites from other sprite lists."""
        return [self.drill, self.dirt_list, self.border_wall_list, self.coal_list,
                self.gold_list, self.bullet_list, self.explosion_list, self.entity_list]


class DrillDungeonGame(arcade.Window):
    """
    Basic map class
    """
    # This builds a dictionary of all possible keys that arcade can register as 'pressed'.
    # They unfortunately don't have another method to get this, and populating it before init is not taxing.
    possible_keys = {value: key for key, value in arcade.key.__dict__.items() if not key.startswith('_')}

    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        self.sprites = None
        # Initialize scrolling variables
        self.view_bottom = 0
        self.view_left = 0

        self.drill_down = False
        self.current_layer = 0

        self.gold_per_layer = 20
        self.coal_per_layer = 20
        self.dungeons_per_layer = 3

        self.frame = 0
        self.time = 0
        arcade.set_background_color(arcade.color.BROWN_NOSE)

    def setup(self, number_of_coal_patches: int = 20, number_of_gold_patches: int = 20,
              number_of_dungeons: int = 3, center_x: int = 64, center_y: int = 128) -> None:
        """Set up game and initialize variables"""
        dirt_list = arcade.SpriteList(use_spatial_hash=True)  # spatial hash, makes collision detection faster
        border_wall_list = arcade.SpriteList(use_spatial_hash=True)
        coal_list = arcade.SpriteList(use_spatial_hash=True)  # coal/fuel
        gold_list = arcade.SpriteList(use_spatial_hash=True)  # gold increment
        bullet_list = arcade.SpriteList()  # shooting/aiming
        explosion_list = arcade.SpriteList()  # explosion/smoke
        entity_list = arcade.SpriteList()  # All enemies
        drill = Drill(center_x=center_x, center_y=center_y)
        all_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        destructible_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        indestructible_blocks_list = arcade.SpriteList(use_spatial_hash=True)
        self.sprites = SpriteContainer(drill=drill, dirt_list=dirt_list, border_wall_list=border_wall_list,
                                       coal_list=coal_list, gold_list=gold_list, bullet_list=bullet_list,
                                       explosion_list=explosion_list, entity_list=entity_list,
                                       all_blocks_list=all_blocks_list,
                                       destructible_blocks_list=destructible_blocks_list,
                                       indestructible_blocks_list=indestructible_blocks_list)
        self.sprites.entity_list.append(drill)
        self.sprites.drill.physics_engine_setup(self.sprites.border_wall_list)
        self.sprites.entity_list.append(SpaceshipEnemy(200, 200, 200, 0.3))

        for entity in self.sprites.entity_list:
            entity.physics_engine_setup(self.sprites.border_wall_list)

        # Initialize the map layer with some dungeon
        map_layer = MapLayer(100, 100, meanDungeonSize=400, meanCoalSize=10, meanGoldSize=10)
        map_layer.generate_blank_map()
        for i in range(number_of_dungeons):
            map_layer.generate_dungeon()
        for i in range(number_of_coal_patches):
            map_layer.generate_coal()
        for i in range(number_of_gold_patches):
            map_layer.generate_gold()

        map_layer.generate_border_walls()
        # Load map layer from mapLayer
        self.load_map_layer_from_matrix(map_layer.mapLayerMatrix)

        # Set viewpoint boundaries - where the drill currently has scrolled to
        self.view_left = 0
        self.view_bottom = 0

    def draw_next_map_layer(self) -> None:
        """
        Generates and loads the next layer of the map when drilling down
        """
        self.setup(self.coal_per_layer,
                   self.gold_per_layer,
                   self.dungeons_per_layer,
                   self.sprites.drill.turret.center_x,
                   self.sprites.drill.turret.center_y)

        self.current_layer += 1
        self.update_map_configuration()

        arcade.start_render()
        self.sprites.dirt_list.draw()
        self.sprites.border_wall_list.draw()
        self.sprites.coal_list.draw()
        self.sprites.gold_list.draw()
        self.sprites.drill.draw()
        self.sprites.bullet_list.draw()
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
        self.sprites.bullet_list.draw()
        self.sprites.explosion_list.draw()

        for entity in self.sprites.entity_list:
            entity.draw()

        for entity in self.sprites.entity_list:
            if entity.path:
                arcade.draw_line_strip(entity.path, arcade.color.BLUE, 2)

        hud = f"Ammunition: {self.sprites.drill.ammunition}\nCoal:{self.sprites.drill.coal}\nGold:{self.sprites.drill.gold}"
        # update hud with screen scroll
        arcade.draw_text(hud, self.view_left + 10, self.view_bottom + 20, arcade.color.BLACK, 20)

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

    def fill_row_with_terrain(self, map_row: list, y_block_center: int, block_width: int, block_height: int) -> None:
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
        for entity in self.sprites.entity_list:
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

        if self.keys_pressed['T']:
            self.drill_down = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Same as above function, but it sets the value to False"""
        key_stroke = self.possible_keys.get(key)
        if key_stroke is None:
            return

        self.keys_pressed[key_stroke] = False
        for entity in self.sprites.entity_list:
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

        if self.keys_pressed['T']:
            self.drill_down = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """ Handle Mouse Motion """
        self.sprites.drill.aim(x + self.view_left, y + self.view_bottom)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.4)

        start_x = self.sprites.drill.turret.center_x
        start_y = self.sprites.drill.turret.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        dest_x = x + self.view_left
        dest_y = y + self.view_bottom

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        bullet.angle = math.degrees(angle)

        # bullet speed at the end
        bullet.change_x = math.cos(angle) * 7
        bullet.change_y = math.sin(angle) * 7

        # limited ammunition
        if self.sprites.drill.ammunition > 0:
            self.sprites.bullet_list.append(bullet)  # if empty, no more bullets append to bullet_list, no shooting
            self.sprites.drill.ammunition = self.sprites.drill.ammunition - 1

    def update_map_view(self) -> None:
        # Check if the drill has reached the edge of the box
        changed = False
        changed = self.check_for_scroll_left(changed)
        changed = self.check_for_scroll_right(changed)
        changed = self.check_for_scroll_up(changed)
        changed = self.check_for_scroll_down(changed)

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if changed:
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

    def check_for_scroll_left(self, changed: bool) -> bool:
        left_boundary = self.view_left + VIEWPOINT_MARGIN
        if self.sprites.drill.left < left_boundary:
            self.view_left -= left_boundary - self.sprites.drill.left
            changed = True
        return changed

    def check_for_scroll_right(self, changed: bool) -> bool:
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPOINT_MARGIN
        if self.sprites.drill.right > right_boundary:
            self.view_left += self.sprites.drill.right - right_boundary
            changed = True
        return changed

    def check_for_scroll_up(self, changed: bool) -> bool:
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPOINT_MARGIN
        if self.sprites.drill.top > top_boundary:
            self.view_bottom += self.sprites.drill.top - top_boundary
            changed = True
        return changed

    def check_for_scroll_down(self, changed: bool) -> bool:
        bottom_boundary = self.view_bottom + VIEWPOINT_MARGIN
        if self.sprites.drill.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.sprites.drill.bottom
            changed = True
        return changed

    # moved on_update to the end of the main
    def on_update(self, delta_time: float) -> None:
        """ Movement and game logic """
        self.frame += 1
        self.time += delta_time

        for entity in self.sprites.entity_list:
            if issubclass(entity.__class__, DiggingMixin):
                entity.dig(self.sprites.destructible_blocks_list)

        # collects coal and increments fuel tank
        self.sprites.drill.collect_coal(self.sprites.coal_list)
        # collect gold and increments gold
        self.sprites.drill.collect_gold(self.sprites.gold_list)

        # Check for side scrolling
        self.update_map_view()

        # self.physics_engine.update()

        for entity in self.sprites.entity_list:
            entity.update()

        self.sprites.bullet_list.update()
        self.sprites.explosion_list.update()
        self.bullet_update()  # TODO remove.

        if self.drill_down:
            self.draw_next_map_layer()
            self.drill_down = False

        for entity in self.sprites.entity_list:
            if isinstance(entity, ShootingMixin) and not isinstance(entity, Drill) and entity.has_line_of_sight_with(self.sprites.drill, self.sprites.all_blocks_list):
                entity.aim(self.sprites.drill.center_x, self.sprites.drill.center_y)

        # TODO don't use frame as measure of doing task every x loops. Store a variable in each entity class such
        # as last_updated. We can iterate over all entities and check when entity tasks were last updated.
        if self.frame % 30 == 0:  # Do something every 30 frames.
            for entity in self.sprites.entity_list:
                if not isinstance(entity, Drill):
                    # When this gets moved to entity.update(), we won't need to do all this isinstance checks
                    # We only have this code here now as it isn't abstracted yet.
                    if isinstance(entity, (PathFindingMixin, ShootingMixin)) and \
                            entity.has_line_of_sight_with(self.sprites.drill, self.sprites.all_blocks_list):
                        if isinstance(entity, PathFindingMixin):
                            entity.path_to_position(*self.sprites.drill.position, self.sprites.destructible_blocks_list)
                        if isinstance(entity, ShootingMixin):
                            entity.shoot()

    def bullet_update(self) -> None:
        for bullet in self.sprites.bullet_list:
            hit_list_wall = arcade.check_for_collision_with_list(bullet, self.sprites.dirt_list)
            hit_list_coal = arcade.check_for_collision_with_list(bullet, self.sprites.coal_list)
            hit_list_gold = arcade.check_for_collision_with_list(bullet, self.sprites.gold_list)
            # remove bullet
            if len(hit_list_wall) > 0:
                bullet.remove_from_sprite_lists()
            # remove hit wall
            for wall in hit_list_wall:
                # explosion and smoke when wall hit
                for i in range(PARTICLE_COUNT):
                    particle = ParticleDirt(self.sprites.explosion_list)
                    particle.position = wall.position
                    self.sprites.explosion_list.append(particle)
                    wall.remove_from_sprite_lists()

            if len(hit_list_coal) > 0:
                bullet.remove_from_sprite_lists()
            for coal in hit_list_coal:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleCoal(self.sprites.explosion_list)
                    particle.position = coal.position
                    self.sprites.explosion_list.append(particle)

                smoke = Smoke(50)
                smoke.position = coal.position
                self.sprites.explosion_list.append(smoke)
                coal.remove_from_sprite_lists()

            if len(hit_list_gold) > 0:
                bullet.remove_from_sprite_lists()
            for gold in hit_list_gold:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleGold(self.sprites.explosion_list)
                    particle.position = gold.position
                    self.sprites.explosion_list.append(particle)

                    gold.remove_from_sprite_lists()

            # later also add for enemies

            if bullet.center_x > self.width + self.view_left or bullet.center_x < self.view_left or \
                    bullet.center_y > self.width+self.view_bottom or bullet.center_y < self.view_bottom:
                bullet.remove_from_sprite_lists()
