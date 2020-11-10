from __future__ import annotations
import typing
import arcade
import math


from .enemy import Enemy
from .mixins import PathFindingMixin


class SpaceshipEnemy(Enemy, PathFindingMixin):
    def __init__(self, sprite_image: str, sprite_scale: float, turret_sprite: str, turret_sprite_scale: float,
                 pos_x: int, pos_y: int, vision: typing.Union[float, int], speed: typing.Union[float, int] = 1) -> None:
        super().__init__(sprite_image, sprite_scale, pos_x, pos_y, speed)
        self.turret = arcade.Sprite(turret_sprite, turret_sprite_scale)
        self.turret.center_x = pos_x
        self.turret.center_y = pos_y
        self.sprite_list.append(self.turret)

        self.speed = speed
        self.vision = vision
        self.physics_engines = []

    def aim_turret(self, x, y):
        start_x = self.turret.center_x
        start_y = self.turret.center_y
        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        self.turret.angle = math.degrees(math.atan2(y_diff, x_diff)) - 90
        self.body.change_x = self.speed
    #
    # def move(self, direction):
    #     """
    #     direction_list = ["UP", "UPRIGHT", "DOWN", "DOWNRIGHT", "LEFT", "RIGHT", "UPLEFT", "DOWNLEFT"]
    #     if (direction in direction_list):
    #         self.body.left = random.randint(self.width, self.width + 80)
    #         self.body.top = random.randint(10, self.height - 10)
    #     """
    #     if direction == "UP":
    #         self.body.angle = 0
    #         self.body.change_y = self.speed
    #         self.turret.change_y = self.speed
    #     elif direction == "UPRIGHT":
    #         self.body.angle = 315
    #         self.body.change_x = 0.5 * self.speed
    #         self.turret.change_x = 0.5 * self.speed
    #         self.body.change_y = 0.5 * self.speed
    #         self.turret.change_y = 0.5 * self.speed
    #     elif direction == "DOWN":
    #         self.body.angle = 180
    #         self.body.change_y = -self.speed
    #         self.turret.change_y = -self.speed
    #     elif direction == "DOWNRIGHT":
    #         self.body.angle = 225
    #         self.body.change_x = 0.5 * self.speed
    #         self.turret.change_x = 0.5 * self.speed
    #         self.body.change_y = 0.5 * -self.speed
    #         self.turret.change_y = 0.5 * -self.speed
    #     elif direction == "LEFT":
    #         self.body.angle = 90
    #         self.body.change_x = -self.speed
    #         self.turret.change_x = -self.speed
    #     elif direction == "UPLEFT":
    #         self.body.angle = 45
    #         self.body.change_x = 0.5 * -self.speed
    #         self.turret.change_x = 0.5 * -self.speed
    #         self.body.change_y = 0.5 * self.speed
    #         self.turret.change_y = 0.5 * self.speed
    #     elif direction == "RIGHT":
    #         self.body.angle = 270
    #         self.body.change_x = self.speed
    #         self.turret.change_x = self.speed
    #     elif direction == "DOWNLEFT":
    #         self.body.angle = 135
    #         self.body.change_x = 0.5 * -self.speed
    #         self.turret.change_x = 0.5 * -self.speed
    #         self.body.change_y = 0.5 * -self.speed
    #         self.turret.change_y = 0.5 * -self.speed
