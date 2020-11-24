from __future__ import annotations

from typing import Union

from .bullets import BlueNormalBullet
from .turret import Turret
from ..enemy import Enemy
from ..mixins.path_finding_mixin import PathFindingMixin
from ..mixins.shooting_mixin import ShootingMixin, ShotType
from ..mixins.digging_mixin import DiggingMixin


class SpaceshipEnemy(Enemy, PathFindingMixin, DiggingMixin):
    """

    Represents the Spaceship (the enemy) attacking the player.

    Methods
    -------
    update(time: float, sprites)
        Handles specific update logic of the enemy.

    """
    def __init__(self, center_x: int, center_y: int, vision: Union[float, int],
                 speed: Union[float, int] = 1) -> None:

        base_sprite: str = "resources/images/enemy/enemy.png"
        sprite_scale: float = 0.3
        turret_sprite = "resources/images/weapons/turret1.png"
        turret_scale = 0.2
        health = 50
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, health=health)
        PathFindingMixin.__init__(self, vision)  # Init PathfindingMixin.
        self.children.append(Turret(turret_sprite, turret_scale, parent=self, bullet_type=BlueNormalBullet,
                                    firing_mode=ShotType.SINGLE))
        self._last_shot_time = 0
        self._last_pathfind_time = 0
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
        
        Returns
        -------
        None
                         
        """

    def update(self, time: float, sprites) -> None:
        """

        Handles update logic specific to this Enemy.
        Attempts to shoot at and pathfind to the drill every x seconds.

        Note
        ----
        As this function is implemented in an Entity subclass, we need to call super().update() at the end of this
        function so that collision engines are updated accordingly.

        Parameters
        ----------
        time    :   float
            The time that the game has been running for. We can store this to do something every x amount of time.
        sprites :   SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        Returns
        -------
        None

        """
        if (time - self._last_shot_time) > 1.5:
            self._last_shot_time = time
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
                self.children[0].aim(*sprites.drill.position)
                self.children[0].shoot()

        if (time - self._last_pathfind_time) > 1:
            self._last_pathfind_time = time
            if self.has_line_of_sight_with(sprites.drill, sprites.all_blocks_list):
                self.path_to_position(sprites.drill.center_x, sprites.drill.center_y, sprites.destructible_blocks_list)

        super().update(time, sprites)
