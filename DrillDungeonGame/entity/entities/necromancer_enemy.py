from __future__ import annotations
import arcade

from typing import Union

from .bullets import BlueNormalBullet
from .turret import Turret
from ..enemy import Enemy
from ..mixins.path_finding_mixin import PathFindingMixin
from ..mixins.shooting_mixin import ShootingMixin, ShotType
from ..mixins.digging_mixin import DiggingMixin
from ...utility.utility import *


RIGHT_FACING = 0
LEFT_FACING = 1

UPDATES_PER_FRAME = 5

class NecromancerEnemy(Enemy, PathFindingMixin, DiggingMixin):
    """

    Represents the Necromancer (the enemy) attacking the player.

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

        base_sprite: str = "resources/images/enemy/necromancer_idle_anim_f0.png"
        sprite_scale: float = 1.6
        turret_sprite = "resources/images/weapons/weapon_red_magic_staff.png"
        turret_scale = 1.2
        current_health = 50
        max_health = 50

        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed,
                         current_health=current_health, max_health=max_health)
        PathFindingMixin.__init__(self, vision)  # Init PathfindingMixin.
        self.children.append(Turret(turret_sprite, turret_scale, parent=self, bullet_type=BlueNormalBullet,
                                    firing_mode=ShotType.SINGLE))
        self._last_shot_time = 0
        self._last_pathfind_time = 0
        
        self.cur_texture = 0

        self.character_face_direction = RIGHT_FACING
        

        self.walk_textures = []
        self.idle_textures = []

        for i in range(4):
            texture = load_mirrored_textures(f"resources/images/enemy/necromancer_idle_anim_f{i}.png")
            self.idle_textures.append(texture)

        for i in range(4):
            texture = load_mirrored_textures(f"resources/images/enemy/necromancer_run_anim_f{i}.png")
            self.walk_textures.append(texture)


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
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
                self.children[0].aim(*sprites.drill.position)
                self.children[0].shoot(self.children[0].firing_mode, sprites)

        if (time - self._last_pathfind_time) > 1:
            self._last_pathfind_time = time
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
                self.path_to_position(sprites.drill.center_x, sprites.drill.center_y, sprites.destructible_blocks_list)


        #Sprite animation update
        self.update_animation()

        super().update(time, delta_time, sprites, block_grid)
        
    

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[0][0]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]
