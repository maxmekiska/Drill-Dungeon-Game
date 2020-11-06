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
        self.drill_list = None
        self.wall_list = None
        self.border_wall_list = None
        self.bullet_list = None

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
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) # spatial hash, makes collision detection faster
        self.border_wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list = arcade.SpriteList()

        #Initialize the map layer with some dungeon
        mapLayer = MapLayer(100, 100, meanDungeonSize=400)
        mapLayer.generate_blank_map()
        mapLayer.generate_dungeon()
        mapLayer.generate_dungeon()
        mapLayer.generate_dungeon()

        #Load map layer from mapLayer
        self.load_map_layer_from_matrix(mapLayer.mapLayerMatrix)

        drillSpriteImage="resources/images/drills/drill_v2_2.png"
        turretSpriteImage="resources/images/weapons/turret1.png"
        self.drill_list=Drill(drillSpriteImage, 0.3, turretSpriteImage, 0.12)
        self.drill_list.physicsEngineSetup(self.border_wall_list)

        #Set viewpoint boundaries - where the drill currently has scrolled to
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Draws the map
        """
        arcade.start_render()
        self.wall_list.draw()
        self.drill_list.draw()
        self.bullet_list.draw() 


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

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.drill_list.stopMoving()
        self.move_drill()

        self.drill_list.updatePhysicsEngine()
        #clears map to leave tunnel behind drill
        self.drill_list.clearDirt(self.wall_list)

        #Check for side scrolling
        self.update_map_view()

        #self.physics_engine.update()        
        self.bullet_list.update()
        

       
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            # remove bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            # remove hit wall    
            for wall in hit_list:
                wall.remove_from_sprite_lists()
            # later also add for enemies    
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

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

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.drill_list.aimTurret(x, y)

    def on_mouse_press(self, x, y, button, modifiers): # shooting/aiming
        # sprite scaling laser
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.4)
        
      
        start_x = self.drill_list.turret.center_x
        start_y = self.drill_list.turret.center_y 
        bullet.center_x = start_x
        bullet.center_y = start_y
        
        dest_x = x
        dest_y = y

       
        
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")
        
        #bullet speed at the end
        bullet.change_x = math.cos(angle) * 7
        bullet.change_y = math.sin(angle) * 7


        self.bullet_list.append(bullet)

    def update_map_view(self):
        #Check if the drill has reached the edge of the box
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
        """
        Would probably be cleaner to implement using a dictionary
        """
        if self.up_pressed and not (self.down_pressed or self.left_pressed or self.right_pressed):
            self.drill_list.moveDrill("UP")
        # move diagonal up right
        elif self.up_pressed and self.right_pressed and not (self.down_pressed or self.left_pressed):
            self.drill_list.moveDrill("UPRIGHT")
        # move down
        elif self.down_pressed and not (self.up_pressed or self.left_pressed or self.right_pressed):
            self.drill_list.moveDrill("DOWN")
        # move diagonal down right
        elif self.down_pressed and self.right_pressed and not (self.up_pressed or self.left_pressed):
            self.drill_list.moveDrill("DOWNRIGHT")
        # move left
        elif self.left_pressed and not (self.up_pressed or self.down_pressed or self.right_pressed):
            self.drill_list.moveDrill("LEFT")
        # move digonal up left
        elif self.left_pressed and self.up_pressed and not  ( self.down_pressed or self.right_pressed):
            self.drill_list.moveDrill("UPLEFT")
        # move right
        elif self.right_pressed and not (self.up_pressed or self.down_pressed or self.left_pressed):
            self.drill_list.moveDrill("RIGHT")
        # move digonal down left
        elif self.left_pressed and self.down_pressed and not  ( self.up_pressed or self.right_pressed):
            self.drill_list.moveDrill("DOWNLEFT")


    def check_for_scroll_left(self, changed):
        left_boundary = self.view_left + VIEWPOINT_MARGIN
        if self.drill_list.left() < left_boundary:
            self.view_left -= left_boundary - self.drill_list.left()
            changed = True
        return changed

    def check_for_scroll_right(self, changed):
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPOINT_MARGIN
        if self.drill_list.right() > right_boundary:
            self.view_left += self.drill_list.right() - right_boundary
            changed = True
        return changed

    def check_for_scroll_up(self, changed):
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPOINT_MARGIN
        if self.drill_list.top() > top_boundary:
            self.view_bottom += self.drill_list.top() - top_boundary
            changed = True
        return changed

    def check_for_scroll_down(self, changed):
        bottom_boundary = self.view_bottom + VIEWPOINT_MARGIN
        if self.drill_list.bottom() < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.drill_list.bottom()
            changed = True
        return changed






def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
