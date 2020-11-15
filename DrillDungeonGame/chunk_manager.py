from __future__ import annotations


from sprite_container import SpriteContainer
import numpy as np
from map.dungeon_generator import *


mapLayer = MapLayer()
mapLayer.generate_blank_map()


class Chunk:

    def __init__(self, chunk_matrix: list, chunk_sprites: SpriteContainer, x_boundaries: tuple, y_boundaries: tuple):
        self.chunk_matrix = chunk_matrix
        self.chunk_sprites = chunk_sprites
        self.x_boundaries = x_boundaries
        self.y_boundaries = y_boundaries

class ChunkManager:

    def __init__(self, map_layer_matrix, number_of_chunks=64):
        self.chunks_dictionary = {}

    def _update_chunks(self):
        """
        Checks all chunks to see if they should be activated/deactivated
        """
        pass

    def load_chunk(self):
        """
        Draws a chunk based on its current configuration
        """
        pass

    def deload_chunk(self):
        """
        Removes a chunk from the map
        """
        pass

    def _load_chunks_from_map_config(self, map_layer_matrix, n_chunks):
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
        for i in range(n_chunks):
            current_chunk = self._load_single_chunk(startX, startY, map_layer_matrix)
            self.chunks_dictionary[i] = current_chunk
            startX += 16
            if startX >= length_of_map_layer:
                startY += 16
                startX = 0

    def _load_single_chunk(self, startX, startY, map_layer_matrix, chunk_size=16):
        chunk_piece = []
        for i in range(startY, startY + chunk_size):
            chunk_piece.append(map_layer_matrix[i][startX : startX + chunk_size])
        return chunk_piece




mapLayer.generate_map_layer_configuration()

cmanager = ChunkManager(mapLayer.map_layer_configuration)
cmanager._load_chunks_from_map_config(mapLayer.map_layer_configuration, 64)
print((cmanager.chunks_dictionary[1]))





