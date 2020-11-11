from __future__ import annotations

import arcade
import math

from ..entity import Entity
from ..mixins import DiggingMixin, ShootingMixin, ControllableMixin


class Drill(Entity, ShootingMixin, DiggingMixin, ControllableMixin):
    def __init__(self, center_x=64, center_y=128, speed=0.5, ammunition=50, distance_moved=0, coal=100, gold=0):
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

    # def move_drill(self, direction):
    #     if direction == "UP":
    #         self.angle = 0
    #         self.set_velocity((0, self.speed))
    #     elif direction == "UPRIGHT":
    #         self.angle = 315
    #         self.set_velocity((self.speed/math.sqrt(2) * self.speed, self.speed/math.sqrt(2) * self.speed))
    #     elif direction == "DOWN":
    #         self.angle = 180
    #         self.set_velocity((0, -self.speed))
    #     elif direction == "DOWNRIGHT":
    #         self.angle = 225
    #         self.set_velocity((self.speed/math.sqrt(2) * self.speed, self.speed/math.sqrt(2) * -self.speed))
    #     elif direction == "LEFT":
    #         self.angle = 90
    #         self.set_velocity((-self.speed, 0))
    #     elif direction == "UPLEFT":
    #         self.angle = 45
    #         self.set_velocity((self.speed/math.sqrt(2) * -self.speed, self.speed/math.sqrt(2) * self.speed))
    #     elif direction == "RIGHT":
    #         self.angle = 270
    #         self.set_velocity((self.speed, 0))
    #     elif direction == "DOWNLEFT":
    #         self.angle = 135
    #         self.set_velocity((self.speed/math.sqrt(2) * -self.speed, self.speed/math.sqrt(2) * -self.speed))
    #
    #     # implement ammunition increment after every 200 units of movement
    #     # note: absolute values of x and y need to be summed because diagonal movement cancel distance out
    #     self.distance_moved += (abs(self.change_x) + abs(self.change_y))
    #     self.distance_moved = round(self.distance_moved, 1)
    #
    #     # reset counter after every 200 units of movement and increment ammunition by 1
    #     if self.distance_moved > 200:
    #         self.distance_moved = 0
    #         self.ammunition += 1
    #         self.coal -= 1

    # add coal removal
    def collect_coal(self, coal_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, coal_list)
            for coal in drill_hole_list:
                coal.remove_from_sprite_lists()
                self.coal += 1  # increment coal

    # add gold removal
    def collect_gold(self, gold_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, gold_list)
            for gold in drill_hole_list:
                gold.remove_from_sprite_lists()
                self.gold += 1  # increment gold
