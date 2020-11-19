from __future__ import annotations

from typing import Union, Dict

from .bullets import BlueNormalBullet
from .turret import Turret
from ..entity import Entity
from ..mixins.digging_mixin import DiggingMixin
from ..mixins.controllable_mixin import ControllableMixin
from ..mixins.shooting_mixin import ShotType
from ...inventory import Inventory


class Drill(Entity, DiggingMixin, ControllableMixin):
    def __init__(self, center_x: Union[float, int], center_y: Union[float, int],
                 speed: Union[float, int] = 1, angle: float = 0.0, ammunition: int = -1, coal: int = -1, gold: int = -1,
                 distance_moved: Union[float, int] = 0, health: Union[float, int] = -1) -> None:
        base_sprite: str = "resources/images/drills/drill_v2_2.png"
        turret_sprite: str = "resources/images/weapons/turret1.png"
        sprite_scale = 0.3
        turret_scale = 0.2
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle, health=health)

        self.inventory = Inventory(gold=gold, coal=coal, ammunition=ammunition)
        self.children.append(Turret(turret_sprite, turret_scale, parent=self, bullet_type=BlueNormalBullet,
                                    firing_mode=ShotType.SINGLE))
        self.distance_moved = distance_moved

    def handle_key_press_release(self, keys: Dict[str, bool]) -> None:
        ControllableMixin.handle_key_press_release(self, keys)

        if keys['B']:
            # Change firing mode.
            if self.children[0].firing_mode == ShotType.BUCKSHOT:
                self.children[0].firing_mode = ShotType.SINGLE
            elif self.children[0].firing_mode == ShotType.SINGLE:
                self.children[0].firing_mode = ShotType.BUCKSHOT

    def handle_mouse_click(self, button: int) -> None:
        ControllableMixin.handle_mouse_click(self, button)
        if button == 1:  # Left click
            self.children[0].shoot()
        elif button == 4:  # Right click
            pass
            # TODO enable shield.

    def update(self, time: float, sprites) -> None:
        self.distance_moved += abs(self.change_x) + abs(self.change_y)
        if self.distance_moved > 200:
            self.distance_moved = 0
            self.inventory.ammunition += 1
            self.inventory.coal -= 1

        # If we do end up updating this in an entity subclass, we need to call super.update() so mixins get updated.
        super().update(time, sprites)
