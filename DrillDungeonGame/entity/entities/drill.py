from __future__ import annotations

from typing import Union

from ..entity import Entity
from ..mixins.digging_mixin import DiggingMixin
from ..mixins.shooting_mixin import ShootingMixin
from ..mixins.controllable_mixin import ControllableMixin
from ..inventory import Inventory


class Drill(Entity, ShootingMixin, DiggingMixin, ControllableMixin):
    def __init__(self, center_x: Union[float, int] = 64, center_y: Union[float, int] = 128,
                 speed: Union[float, int] = 1, ammunition: int = 50, distance_moved: Union[float, int] = 0,
                 coal: int = 100, gold: int = 0) -> None:
        base_sprite: str = "resources/images/drills/drill_v2_2.png"
        turret_sprite: str = "resources/images/weapons/turret1.png"
        sprite_scale = 0.3
        turret_scale = 0.2
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed)
        ShootingMixin.__init__(self, turret_sprite, turret_scale, center_x, center_y)

        self.inventory = Inventory(gold=gold, coal=coal, ammunition=ammunition)
        self.distance_moved = distance_moved

    def update(self, time: float, sprites) -> None:
        self.distance_moved += abs(self.change_x) + abs(self.change_y)
        if self.distance_moved > 200:
            self.distance_moved = 0
            self.inventory.ammunition += 1
            self.inventory.coal -= 1

        # If we do end up updating this in an entity subclass, we need to call super.update() so mixins get updated.
        super().update(time, sprites)
