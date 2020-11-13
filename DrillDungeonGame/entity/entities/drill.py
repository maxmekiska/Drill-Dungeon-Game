from __future__ import annotations

from ..entity import Entity
from ..mixins.digging_mixin import DiggingMixin
from ..mixins.shooting_mixin import ShootingMixin
from ..mixins.controllable_mixin import ControllableMixin
from ...inventory import Inventory


class Drill(Entity, ShootingMixin, DiggingMixin, ControllableMixin):
    def __init__(self, center_x=64, center_y=128, speed=1, ammunition=50, distance_moved=0, coal=100, gold=0):
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
