from __future__ import annotations

from typing import Union

from .bullets import BlueNormalBullet
from .turret import Turret
from ..enemy import Enemy
from ..mixins import DiggingMixin, PathFindingMixin, ShotType
from ...utility import load_mirrored_textures, FaceDirection

import arcade


class GoblinEnemy(Enemy, DiggingMixin, PathFindingMixin):
    """

    Represents the Goblin (the enemy) attacking the player.

    Methods
    -------
    update(time: float, sprites)
        Handles specific update logic of the enemy.

    """
    def __init__(self, center_x: int, center_y: int, vision: Union[float, int],
                 speed: Union[float, int] = 1) -> None:
        """

        Parameters
        ----------
        center_x    :   int
            The starting x position in the map for this entity.
        center_y    :   int
            The starting y position in the map for this entity.
        vision      :   Union[float, int]
            The vision/detection field of the enemy.
        speed       :   Union[float, int]
            The movement speed of the enemy.

        """

        base_sprite: str = "resources/images/enemy/goblin/goblin_idle_1.png"
        sprite_scale: float = 1
        current_health = 50
        max_health = 50

        idle_textures = ["resources/images/enemy/goblin/goblin_idle_1.png",
                         "resources/images/enemy/goblin/goblin_idle_2.png",
                         "resources/images/enemy/goblin/goblin_idle_3.png",
                         "resources/images/enemy/goblin/goblin_idle_4.png",]

        moving_textures = ["resources/images/enemy/goblin/goblin_run_1.png",
                           "resources/images/enemy/goblin/goblin_run_2.png",
                           "resources/images/enemy/goblin/goblin_run_3.png",
                           "resources/images/enemy/goblin/goblin_run_4.png",]

        attack_textures = ["resources/images/enemy/goblin/goblin_attack_1.png",
                           "resources/images/enemy/goblin/goblin_attack_2.png",
                           "resources/images/enemy/goblin/goblin_attack_3.png",
                           "resources/images/enemy/goblin/goblin_attack_4.png",
                           "resources/images/enemy/goblin/goblin_attack_5.png",
                           "resources/images/enemy/goblin/goblin_attack_6.png",
                           "resources/images/enemy/goblin/goblin_attack_7.png",
                           "resources/images/enemy/goblin/goblin_attack_8.png",]

        time_between_animation_texture_updates = 0.15  # How many seconds between cycling to next texture

        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed,
                         current_health=current_health, max_health=max_health,
                         idle_textures=idle_textures, moving_textures=moving_textures,
                         time_between_animation_texture_updates=time_between_animation_texture_updates)
        PathFindingMixin.__init__(self, vision)

        self._last_shot_time = 0
        self._last_pathfind_time = 0

        self.attack = False
        self._attack_textures = []
        for texture in attack_textures:
            self._attack_textures.append(load_mirrored_textures(texture))

        self.damage = 400

        self._attack_sound = arcade.load_sound("resources/sound/meele.wav")

    def update(self, time: float, delta_time: float, sprites, block_grid) -> None:
        """

        Handles update logic specific to this Enemy.
        Attempts to shoot at and pathfind to the drill every x seconds.

        Note
        ----
        As this function is implemented in an Entity subclass, we need to call super().update() at the end of this
        function so that collision engines are updated accordingly.

        Parameters
        ----------
        time       :   float
            The time that the game has been running for. We can store this to do something every x amount of time.
        delta_time : float
            The time in seconds since the last game loop iteration.
        sprites    :   SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.
        block_grid : BlockGrid
            Reference to all blocks in the game.

        """
        if (time - self._last_shot_time) > 1.5:
            self._last_shot_time = time
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list) and (arcade.get_distance_between_sprites(self, sprites.drill) < 40):
                self.attack = True
                sprites.drill.hurt(self.damage)

        if (time - self._last_pathfind_time) > 1:
            self._last_pathfind_time = time
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
                self.path_to_position(sprites.drill.center_x, sprites.drill.center_y, sprites.all_blocks_list)

        super().update(time, delta_time, sprites, block_grid)

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self._facing_direction == FaceDirection.RIGHT:
            self._facing_direction = FaceDirection.LEFT
        elif self.change_x > 0 and self._facing_direction == FaceDirection.LEFT:
            self._facing_direction = FaceDirection.RIGHT

        self._time_since_last_texture_update += delta_time
        if self._time_since_last_texture_update > self._time_between_animation_texture_updates:
            self._time_since_last_texture_update = 0

            if self.change_x == 0 and self.change_y == 0:
                textures = self._idle_textures
            else:
                textures = self._moving_textures

            if self.attack:
                textures = self._attack_textures
                if (self._texture_index % len(textures))==(len(textures)-1):
                    self.attack = False

            self._texture_index = (self._texture_index + 1) % len(textures)
            self.texture = textures[self._texture_index][self._facing_direction.value]
