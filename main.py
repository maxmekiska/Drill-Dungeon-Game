# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:12:48 2020

"""
  
import random
import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Welcome to the Drill Dungeon"


class DrillDungeonGame(arcade.Window):
    """ 
    Basic map class
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Sprite variables
        self.player_drill = None
        self.wall_list = None # generates walls inside of map

        
        arcade.set_background_color(arcade.color.BROWN_NOSE)
    def setup(self):
        """
        Set up game and initialize variables
        """
        self.wallsprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.1)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) # spatial hash, makes collision detection faster
        
        x = 50
        y = 350
        
        # function introduces random walls
        
        for j in range(10):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            for i in range(10):
                wallsprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.1)
                wallsprite.center_x = x + i* wallsprite.width 
                wallsprite.center_y = y + i* wallsprite.height 
                self.wall_list.append(wallsprite) 

        
        
        #self.wallsprite.center_x = 50
        #self.wallsprite.center_y = 350
        
        self.wall_list.append(self.wallsprite)
        
    def on_draw(self):
        """print map"""
        arcade.start_render()
        self.wall_list.draw()




def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
