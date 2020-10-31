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
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) # spatial hash, makes collision detection faster
        #self.generate_random_walls()
        self.fill_map_with_terrain()
       
    def on_draw(self):
        """print map"""
        arcade.start_render()
        self.wall_list.draw()

    def fill_map_with_terrain(self, blockWidth=20, blockHeight=20):
        """
        Fills the terrain with blocks. Requires that the block width/height be a
        multiple of the screen width and height or it will end up looking strange
        """
        numberOfBlocksX = int(SCREEN_WIDTH / blockWidth)
        numberOfBlocksY = int(SCREEN_HEIGHT / blockHeight) 
        x = 0
        y = 0
        for i in range(numberOfBlocksX + 1):
            self.fill_column_with_terrain(x, numberOfBlocksY, blockWidth,  blockHeight)
            x += blockWidth 

    def fill_column_with_terrain(self, x, numberOfBlocksY, blockWidth, blockHeight):
        """
        Fills a column with terrain
        int x              : the x position of the column
        int numberOfWallsY : number of blocks required to fill the columns
        """
        y = 0
        for j in range(numberOfBlocksY + 1):
            wallsprite = arcade.Sprite(":resources:images/tiles/grassCenter.png")
            wallsprite.width = blockWidth 
            wallsprite.height = blockHeight
            wallsprite.center_x = x
            wallsprite.center_y = y
            self.wall_list.append(wallsprite)
            y += blockHeight 

    def generate_random_walls(self, numberOfWalls=10, sizeOfWalls=10):
        """
        Generates random walls
        int numberOfWalls : Number of walls to add
        int sizeOfWalls   : The length of each wall (number of blocks)
        """
        for j in range(10):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            for i in range(10):
                wallsprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.1)
                wallsprite.center_x = x + i* wallsprite.width 
                wallsprite.center_y = y + i* wallsprite.height 
                self.wall_list.append(wallsprite) 






def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
