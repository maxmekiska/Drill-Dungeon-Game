"""
A module to generate the specifications of the map which can then be loaded up by arcade.
Initially will configure the maps as arrays, but can look to save these as some other 
file type, depending on how performance is affected.
"""
import random
import numpy as np

class MapLayer:
    """ 
    A class that holds a single map layer 
    """

    def __init__(self, height=200, width=200, meanDungeonSize=40, meanCoalSize=5, meanGoldSize=5): # added meanCoalSize, meanGoldSize parameter
        self.mapLayerMatrix = []
        self.height = height 
        self.width = width
        self.meanDungeonSize = meanDungeonSize
        self.meanCoalSize = meanCoalSize # coal
        self.meanGoldSize = meanGoldSize # gold 

    def __repr__(self):
        """
        Prints the.mapLayerMatrix row by row. 
        """
        mapLayerMatrixString = ''
        for row in self.mapLayerMatrix:
            for item in row:
                mapLayerMatrixString += (item + " ")
            mapLayerMatrixString += "\n"
        return mapLayerMatrixString

    def generate_dungeon(self):
        """
        Generates a.mapLayerMatrix on the map. Current issues are: it can repeat certain steps
        """
        x, y = self.generate_dungeon_start_point()
        dungeonSize = self.generate_dungeon_size()
        while dungeonSize > 0:
            if self.mapLayerMatrix[y][x] != ' ':
                self.mapLayerMatrix[y][x] = ' '
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)
            
    def generate_coal(self): # coal
        """
        Generates a.mapLayerMatrix on the map. Current issues are: it can repeat certain steps
        """
        x, y = self.generate_coal_start_point()
        dungeonSize = self.generate_coal_size()
        while dungeonSize > 0:
            if self.mapLayerMatrix[y][x] != 'C':
                self.mapLayerMatrix[y][x] = 'C'
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)
            
    def generate_gold(self): # gold
        x, y = self.generate_coal_start_point()
        dungeonSize = self.generate_coal_size()
        while dungeonSize > 0:
            if self.mapLayerMatrix[y][x] != 'G':
                self.mapLayerMatrix[y][x] = 'G'
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)
    

    def generate_blank_map(self):
        """
        Generates a blank (featurless, not empyt).mapLayerMatrix map (full of
        'X' - meaning full of blocks)
        """
        for i in range(self.height):
            self.generate_blank_row()

    def generate_blank_row(self):
        """
        Appends a blank row (full of 'X' - meaning full of blocks) to 
        self.mapLayerMatrix
        """
        row = []
        for i in range(self.width):
            row.append('X')
        self.mapLayerMatrix.append(row)
           
    def generate_dungeon_start_point(self):
        """
        Generates the location of the first block in the.mapLayerMatrix
        --------------------------------------------------------
        Returns
        int startX : The x coordinate of the first block in the.mapLayerMatrix
        int startY : The y coordinate of the first block in the.mapLayerMatrix
        """
        startX = random.randint(0, self.width - 1)
        startY = random.randint(0, self.height - 1)
        return startX, startY


    def generate_coal_start_point(self): # might be possible to refactor
        """
        Generates the location of the first block in the.mapLayerMatrix
        --------------------------------------------------------
        Returns
        int startX : The x coordinate of the first block in the.mapLayerMatrix
        int startY : The y coordinate of the first block in the.mapLayerMatrix
        """
        startX = random.randint(0, self.width - 1)
        startY = random.randint(0, self.height - 1)
        return startX, startY
        
    def generate_gold_start_point(self): # might be possible ot refactor
        """
        Generates the location of the first block in the.mapLayerMatrix
        --------------------------------------------------------
        Returns
        int startX : The x coordinate of the first block in the.mapLayerMatrix
        int startY : The y coordinate of the first block in the.mapLayerMatrix
        """
        startX = random.randint(0, self.width - 1)
        startY = random.randint(0, self.height - 1)
        return startX, startY


    def generate_dungeon_size(self):
        """
        Generates the size of the.mapLayerMatrix using a poisson distribution with mean
        self.meanDungeonSize
        ---------------------------------------------------------
        Returns
        int.mapLayerMatrixSize : The size of the dungeon in number of blocks
        """
        rng = np.random.default_rng()
        dungeonSize = rng.poisson(self.meanDungeonSize)
        return dungeonSize


    def generate_coal_size(self): # might be possible to refactor
        """
        Generates the size of the.mapLayerMatrix using a poisson distribution with mean
        self.meanCoalSizeSize
        ---------------------------------------------------------
        Returns
        int.mapLayerMatrixSize : The size of the dungeon in number of blocks
        """
        rng = np.random.default_rng()
        dungeonSize = rng.poisson(self.meanCoalSize) #cluster of coal
        return dungeonSize

    def generate_gold_size(self): # might be possible to refactor
        """
        Generates the size of the.mapLayerMatrix using a poisson distribution with mean
        self.meanGoldSizeSize
        ---------------------------------------------------------
        Returns
        int.mapLayerMatrixSize : The size of the dungeon in number of blocks
        """
        rng = np.random.default_rng()
        dungeonSize = rng.poisson(self.meanGoldSize) #cluster of gold
        return dungeonSize         

    def update_dungeon_coords(self, x, y, walkDirection):
        """
        Moves the.mapLayerMatrix block coordinate in the direction dictated by the 
        walkDirection
        int x             : The x (horizontal) coordinate of the current block
        int y             : The y (vertical) coordinate of the current block
        int walkDirection : The direction of the random walk where:
        0 = Upwards (y + 1)
        1 = Right (x + 1)
        2 - Downwards (y - 1)
        3 = Left (x - 1)
        ----------------------------------------------------------
        Returns
        int x             : The updated x coordinate of the current block
        int y             : The updated y coordinate of the current block
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
        

    def get_walk_direction(self, x, y):
        """
        Generates the walk direction for the.mapLayerMatrix's random walk. 
        int x : The x (horizontal) coordinate of the current block
        int y : The y (vertical) coordinate of the current block
        ----------------------------------------------------------
        Returns
        int walkDirection : The direction of the random walk where:
        0 = Upwards (y + 1)
        1 = Right (x + 1)
        2 - Downwards (y - 1)
        3 = Left (x - 1)
        """
        if x == 0:
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