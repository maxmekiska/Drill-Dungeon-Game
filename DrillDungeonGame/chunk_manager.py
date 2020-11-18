from __future__ import annotations
import arcade


from DrillDungeonGame.sprite_container import SpriteContainer
import numpy as np
from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.map.dungeon_generator import *


class Chunk:

    def __init__(self, chunk_matrix: list):
        self.chunk_matrix = chunk_matrix
        self.chunk_sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()) 
        self.load_chunk_sprites()
        self.chunk_center = self.get_chunk_center()

    def load_chunk_sprites(self):
        for row in self.chunk_matrix:
            for item in row:
                if item[0] == 'X':  # Dirt
                    wall_sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.16)
                    wall_sprite.center_x = item[1] 
                    wall_sprite.center_y = item[2]
                    self.chunk_sprites.dirt_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                    self.chunk_sprites.all_blocks_list.append(wall_sprite)
                if item[0] == 'C':  # Coal
                    wall_sprite = arcade.Sprite("resources/images/material/Coal_square.png", 0.03)
                    wall_sprite.center_x = item[1] 
                    wall_sprite.center_y = item[2]
                    self.chunk_sprites.coal_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                    self.chunk_sprites.all_blocks_list.append(wall_sprite)
                if item[0] == 'G':  # Gold
                    wall_sprite = arcade.Sprite("resources/images/material/Gold_square.png", 0.03)
                    wall_sprite.center_x = item[1] 
                    wall_sprite.center_y = item[2]
                    self.chunk_sprites.gold_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                    self.chunk_sprites.all_blocks_list.append(wall_sprite)
                if item[0] == 'O':  # Border block.
                    wall_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.18)
                    wall_sprite.center_x = item[1] 
                    wall_sprite.center_y = item[2]
                    self.chunk_sprites.border_wall_list.append(wall_sprite)
                    self.chunk_sprites.indestructible_blocks_list.append(wall_sprite)
                    self.chunk_sprites.all_blocks_list.append(wall_sprite)


    def get_chunk_center(self):
        """
        Returns the x, y coordinates of the center of the chunk
        """
        startX, startY = self.chunk_matrix[0][0][1], self.chunk_matrix[0][0][2]
        endX, endY = self.chunk_matrix[-1][-1][1], self.chunk_matrix[-1][-1][2]
        middleX = (endX + startX) / 2
        middleY = (endY + startY) / 2
        return (middleX, middleY)

class ChunkManager:

    def __init__(self, map_layer_matrix, number_of_chunks=64, chunk_side_length=16, number_of_active_chunks=9):
        self.chunks_dictionary = {}
        self.number_of_chunks = number_of_chunks
        self.chunk_side_length = chunk_side_length
        self.active_chunks = [0, 1, 2] #list of all currently active chunks by dict index
        self._load_chunks_from_map_config(map_layer_matrix)
        self.number_of_active_chunks = number_of_active_chunks

    def _update_chunks(self, drill_x, drill_y):
        """
        Checks all chunks to see if they should be activated/deactivated
        Checks for the nearest 9? Chunks or so and loads them in. Basically anything that could potentially be on screen soon, but can move this number based on need
        The nicer way of doing this would be to have some kind of k nearest neighbours approach,
        But hard coding it to only consider those within a certain x range would probably
        be faster
        """
        current_active_chunks = []
        for key in self.chunks_dictionary:
            chunkX, chunkY = self.chunks_dictionary[key].chunk_center
            if chunkX < drill_x + 800 and chunkX > drill_x - 800:
                if chunkY < drill_y + 800 and chunkY > drill_y - 800:
                    current_active_chunks.append(key)
        self.active_chunks = current_active_chunks


    def _load_chunks_from_map_config(self, map_layer_matrix):
        """
        Loads the chunks from a given map layer
        Needs to cut through the matrix and break it into chunks of appropriate
        size. This can be achieved by 1 - Finding number of chunks per row and then iterating
        it up in a similar way as the loading feature but in reverse
        """
        chunk_number = 0
        startX = 0
        startY = 0
        length_of_map_layer = len(map_layer_matrix)
        for i in range(self.number_of_chunks):
            current_chunk = self._load_single_chunk(startX, startY, map_layer_matrix)
            self.chunks_dictionary[i] = current_chunk
            startX += self.chunk_side_length
            if startX >= length_of_map_layer:
                startY += self.chunk_side_length 
                startX = 0

    def _load_single_chunk(self, startX, startY, map_layer_matrix, chunk_size=16):
        chunk_piece = []
        for i in range(startY, startY + chunk_size):
            chunk_piece.append(map_layer_matrix[i][startX : startX + chunk_size])
        return Chunk(chunk_piece)





