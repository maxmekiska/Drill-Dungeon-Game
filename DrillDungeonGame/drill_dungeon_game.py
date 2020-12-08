import arcade

from .entity.entities import Drill
from .entity.mixins import ControllableMixin, ShotType
from .in_game_menus import draw_3d_rectangle
from .level import Level
from .obscure_vision import ObscuredVision
from .utility import generate_next_layer_resource_patch_amount, generate_next_layer_dungeon_amount
from .view_margins import View


class DrillDungeonGame(arcade.View):
    """
    Contains the game logic.

    Methods
    -------
    setup(number_of_coal_patches: int, number_of_gold_patches: int, number_of_dungeons: int, center_x: int, center_y: int)
        Set up game and initialize variables.
    draw_next_map_layer()
        Generates and loads the next layer of the map when drilling down.
    draw_previous_layer()
        Generates and loads previous layer before drill down action has been performed.
    update_map_configuration()
        Updates the map's configuration specs for the next layer, allowing for increased difficulty.
    on_draw()
        Draws map.
    load_map_layer_from_matrix(map_layer_matrix: List)
        Loads a map from a layer matrix.
    fill_row_with_terrain(map_row: list, y_block_center: Union[float, int], block_width: Union[float, int], block_height: Union[float, int])
        Fills a row with terrain.
    on_key_press(key: int, modifiers: int)
        If key is pressed, it sets that key in self.keys_pressed dict to True.
    on_key_release(key: int, modifiers: int)
        If key is released, sets that key in self.keys_pressed dict to False.
    on_mouse_motion(x: float, y: float, dx: float, dy: float)
        Handles mouse motion.
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Executes logic when mouse key is pressed.
    on_mouse_release(x: float, y: float, button: int, modifiers: int)
        Executes logic when mouse key is released.
    reload_chunks()
        Loads fresh set of chunks.
    on_update(delta_time: float)
        Method is called by the arcade library every iteration. Provides basis for game running time.

    """
    # This builds a dictionary of all possible keys that arcade can register as 'pressed'.
    # They unfortunately don't have another method to get this, and populating it before init is not taxing.
    possible_keys = {value: key for key, value in arcade.key.__dict__.items() if not key.startswith('_')}

    def __init__(self, window) -> None:
        """

        Parameters
        ----------
        window: entity
            Window to be shown to the player.

        """
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.window = window
        self.keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        self.sprites = None
        self.upwards_layer = None
        self.downwards_layer = None

        self.view = View()

        self.gold_per_layer = 20
        self.coal_per_layer = 20
        self.dungeons_per_layer = 3

        self.frame = 0
        self.time = 0

        self.mouse_position = (1, 1)

        self.drill = Drill(center_x=150,
                           center_y=150,
                           current_health=700,
                           max_health=700,
                           ammunition=400,
                           coal=200,
                           gold=0)

        self._levels = []
        self._level_index = 0
        self._levels.append(Level(drill=self.drill))
        self.drill.setup_collision_engine([self.current_level.sprites.indestructible_blocks_list])

        self.vignette = ObscuredVision()

        self.score = 0

    def setup(self):
        self.frame = 0
        self.time = 0

        self.mouse_position = (1, 1)

        self.drill = Drill(center_x=150,
                           center_y=150,
                           current_health=700,
                           max_health=700,
                           ammunition=400,
                           coal=200,
                           gold=0)

        self._levels = []
        self._level_index = 0
        self._levels.append(Level(drill=self.drill))
        self.drill.setup_collision_engine([self.current_level.sprites.indestructible_blocks_list])

        self.vignette = ObscuredVision()

        self.score = 0

    @property
    def current_level(self):
        return self._levels[self._level_index]

    def update_map_configuration(self) -> None:
        """

        Updates the map's configuration specs for the next layer, allowing for
        increased difficulty.

        """
        self.coal_per_layer = generate_next_layer_resource_patch_amount(self.current_layer)
        self.gold_per_layer = generate_next_layer_resource_patch_amount(self.current_layer)
        self.dungeons_per_layer = generate_next_layer_dungeon_amount(self.current_layer)

    def on_draw(self) -> None:
        """Draws the map."""
        self.current_level.draw()

        self.vignette.draw(self.drill.center_x, self.drill.center_y)

        draw_3d_rectangle(self.view.left_offset+110, self.view.bottom_offset+70, 220, 140, arcade.color.LIGHT_GRAY+(150,),
                          arcade.color.WHITE+(150,), arcade.color.GRAY+(150,), 2)
        self.drill.draw_health_bar(self.view.left_offset+80, self.view.bottom_offset+50, 130, 20)
        self.drill.draw_shield_bar(self.view.left_offset+80, self.view.bottom_offset+20, 130, 20)
        hud = f"Ammunition: {self.drill.inventory.ammunition}\nCoal:{self.drill.inventory.coal}" \
              f"\nGold:{self.drill.inventory.gold}"
        # update hud with screen scroll
        arcade.draw_text(hud, self.view.left_offset + 10, self.view.bottom_offset + 60, arcade.color.BLACK, 20)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """

        If a key is pressed, it sets that key in self.keys_pressed dict to True, and passes the dict onto
        every entity that requires this information.

        Notes
        -----
        For example, all that subclass ControllableMixin.
        This will probably just be the drill...
        but maybe we want controllable minions?

        Parameters
        ----------
        key         : int
            Key of self.keys_pressed
        modifiers   : int
            Modifier value.

        """
        key_stroke = self.possible_keys.get(key)
        if key_stroke is None:
            return

        self.keys_pressed[key_stroke] = True
        for entity in (*self.current_level.sprites.entity_list, self.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

        if self.keys_pressed['T']:
            # Drill down to the next layer.
            if self.drill.check_ground_for_drilling(self.current_level.sprites):
                if (len(self._levels) - self._level_index) == 1:
                    next_level = Level(self.drill)
                    self._levels.append(next_level)
                self._level_index += 1
                self.drill.collision_engine = []  # Clear previous level collision engine first.
                self.drill.setup_collision_engine([self.current_level.sprites.indestructible_blocks_list])
                self.vignette.decrease_vision()
                self.drill.children[0].shoot(ShotType.SINGLE, self.current_level.sprites)
            else:
                print("Cannot drill here")

        elif self.keys_pressed['ESCAPE']:
            # pause game
            self.keys_pressed = {key: False for key in self.keys_pressed}
            self.drill.stop_moving()
            self.window.show_view(self.window.pause_view)

        elif self.keys_pressed['U']:
            if self.drill.check_ground_for_drilling(self.current_level.sprites):
                if self._level_index > 0:
                    self._level_index -= 1
                self.drill.collision_engine = []  # Clear previous level collision engine first.
                self.drill.setup_collision_engine([self.current_level.sprites.indestructible_blocks_list])
                self.vignette.increase_vision()
            else:
                print('Cannot drill here')

        # DEBUGGING CONTROLS
        elif self.keys_pressed['O']:
            self.vignette.increase_vision()

        elif self.keys_pressed['L']:
            self.vignette.decrease_vision()

        elif self.keys_pressed['K']:
            self.vignette.blind()

        elif self.keys_pressed['SEMICOLON']:
            self.vignette.far_sight()

        elif self.keys_pressed['M']:
            self.window.show_view(self.window.shop_view)

    def on_key_release(self, key: int, modifiers: int) -> None:
        """

        If a key is released, it sets that key in self.keys_pressed dict to False, and passes the dict onto
        every entity that requires this information.

        Parameters
        ----------
        key         : int
            Key of self.keys_pressed
        modifiers   : int
            Modifier value.

        """
        key_stroke = self.possible_keys.get(key)
        if key_stroke is None:
            return

        self.keys_pressed[key_stroke] = False

        for entity in (*self.current_level.sprites.entity_list, self.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_key_press_release(self.keys_pressed)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        """

        Detects when button on mouse is pressed.

        Parameters
        ----------
        x           : float
            x-coordinate.
        y           : float
            y-coordinate.
        button      : int
            Button pressed.
        modifiers   : int
            Modifier value.

        """
        for shop in self.current_level.sprites.shop_list:
            if shop.collides_with_point((self.view.left_offset + x, self.view.bottom_offset + y)) and \
               (arcade.get_distance_between_sprites(shop, self.drill) < 70):
                self.drill.stop_moving()

                #  Release all buttons and mouse clicks.
                self.keys_pressed = {key: False for key in self.keys_pressed}
                for entity in (*self.current_level.sprites.entity_list, self.drill):
                    if issubclass(entity.__class__, ControllableMixin):
                        entity.handle_mouse_release(button)

                self.window.show_view(self.window.shop_view)

        for entity in (*self.current_level.sprites.entity_list, self.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_mouse_click(button)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """

        Detects when button on mouse is released.

        Parameters
        ----------
        x           : float
            x-coordinate.
        y           : float
            y-coordinate.
        button      : int
            Button pressed.
        modifiers   : int
            Modifier value.

        """
        for entity in (*self.current_level.sprites.entity_list, self.drill):
            if issubclass(entity.__class__, ControllableMixin):
                entity.handle_mouse_release(button)

    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.BLACK)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """

        Handle Mouse Motion.

        Parameters
        ----------
        x       : float
            x-coordinate.
        y       : float
            y-coordinate.
        dx      : float
            Change in x-coordinate.
        dy      : float
            Change in y-coordinate.

        """
        self.mouse_position = (x, y)

    # moved on_update to the end of the main
    def on_update(self, delta_time: float) -> None:
        """

        This method is called by the arcade library every iteration (or frame).

        Notes
        -----
        We can add these up each time this function is called
        to get the 'running time' of the game.

        Parameters
        ----------
        delta_time  : float
            Time since last iteration

        """
        self.frame += 1
        self.time += delta_time

        if self.frame == 1:
            self.drill.children[0].shoot(ShotType.SINGLE, self.current_level.sprites)

        if self.drill.current_health <= 0:
            self.drill.current_health = 0
            self.window.show_view(self.window.game_over_view)
            return

        # Check for side scrolling
        self.view.update(self.drill)

        # TODO move this into entities.Drill.update(). We need to pass view as a param to update()
        self.drill.children[0].aim(self.mouse_position[0] + self.view.left_offset,
                                   self.mouse_position[1] + self.view.bottom_offset)

        enemies = len(self.current_level.sprites.entity_list)
        gold = self.drill.inventory.gold
        coal = self.drill.inventory.coal

        for entity in (*self.current_level.sprites.entity_list, self.drill):
            # pass the sprite Container so update function can interact with other sprites.
            entity.update(self.time, delta_time, self.current_level.sprites, self.current_level.block_grid)

        if len(self.current_level.sprites.entity_list) < enemies:
            self.score += enemies-len(self.current_level.sprites.entity_list)
        if self.drill.inventory.gold > gold:
            self.score += self.drill.inventory.gold-gold
        if self.drill.inventory.coal > coal:
            self.score += self.drill.inventory.coal-coal

        self.current_level.sprites.explosion_list.update()

        # for bullet in self.current_level.sprites.bullet_list:
        #     if bullet.center_x > self.window.width + self.view.left_offset or \
        #             bullet.center_x < self.view.left_offset or \
        #             bullet.center_y > self.window.width + self.view.bottom_offset or \
        #             bullet.center_y < self.view.bottom_offset:
        #         bullet.remove_from_sprite_lists()
