# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:12:48 2020

"""

import random
import arcade
from utils.drill import *
from utils.dungeon_generator import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MAP_WIDTH = 2400
MAP_HEIGHT = 2400
SCREEN_TITLE = "Welcome to the Drill Dungeon"

VIEWPOINT_MARGIN = 40


class DrillDungeonGame(arcade.Window):
    """
    Basic map class
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Sprite variables
        self.player_drill = None

        self.player_list = None
        self.wall_list = None
        self.border_wall_list = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        
        #Initialize scrolling variables
        self.view_bottom = 0
        self.view_left = 0


        arcade.set_background_color(arcade.color.BROWN_NOSE)
    def setup(self):
        """
        Set up game and initialize variables
        """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) # spatial hash, makes collision detection faster
        self.border_wall_list = arcade.SpriteList(use_spatial_hash=True)

        #Initialize the map layer with some dungeon
        mapLayer = MapLayer(100, 100, meanDungeonSize=400)
        mapLayer.generate_blank_map()
        mapLayer.generate_dungeon()
        mapLayer.generate_dungeon()
        mapLayer.generate_dungeon()

        #Load map layer from mapLayer
        self.load_map_layer_from_matrix(mapLayer.mapLayerMatrix)

        self.player_drill = Drill("resources/images/drills/drill_v2.png")
        self.player_list.append(self.player_drill)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_drill, self.border_wall_list)

        #Set viewpoint boundaries - where the drill currently has scrolled to
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Draws the map
        """
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()


    def load_map_layer_from_matrix(self, mapLayerMatrix):
        """
        Loads a map from a layer matrix
        """
        mapLayerHeight = len(mapLayerMatrix)
        mapLayerWidth = len(mapLayerMatrix[0])
        blockHeight = MAP_HEIGHT / mapLayerHeight
        blockWidth = MAP_WIDTH / mapLayerWidth
        y = 0.5 * blockHeight #this is probably the center of the block so needs to be height/2
        for row in mapLayerMatrix:
            self.fill_row_with_terrain(row, y, blockWidth, blockHeight)
            y += blockHeight

    def fill_row_with_terrain(self, mapRow, y, blockWidth, blockHeight):
        """
        Fills a row with terrain
        list mapRow        : a row of the map matrix
        int y              : the y position of the row
        int blockWidth     : width of the blocks to fill the terrain
        int blockHeight    : height of the blocks to fill the terrain
        """
        x = 0.5 * blockWidth
        for item in mapRow:
            if item == 'X':
                wallsprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.18)
                #wallsprite.width = blockWidth 
                #wallsprite.height = blockHeight
                wallsprite.center_x = x
                wallsprite.center_y = y
                self.wall_list.append(wallsprite)
            x += blockWidth  

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

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player_drill.change_x = 0
        self.player_drill.change_y = 0
        
        self.move_drill()

        self.physics_engine.update()

        drill_hole_list = arcade.check_for_collision_with_list(self.player_drill, self.wall_list)
        for dirt in drill_hole_list:
            dirt.remove_from_sprite_lists()

        #Check for side scrolling
        self.update_map_view()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def update_map_view(self):
        changed = False
        changed = self.check_for_scroll_left(changed)
        changed = self.check_for_scroll_right(changed)
        changed = self.check_for_scroll_up(changed)
        changed = self.check_for_scroll_down(changed)

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if changed:
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


    def move_drill(self):
        if self.up_pressed and not (self.down_pressed or self.left_pressed or self.right_pressed): 
            self.player_drill.angle = 0
            self.player_drill.change_y = self.player_drill.drillSpeed
            
        # move diagonal up right  
        elif self.up_pressed and self.right_pressed and not (self.down_pressed or self.left_pressed):
            self.player_drill.angle = 315
            self.player_drill.change_x = 0.5 * self.player_drill.drillSpeed
            self.player_drill.change_y = 0.5 * self.player_drill.drillSpeed
            
        # move down    
        elif self.down_pressed and not (self.up_pressed or self.left_pressed or self.right_pressed):
            self.player_drill.angle = 180
            self.player_drill.change_y = -self.player_drill.drillSpeed
           
        # move diagonal down right
        elif self.down_pressed and self.right_pressed and not (self.up_pressed or self.left_pressed):
            self.player_drill.angle = 225
            self.player_drill.change_x = 0.5 * self.player_drill.drillSpeed
            self.player_drill.change_y = 0.5 * -self.player_drill.drillSpeed
            
        # move left       
        elif self.left_pressed and not (self.up_pressed or self.down_pressed or self.right_pressed):
            self.player_drill.angle = 90
            self.player_drill.change_x = -self.player_drill.drillSpeed
        
        # move digonal up left
        elif self.left_pressed and self.up_pressed and not  ( self.down_pressed or self.right_pressed):
            self.player_drill.angle = 45
            self.player_drill.change_x = 0.5 * -self.player_drill.drillSpeed
            self.player_drill.change_y = 0.5 * self.player_drill.drillSpeed
        
        # move right
        elif self.right_pressed and not (self.up_pressed or self.down_pressed or self.left_pressed):
            self.player_drill.angle = 270
            self.player_drill.change_x = self.player_drill.drillSpeed
            
        # move digonal down left
        elif self.left_pressed and self.down_pressed and not  ( self.up_pressed or self.right_pressed):
            self.player_drill.angle = 135
            self.player_drill.change_x = 0.5 * -self.player_drill.drillSpeed
            self.player_drill.change_y = 0.5 * -self.player_drill.drillSpeed




    def check_for_scroll_left(self, changed):
        left_boundary = self.view_left + VIEWPOINT_MARGIN
        if self.player_drill.left < left_boundary:
            self.view_left -= left_boundary - self.player_drill.left
            changed = True
        return changed

    def check_for_scroll_right(self, changed):
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPOINT_MARGIN
        if self.player_drill.right > right_boundary:
            self.view_left += self.player_drill.right - right_boundary
            changed = True
        return changed

    def check_for_scroll_up(self, changed):
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPOINT_MARGIN
        if self.player_drill.top > top_boundary:
            self.view_bottom += self.player_drill.top - top_boundary
            changed = True
        return changed

    def check_for_scroll_down(self, changed):
        bottom_boundary = self.view_bottom + VIEWPOINT_MARGIN
        if self.player_drill.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_drill.bottom
            changed = True
        return changed






def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
