from __future__ import annotations

import arcade
import math

from .entity import Entity


class Drill(Entity):
    def __init__(self, base_sprite, sprite_scale, turret_sprite, turret_scale, pos_x=64, pos_y=128, speed=1,
                 ammunition=50, distance_moved=0, coal=100, gold=0):
        super().__init__(base_sprite, sprite_scale, pos_x, pos_y, speed)
        self.turret = arcade.Sprite(turret_sprite, turret_scale)
        self.turret.center_x = pos_x
        self.turret.center_y = pos_y

        self.sprite_list.extend([self.turret])

        self.physicsEngines = []
        self.ammunition = ammunition
        self.coal = coal
        self.gold = gold

        self.distance_moved = distance_moved

    def move_drill(self, direction):
        if direction == "UP":
            self.body.angle = 0
            self.body.change_y = self.speed
        elif direction == "UPRIGHT":
            self.body.angle = 315
            self.body.change_x = self.speed/math.sqrt(2) * self.speed
            self.body.change_y = self.speed/math.sqrt(2) * self.speed
        elif direction == "DOWN":
            self.body.angle = 180
            self.body.change_y = -self.speed
        elif direction == "DOWNRIGHT":
            self.body.angle = 225
            self.body.change_x = self.speed/math.sqrt(2) * self.speed
            self.body.change_y = self.speed/math.sqrt(2) * -self.speed
        elif direction == "LEFT":
            self.body.angle = 90
            self.body.change_x = -self.speed
        elif direction == "UPLEFT":
            self.body.angle = 45
            self.body.change_x = self.speed/math.sqrt(2) * -self.speed
            self.body.change_y = self.speed/math.sqrt(2) * self.speed
        elif direction == "RIGHT":
            self.body.angle = 270
            self.body.change_x = self.speed
        elif direction == "DOWNLEFT":
            self.body.angle = 135
            self.body.change_x = self.speed/math.sqrt(2) * -self.speed
            self.body.change_y = self.speed/math.sqrt(2) * -self.speed

        # implement ammunition increment after every 200 units of movement
        # note: absolute values of x and y need to be summed because diagonal movement cancel distance out
        self.distance_moved += (abs(self.body.change_x) + abs(self.body.change_y))
        self.distance_moved = round(self.distance_moved, 1)

        # reset counter after every 200 units of movement and increment ammunition by 1
        if self.distance_moved > 200:
            self.distance_moved = 0
            self.ammunition += 1
            self.coal -= 1

    def physics_engine_setup(self, engine_wall):
        for item in self.sprite_list:
            self.physicsEngines.append(arcade.PhysicsEngineSimple(item, engine_wall))

    def draw(self):
        self.turret.center_x = self.body.center_x
        self.turret.center_y = self.body.center_y
        for item in self.sprite_list:
            item.draw()

    def update_physics_engine(self):
        for engine in self.physicsEngines:
            engine.update()

    def clear_dirt(self, dirt_wall_list):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, dirt_wall_list)
            for dirt in drill_hole_list:
                dirt.remove_from_sprite_lists()

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

    def aim_turret(self, pos_x, pos_y):

        start_x = self.turret.center_x
        start_y = self.turret.center_y
        dest_x = pos_x
        dest_y = pos_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        self.turret.angle = math.degrees(math.atan2(y_diff, x_diff))-90
