from __future__ import annotations
import arcade


from DrillDungeonGame.sprite_container import SpriteContainer
import numpy as np
from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.map.dungeon_generator import *


class Chunk:

    def __init__(self, chunk_matrix: list):
        self.chunk_matrix = chunk_matrix
        self.chunk_sprites = SpriteContainer(Drill(center_x=100,center_y=100), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()) 
        self.load_chunk_sprites()

    def load_chunk_sprites(self):
        for row in self.chunk_matrix:
            for item in row:
                if item[0] == 'X':  # Dirt
                    wall_sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.18)
                    wall_sprite.center_x = row[1] 
                    wall_sprite.center_y = row[2]
                    self.chunk_sprites.dirt_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                if item == 'C':  # Coal
                    wall_sprite = arcade.Sprite("resources/images/material/Coal_square.png", 0.03)
                    wall_sprite.center_x = row[1] 
                    wall_sprite.center_y = row[2]
                    self.chunk_sprites.coal_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                if item == 'G':  # Gold
                    wall_sprite = arcade.Sprite("resources/images/material/Gold_square.png", 0.03)
                    wall_sprite.center_x = row[1] 
                    wall_sprite.center_y = row[2]
                    self.chunk_sprites.gold_list.append(wall_sprite)
                    self.chunk_sprites.destructible_blocks_list.append(wall_sprite)
                if item == 'O':  # Border block.
                    wall_sprite = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.18)
                    wall_sprite.center_x = row[1] 
                    wall_sprite.center_y = row[2]
                    self.chunk_sprites.border_wall_list.append(wall_sprite)
                    self.chunk_sprites.indestructible_blocks_list.append(wall_sprite)

class ChunkManager:

    def __init__(self, map_layer_matrix, number_of_chunks=64, chunk_side_length=16):
        self.chunks_dictionary = {}
        self.number_of_chunks = number_of_chunks
        self.chunk_side_length = chunk_side_length
        self.active_chunks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] #list of all currently active chunks by dict index
        self._load_chunks_from_map_config(map_layer_matrix)

    def _update_chunks(self):
        """
        Checks all chunks to see if they should be activated/deactivated
        """
        pass

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





