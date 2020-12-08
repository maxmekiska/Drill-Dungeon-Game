import random

import numpy as np

from ..map.prefab_dungeon_rooms import *

MAP_WIDTH = 2400
MAP_HEIGHT = 2400



class MapLayer:
    """

    Class for generating and holding the configuration of map layers

    Methods
    -------
    get_full_map_layer_configuration(number_of_dungeons: int, number_of_coal_patches: int, number_of_gold_patches: int)
        Generates a map layer configuration from scratch.
    generate_map_layer_configuration()
        Generates a map layer configuration from the pre-existing map layer matrix.
    load_row_from_matrix(row: list, y_block_center: float, block_width: float, block_height: float)
        Loads a single row from the map layer matrix to the configuration matrix.
    generate_dungeon(enemy_chance: float=0.1)
        Generates a single dungeon on a map layer matrix
    generate_coal()
        Generates a single coal patch on a map layer matrix.
        Coal blocks are represented by the character 'C'
    generate_gold()
        Generates a single gold patch on a map layer matrix
        Gold blocks are represented by the character 'G'
    generate_shop()
        Generates a shop on a map layer matrix
        Shop blocks are represented by the character 'S'
    generate_border_walls()
        Generates a impassable border walls on a map layer matrix
        Impassable blocks are represented by the character 'O'
    generate_blank_map()
        Generates a blank (dirt filled) map layer matrix.
        Blank blocks are represented by the character 'X'
    generate_blank_row()
        Generates a blank (dirt filled) map layer row.
        Blank blocks are represented by the character 'X'
    generate_random_start_point()
        Generates a random location in the.map_layer_matrix
    generate_patch_size(mean_size: int)
        Generates the size of the dungeon using a poisson distribution with mean self.mean_dungeon_size
    update_dungeon_coords(x : int, y : int, walkDirection : int)
        Moves the.map_layer_matrix block coordinate in the direction dictated by the walkDirection
    get_walk_direction(x : int, y : int)
        Generates the walk direction for the.map_layer_matrix's random walk.

    """

    def __init__(self, height: int=128, width: int=128, mean_dungeon_size: int=500, mean_coal_size: int=5, mean_gold_size: int=5, mean_drillable_size: int=8) -> None:
        """

        Parameters
        ----------
        height              :   int
            The height of the map in number of blocks.
        width               :   int
            The width of the map in number of blocks.
        mean_dungeon_size   :   int
            The mean size of empty dungeons in blocks.
        mean_coal_size      :   int
            The mean size of coal patches in blocks.
        mean_gold_size      :   int
            The mean size of gold patches in blocks

        """
        self.map_layer_matrix = []
        self.height = height
        self.width = width
        self.mean_dungeon_size = mean_dungeon_size
        self.mean_coal_size = mean_coal_size # coal
        self.mean_gold_size = mean_gold_size # gold
        self.mean_drillable_size = mean_drillable_size #Size of drillable patches
        self.map_layer_configuration = []

    def __repr__(self) -> str:
        """

        Represents the map layer matrix as a string

        Parameters
        ----------
        None

        Returns
        -------
        str
            The map layer matrix as a formatted string.

        """
        map_layer_matrixString = ''
        for row in self.map_layer_matrix:
            for item in row:
                map_layer_matrixString += (item + " ")
            map_layer_matrixString += "\n"
        return map_layer_matrixString

    def get_full_map_layer_configuration(self, number_of_dungeons: int, number_of_coal_patches: int, number_of_gold_patches: int, number_of_shops: int, drillX, drillY, number_of_drillable_patches: int=8) -> list:
        """

        Generates a map layer configuration from scratch

        Notes
        -----
        Map layer configuration is different from map layer matrix because it includes the locations of
        each component of the map layer. While the map layer matrix has just the type of block, the
        configuration also includes the block's x and y location in a tuple.

        Parameters
        ----------
        number_of_dungeons       :   int
            Number of dungeons to add to the map layer.
        number_of_coal_patches   :   int
            Number of coal patches to add to map layer.
        number_of_gold_patches   :   int
            Number of gold patches to add to map layer.

        Returns
        -------
        List[List[Tuple]]
            The map layer configuration. Each item in the matrix is a tuple of:
            1 - the block type,
            2 - the block's X location
            3 - the block's Y location

        """

        self.generate_blank_map()
        for i in range(number_of_dungeons):
            self.generate_dungeon()
        for i in range(number_of_coal_patches):
            self.generate_coal()
        for i in range(number_of_gold_patches):
            self.generate_gold()
        for i in range(number_of_shops):
            self.generate_shop()
        for i in range(number_of_drillable_patches):
            self.generate_drillable_zones()

        self.generate_border_walls()
        self.generate_advanced_dungeon()
        self.generate_map_layer_configuration()
        self.generate_drillable_zones()
        self.create_space_for_drill(drillX, drillY)
        return self.map_layer_configuration

    def generate_map_layer_configuration(self):
        """

        Generates a map layer configuration from the pre-existing map layer matrix.

        Notes
        -----
        Saves the map layer configuration under self.map_layer_configuration.

        Parameters
        ----------
        None

        """
        block_height = 20
        block_width = 20

        y_block_center = 0.5 * block_height
        for row in self.map_layer_matrix:
            configuration_row = self.load_row_from_matrix(row, y_block_center, block_width, block_height)
            self.map_layer_configuration.append(configuration_row)
            y_block_center += block_height


    def generate_drillable_zones(self):
        """
        Generates drillable patches. The start point only spawns within 10 blocks of the side
        """
        x = np.random.choice([np.random.randint(0, 10), np.random.randint(self.width-11, self.width-1)])
        y = np.random.choice([np.random.randint(0, 10), np.random.randint(self.height-11, self.height-1)])
        drillable_size = self.generate_patch_size(self.mean_drillable_size)
        while drillable_size > 0:
            if self.map_layer_matrix[y][x] != 'D':
                self.map_layer_matrix[y][x] = 'D'
                drillable_size -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)

    def load_row_from_matrix(self, row: list, y_block_center: float, block_width: float, block_height: float) -> list:
        """

        Loads a single row from the map layer matrix to the configuration matrix

        Parameters
        ----------
        row              :   list
            The row of the map layer matrix currently being loaded
        y_block_center   :   float
            Y location of the current row.
        block_width      :   float
            Width of the blocks to be loaded.
        block_height     :   float
            Height of the blocks to be loaded.

        Returns
        -------
        List[Tuple]
            The row loaded into configuration format. Each item in the row is a tuple of:
            1 - the block type,
            2 - the block's X location and
            3 - the block's Y location

        """
        x_block_center = 0.5 * block_width
        configuration_row = []
        for item in row:
            configuration_row.append((item, x_block_center, y_block_center))
            x_block_center += block_width
        return configuration_row


    def create_space_for_drill(self, drillX, drillY) -> None:
        """
        Clears out empty space for when the drill goes down or up a layer.

        Parameters
        ----------
        drillX   :   int, float
            The X coordinate of the drill
        drillY   :   int, float
            The Y coordinate of the drill
        """
        for i, row in enumerate(self.map_layer_configuration):
            for j, item in enumerate(row):
                distance_from_drill = np.sqrt((drillX - item[1])**2 + (drillY - item[2])**2)
                if distance_from_drill < 50:
                    new_item = (" ", item[1], item[2])
                    self.map_layer_configuration[i][j] = new_item

    def generate_advanced_dungeon(self) -> None:
        """
        Generates an advanced dungeon from several preconfigured 
        rooms
        """
        startX = np.random.randint(20, 40)
        startY = np.random.randint(20, 40)
        entrance_room = entrance_room_one #Add method to choose random
        for i in  range(len(entrance_room)):
            for j in range(len(entrance_room[0])):
                    self.map_layer_matrix[i+startY][j+startX] = entrance_room[i][j]


    def generate_dungeon(self) -> None:
        """
        Generates a single dungeon on a map layer matrix
        """
        x, y = self.generate_random_start_point()
        dungeonSize = self.generate_patch_size(self.mean_dungeon_size)
        while dungeonSize > 0:
            if self.map_layer_matrix[y][x] != ' ':
                self.map_layer_matrix[y][x] = ' '
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)

    def generate_coal(self) -> None:
        """

        Generates a single coal patch on a map layer matrix.
        Coal blocks are represented by the character 'C'

        Parameters
        ----------
        None

        """
        x, y = self.generate_random_start_point()
        dungeonSize = self.generate_patch_size(self.mean_coal_size)
        while dungeonSize > 0:
            if self.map_layer_matrix[y][x] != 'C':
                self.map_layer_matrix[y][x] = 'C'
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)

    def generate_gold(self) -> None: # gold
        """

        Generates a single gold patch on a map layer matrix
        Gold blocks are represented by the character 'G'

        Parameters
        ----------
        None

        """
        x, y = self.generate_random_start_point()
        dungeonSize = self.generate_patch_size(self.mean_gold_size)
        while dungeonSize > 0:
            if self.map_layer_matrix[y][x] != 'G':
                self.map_layer_matrix[y][x] = 'G'
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)

    def generate_shop(self) -> None:
        """

        Generates a shop on a map layer matrix
        Shop blocks are represented by the character 'S'

        Parameters
        ----------
        None

        """
        x, y = self.generate_random_start_point()
        self.map_layer_matrix[x][y] = 'S'

    def generate_border_walls(self) -> None:
        """

        Generates a impassable border walls on a map layer matrix
        Impassable blocks are represented by the character 'O'

        Parameters
        ----------
        None

        """
        for i, row in enumerate(self.map_layer_matrix):
            if i == 0 or i == len(self.map_layer_matrix) - 1:
                for j, item in enumerate(row):
                    row[j] = 'O'
            else:
                row[0] = 'O'
                row[-1] = 'O'

    def generate_blank_map(self) -> None:
        """

        Generates a blank (dirt filled) map layer matrix.
        Blank blocks are represented by the character 'X'

        Parameters
        ----------
        None

        """
        for i in range(self.height):
            self.generate_blank_row()

    def generate_blank_row(self) -> None:
        """

        Generates a blank (dirt filled) map layer row.
        Blank blocks are represented by the character 'X'

        Parameters
        ----------
        None

        """
        row = []
        for i in range(self.width):
            row.append('X')
        self.map_layer_matrix.append(row)

    def generate_random_start_point(self) -> tuple:
        """

        Generates a random location in the.map_layer_matrix

        Parameters
        ----------
        None

        Returns
        -------
            startX   :   int
                The x coordinate of the first block in the.map_layer_matrix
            startY   :   int
                The y coordinate of the first block in the.map_layer_matrix

        """
        startX = random.randint(0, self.width - 1)
        startY = random.randint(0, self.height - 1)
        return startX, startY

    def generate_patch_size(self, mean_size: int) -> int:
        """

        Generates the size of the dungeon using a poisson distribution with mean
        self.mean_dungeon_size

        Parameters
        ----------
        mean_size      :   int
            The mean size of the patch in number of blocks

        Returns
        -------
        dungeon_size   :   int
            The size of the dungeon in number of blocks

        """
        rng = np.random.default_rng()
        patch_size = rng.poisson(mean_size)
        return patch_size

    def update_dungeon_coords(self, x : int, y : int, walkDirection : int) -> tuple:
        """

        Moves the.map_layer_matrix block coordinate in the direction dictated by the
        walkDirection.

        Parameters
        ----------
        x               : int
            The x (horizontal) coordinate of the current block
        y               : int
            The y (vertical) coordinate of the current block
        walkDirection   : int
            The direction of the random walk where:
            0 = Upwards     (y + 1)
            1 = Right       (x + 1)
            2 = Downwards   (y - 1)
            3 = Left        (x - 1)

        Returns
        -------
        x   : int
            The updated x coordinate of the current block.
        y   : int
            The updated y coordinate of the current block.

        """
        if walkDirection == 0:
            y += 1
        if walkDirection == 1:
            x += 1
        if walkDirection == 2:
            y -= 1
        if walkDirection == 3:
            x -= 1
        return x, y

    def get_walk_direction(self, x : int, y : int) -> int:
        """

        Generates the walk direction for the.map_layer_matrix's random walk.

        Parameters
        ----------
        x   :   int
            The x (horizontal) coordinate of the current block
        y   :   int
            The y (vertical) coordinate of the current block

        Returns
        --------
        walkDirection   :   int
            The direction of the random walk where:
            0 = Upwards     (y + 1)
            1 = Right       (x + 1)
            2 - Downwards   (y - 1)
            3 = Left        (x - 1)

        """
        if x not in range(0, self.width) or y not in range(0, self.height):
            raise ValueError("Row or column out of range")
        elif x == 0:
            if y == 0:
                return random.choice([0, 1])
            elif y == self.height - 1:
                return random.choice([1, 2])
            else:
                return random.choice([0, 1, 2])
        elif y == 0:
            if x == self.width - 1:
                return random.choice([0, 3])
            else:
                return random.choice([0, 1, 3])
        elif x == self.width - 1:
            if y == self.height - 1:
                return random.choice([2, 3])
            else:
                return random.choice([0,2,3])
        elif y == self.height -1:
            return random.choice([1,2,3])
        else:
            return random.choice([0, 1, 2, 3])
