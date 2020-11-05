"""
Module to create drill and control its specifications
such as speed.
"""

import arcade
import math

class Drill():

    def __init__(self, drillSpriteImage, drillSpriteScale, turretSpriteImage, turretSpriteScale, startPositionX=64, startPositionY=128, drillSpeed=1):
        self.body = arcade.Sprite(drillSpriteImage, drillSpriteScale)
        self.body.center_x = startPositionX
        self.body.center_y = startPositionY

        self.turret = arcade.Sprite(turretSpriteImage, turretSpriteScale)
        self.turret.center_x = startPositionX
        self.turret.center_y = startPositionY

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.extend([self.body, self.turret])

        self.drillSpeed = drillSpeed
        self.physicsEngines = []

    def stopMoving(self):
        for item in self.sprite_list:
            item.change_x = 0
            item.change_y = 0

    def moveDrill(self, direction):
        if direction == "UP":
            self.body.angle = 0
            self.body.change_y = self.drillSpeed
            self.turret.change_y = self.drillSpeed
        elif direction == "DOWN":
            self.body.angle = 180
            self.body.change_y = -self.drillSpeed
            self.turret.change_y = -self.drillSpeed
        elif direction == "LEFT":
            self.body.angle = 90
            self.body.change_x = -self.drillSpeed
            self.turret.change_x = -self.drillSpeed
        elif direction == "RIGHT":
            self.body.angle = 270
            self.body.change_x = self.drillSpeed
            self.turret.change_x = self.drillSpeed


    def physicsEngineSetup(self, engineWall):
        for item in self.sprite_list:
            self.physicsEngines.append(arcade.PhysicsEngineSimple(item, engineWall))

    def draw(self):
        for item in self.sprite_list:
            item.draw()

    def updatePhysicsEngine(self):
        for engine in self.physicsEngines:
          engine.update()

    def clearDirt(self, dirtWallList):
        for item in self.sprite_list:
            drill_hole_list = arcade.check_for_collision_with_list(item, dirtWallList)
            for dirt in drill_hole_list:
                dirt.remove_from_sprite_lists()

    def aimTurret(self, aimX, aimY):
        start_x = self.turret.center_x
        start_y = self.turret.center_y
        dest_x = aimX
        dest_y = aimY

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        self.turret.angle = math.degrees(math.atan2(y_diff, x_diff))-90

    def top(self):
        return self.body.top
    def bottom(self):
        return self.body.bottom
    def left(self):
        return self.body.left
    def right(self):
        return self.body.right
