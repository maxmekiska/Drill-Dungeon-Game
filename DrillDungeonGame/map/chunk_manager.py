from __future__ import annotations
import arcade


from DrillDungeonGame.sprite_container import SpriteContainer
import numpy as np
from DrillDungeonGame.entity.entities.drill import Drill
from DrillDungeonGame.map.dungeon_generator import *
from DrillDungeonGame.map.chunk import Chunk


class ChunkManager:
    """

    Takes care of all aspects related to updating and loading of chunks.

    Methods
    -------
    _update_chunks(drill_x, drill_y)
        Checks if chunks need to be activate or deactivated.
    _load_chunks_from_map_config(map_layer_matrix)
        Loads chunks from given map layer.
    _load_single_chunk(startX, startY, map_layer_matrix, chunk_size=16)
        Loads a single chunk.

    """

    def __init__(self, map_layer_matrix, number_of_chunks=64, chunk_side_length=16, number_of_active_chunks=9):
        """

        Parameters
        ----------
        map_layer_matrix        :   List[map_layer_matrix]
            List containing the map layer matrix.
        number_of_chunks        :   int
            Number of chunks to be created.
        chunk_side_length       :   int
            The length of the chunks.
        number_of_active_chunks :   int
            Number of active chunks.

        """
        self.chunks_dictionary = {}
        self.number_of_chunks = number_of_chunks
        self.chunk_side_length = chunk_side_length
        self.active_chunks = [0, 1, 2] #list of all currently active chunks by dict index
        self._load_chunks_from_map_config(map_layer_matrix)
        self.number_of_active_chunks = number_of_active_chunks

    def _update_chunks(self, drill_x, drill_y):
        """

        Checks all chunks to see if they should be activated/deactivated.

        Notes
        -----
        Checks for the nearest 9? Chunks or so and loads them in.
        Basically anything that could potentially be on screen soon, but can move this number based on need.
        The nicer way of doing this would be to have some kind of k nearest neighbours approach.
        But hard coding it to only consider those within a certain x range would probably
        be faster

        Parameters
        ----------
        drill_x : int
            x coordinate of the drill.
        drill_y : int
            y coordinate of the drill.

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

        Loads the chunks from a given map layer.

        Notes
        -----
        Needs to cut through the matrix and break it into chunks of appropriate
        size. This can be achieved by 1 - Finding number of chunks per row and then iterating
        it up in a similar way as the loading feature but in reverse.

        Parameters
        ----------
        map_layer_matrix: List[map_layer_matrix]
            List containing the map layer matrix.

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
        """

        Loads a single chunk.

        Parameters
        ----------
        startX              : int
            Starting x coordinate of the chunk.
        startY
            Starting y coordinate of the chunk.
        map_layer_matrix    : List[map_layer_matrix]
            List containing the map layer matrix.
        chunk_size          : int
            Size of the chunk.

        Returns
        -------
        Chunk(List[chunk_piece])

        """
        chunk_piece = []
        for i in range(startY, startY + chunk_size):
            chunk_piece.append(map_layer_matrix[i][startX : startX + chunk_size])
        return Chunk(chunk_piece)





