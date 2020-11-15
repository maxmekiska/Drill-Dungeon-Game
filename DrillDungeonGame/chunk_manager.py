from __future__ import annotations


from sprite_container.py import SpriteContainer
import numpy as np
from map.dungeon_generator import *


mapLayer = MapLayer()
mapLayer.generate_blank_map()

cmanager = ChunkManager(mapLayer.mapLayerMatrix)
cmanager._load_chunks_from_map_config(mapLayer.mapLayerMatrix, 25)

class Chunk:

    def __init__(self, chunk_matrix: list, chunk_sprites: SpriteContainer, x_boundaries: tuple, y_boundaries: tuple):
        self.chunk_matrix = chunk_matrix
        self.chunk_sprites = chunk_sprites
        self.x_boundaries = x_boundaries
        self.y_boundaries = y_boundaries

class ChunkManager:

    def __init__(self, map_layer_matrix, number_of_chunks=20):
        self.chunks_dictionary = {}
        self.map_layer_configuration = self.load_map_layer_from_matrix(map_layer_matrix)

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
        map_layer_height = len(map_layer_matrix)
        map_layer_width = len(map_layer_matrix[0])
        chunk_height = int(map_layer_height / np.sqrt(n_chunks))
        chunk_width = int(map_layer_width / np.sqrt(n_chunks))
        x_start = 0
        y_start = 0
        for i in range(n_chunks):
            current_chunk = self._load_single_chunk(map_layer_matrix, x_start, y_start, chunk_height, chunk_width)
            self.chunks_dictionary[i] = current_chunk
            x_start += chunk_width
            if x_start > map_layer_height:
                y_start += chunk_height
                x_start = 0

        

    def _load_single_chunk(self, map_layer_matrix, x_start, y_start, chunk_height, chunk_width):
        """
        Returns a single chunk
        """
        chunk = []
        for i in range(y_start, chunk_height + y_start - 1):
            chunk_row = map_layer_matrix[i][x_start : x_start + chunk_width - 1]
            chunk.append(chunk_row)
        return chunk

    def load_map_layer_from_matrix(self, map_layer_matrix) -> None:
        map_layer_height = len(map_layer_matrix)
        map_layer_width = len(map_layer_matrix[0])
        block_height = MAP_HEIGHT / map_layer_height
        block_width = MAP_WIDTH / map_layer_width
        y_block_center = 0.5 * block_height
        map_layer_configuration = []
        for row in map_layer_matrix:
            map_layer_configuration.append(self.load_row_from_matrix(row, y_block_center, block_width, block_height))
            y_block_center += block_height
            

    def load_row_from_matrix(self, row, y_block_center, block_width, block_height) -> list:
        x_block_center = 0.5 * block_width
        configuration_row = []
        for item in row:
            configuration_row.append((item, x_block_center, y_block_center))
            x_block_center += block_width








