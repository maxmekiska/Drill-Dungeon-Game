from __future__ import annotations

from typing import Union, Dict

import arcade

from .bullets import BlueNormalBullet
from .shield import Shield
from .turret import Turret
from ..entity import Entity
from ..mixins.digging_mixin import DiggingMixin
from ..mixins.controllable_mixin import ControllableMixin
from ..mixins.shooting_mixin import ShotType
from ...inventory import Inventory


class Drill(Entity, DiggingMixin, ControllableMixin):
    """

    Represents the drill (the player) that the player can control.
    Has a turret entity as a child.

    Attributes
    ----------
    shield_enabled  : bool
        Whether or not the drill's shield is currently enabled or disabled.

    Methods
    -------
    handle_key_press_release(keys: Dict[str, bool])
        Key press or release logic.
    handle_mouse_click(button: int)
        Left or right mouse click logic.
    update(time: float, sprites)
        Specific update logic for drill.
    enable_shield()
        Enables the shield. Consumes coal at a steady rate and makes the drill untargetable while active.
    disable_shield()
        Disables the shield which stops coal consumption and makes you once again targetable.

    """
    def __init__(self, center_x: Union[float, int], center_y: Union[float, int],
                 speed: Union[float, int] = 1, angle: float = 0.0,
                 ammunition: int = -1, coal: int = -1, gold: int = -1,
                 distance_moved: Union[float, int] = 0,
                 current_health: Union[float, int] = -1, max_health: Union[float, int] = -1) -> None:
        """

        Parameters
        ----------
        center_x        :   Union[float, int]
            The starting x position in the map for this entity.
        center_y        :   Union[float, int]
            The starting y position in the map for this entity.
        speed           :   Union[float, int]
            The speed that entity can move at.
        angle           :   float
            The starting angle for this entity.
        ammunition      :   int
            The number of bullets that the drill starts with in its inventory. -1 means unlimited ammo.
        coal            :   int
            The amount of coal that the drill starts with in its inventory. -1 means unlimited.
        gold            :   int
            The amount of gold that the drill starts with in its inventory. -1 means unlimited.
        distance_moved  :   Union[float, int]
            The distance that the drill has moved. This is useful when drilling up/down and reloading the map.
        current_health  :   float
            The starting health for this entity.  -1 means invincible.
        max_health
            The maximum amount of health that this entity can have. -1 means unlimited.

        """
        base_sprite: str = "resources/images/drills/drill_v2_2.png"
        turret_sprite: str = "resources/images/weapons/turret1.png"
        sprite_scale = 0.3
        turret_scale = 0.2
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle,
                         current_health=current_health, max_health=max_health)

        self.inventory = Inventory(gold=gold, coal=coal, ammunition=ammunition)
        self.children.append(Turret(turret_sprite, turret_scale, parent=self, bullet_type=BlueNormalBullet,
                                    firing_mode=ShotType.SINGLE))
        self.distance_moved = distance_moved
        self.shield_enabled = False
        self._total_shield_uptime = 0.0  # Store the time the shield has been on for coal consumption purposes.
        self._shield_duration = 6.0
        self._max_shield_duration = 12.0
        self.shield_cooldown_enabled = False
        self._shield_cooldown_duration = 2.0
        self._shield_cooldown_uptime = 0.0
        self._shield_sprite = Shield("resources/images/shield/blue_aura.png", 0.9, parent=self, relative_x=4)

    def draw_shield_bar(self, position_x, position_y, width, height):
        """Draws a shield health below the drill when shield activated."""
        level_width = (self._shield_duration/self._max_shield_duration)*width
        position_x = position_x - width/2 + level_width/2
        arcade.draw_rectangle_filled(
            position_x, position_y, level_width, height, arcade.color.WHITE
        )
        status_width = ((self._shield_duration-self._total_shield_uptime) / self._shield_duration) * level_width
        arcade.draw_rectangle_filled(
            position_x - (level_width / 2 - status_width / 2),
            position_y,
            status_width,
            height,
            arcade.color.BLUE,
        )
        arcade.draw_rectangle_outline(
            position_x,
            position_y,
            level_width,
            height,
            arcade.color.BLACK,
            border_width=1.5
        )

    def handle_key_press_release(self, keys: Dict[str, bool]) -> None:
        """

        Called when a key is pressed or released.
        Passes W A S D movement to the ControllableMixin and processes drill specific control (change firing mode) here.

        Parameters
        ----------
        keys    :   Dict[str, bool]
            A dictionary of all keys and a bool corresponding to whether it is pressed or not.

        """
        ControllableMixin.handle_key_press_release(self, keys)

        if keys['B']:
            # Change firing mode.
            if self.children[0].firing_mode == ShotType.BUCKSHOT:
                self.children[0].firing_mode = ShotType.SINGLE
            elif self.children[0].firing_mode == ShotType.SINGLE:
                self.children[0].firing_mode = ShotType.BUCKSHOT

    def handle_mouse_click(self, button: int) -> None:
        """

        Called when left or right mouse buttons are pressed. Left click shoots. Right click enables shield.

        Parameters
        ----------
        button  :   int
            The button pressed. 1 = Left click, 4 = Right click.

        """
        ControllableMixin.handle_mouse_click(self, button)
        if button == 1:  # Left click
            self.children[0].pull_trigger()
        elif button == 4:  # Right click
            if self.inventory.coal >= 1:
                self.enable_shield()

    def handle_mouse_release(self, button: int) -> None:
        """

        Called when left or right mouse buttons are released. Currently disables shield when right click is released.

        Parameters
        ----------
        button  :   int
            The button released. 1 = Left click, 4 = Right click.

        """
        ControllableMixin.handle_mouse_release(self, button)
        if button == 1:  # Left click
            self.children[0].release_trigger()
        elif button == 4:  # Right click release.
            self.disable_shield()

    def enable_shield(self) -> None:
        """

        Enables the shield. Consumes coal at a steady rate and makes the drill untargetable while active.

        """
        self.shield_enabled = True
        self.children.append(self._shield_sprite)
        self.inventory.coal -= 1  # Immediately remove one coal from the inventory when enabled.

    def disable_shield(self) -> None:
        """

        Disables the shield which stops coal consumption and makes you once again targetable.

        """
        self.shield_enabled = False
        if self._shield_sprite in self.children:
            self.children.remove(self._shield_sprite)

    def hurt(self, damage: Union[float, int]) -> None:
        """

        Override the functionality of hurt function to not damage the drill if the shield is active.

        See Also
        --------
        Entity.hurt

        Parameters
        ----------
        damage : Union[float, int]
            The amount of damage to deal to this entity.

        """
        if not self.shield_enabled:
            super().hurt(damage)

    def update(self, time: float, delta_time: float, sprites, block_grid) -> None:
        """
        Handles update logic specific to this Drill Entity. Currently increases the distance the drill has moved
        every game loop iteration so that we can decrease the amount of coal over time.

        Note
        ----
        As this function is implemented in an Entity subclass, we need to call super().update() at the end of this
        function so that collision engines are updated accordingly.

        Parameters
        ----------
        time       : float
            The time that the game has been running for. We can store this to do something every x amount of time.
        delta_time : float
            The time in seconds since the last game loop iteration.
        sprites    : SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.
        block_grid : BlockGrid
            Reference to all blocks in the game.

        """
        self.distance_moved += abs(self.change_x) + abs(self.change_y)
        if self.distance_moved > 200:
            self.distance_moved = 0.0
            self.inventory.ammunition += 1
            self.inventory.coal -= 1

        if self.shield_enabled:
            self.shield_cooldown_enabled = True
            self._shield_cooldown_uptime = 0.0
            self._total_shield_uptime += delta_time
            if self._total_shield_uptime > self._shield_duration:
                self.disable_shield()
        elif not self.shield_enabled and self._total_shield_uptime>0 and not self.shield_cooldown_enabled:
            self._total_shield_uptime -= delta_time

        if self.shield_cooldown_enabled:
            if self._shield_cooldown_uptime < self._shield_cooldown_duration:
                self._shield_cooldown_uptime += delta_time
            else:
                self._shield_cooldown_uptime = 0.0
                self.shield_cooldown_enabled = False

        if self.inventory.coal < 1:
            self.disable_shield()
            self.stop_moving()

        # If we do end up updating this in an entity subclass, we need to call super.update() so mixins get updated.
        super().update(time, delta_time, sprites, block_grid)
