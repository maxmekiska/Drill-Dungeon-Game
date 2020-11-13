from __future__ import annotations

import arcade
import math

from ..entity import Entity
from ..mixins.digging_mixin import DiggingMixin
from ..mixins.shooting_mixin import ShootingMixin
from ..mixins.controllable_mixin import ControllableMixin


class Drill(Entity, ShootingMixin, DiggingMixin, ControllableMixin):
    def __init__(self, center_x=64, center_y=128, speed=1, ammunition=50, distance_moved=0, coal=100, gold=0):
        base_sprite: str = "resources/images/drills/drill_v2_2.png"
        turret_sprite: str = "resources/images/weapons/turret1.png"
        sprite_scale = 0.3
        turret_scale = 0.2
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed)
        ShootingMixin.__init__(self, turret_sprite, turret_scale, center_x, center_y)

        self.ammunition = ammunition
        self.coal = coal
        self.gold = gold
        self.distance_moved = distance_moved

    def collect_coal(self, coal_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, coal_list)
            for coal in drill_hole_list:
                coal.remove_from_sprite_lists()
                self.coal += 1  # We found coal!

    # add gold removal
    def collect_gold(self, gold_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, gold_list)
            for gold in drill_hole_list:
                gold.remove_from_sprite_lists()
                self.gold += 1  # We found gold!

    def update(self, time: float, sprites) -> None:
        self.collect_coal(sprites.coal_list)
        self.collect_gold(sprites.gold_list)

        self.distance_moved += abs(self.change_x) + abs(self.change_y)
        if round(self.distance_moved) > 200:
            self.distance_moved = 0
            self.ammunition += 1
            self.coal -= 1

        # If we do end up updating this in an entity subclass, we need to call super.update() so mixins get updated.
        super().update(time, sprites)
