"""
Module to create drill and control its specifications
such as speed.
"""

import arcade
class Drill(arcade.Sprite):

    def __init__(self, spriteImage, drillSpeed=2, scale=1, startPositionX=64, startPositionY=128):
        super().__init__()
        self.spriteImage = spriteImage
        self.drillSpeed = drillSpeed
        self.scale = scale
        self.center_x = startPositionX
        self.center_y = startPositionY

        self.texture = arcade.load_texture_pair(spriteImage)[0]
        self.hit_box = self.texture.hit_box_points

    def setup(self, arcade):

        return arcade.Sprite(self.spriteImage, self.scale)


    def changeDrillSpeed(self, newSpeed):
        """

        """
        self.drillSpeed = newSpeed
