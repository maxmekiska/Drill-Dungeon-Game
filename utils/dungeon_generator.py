"""
A module to generate the specifications of the map which can then be loaded up by arcade.
Initially will configure the maps as arrays, but can look to save these as some other 
file type, depending on how performance is affected.
"""
import random
import numpy as np

class DungeonGenerator:
    
    def __init__():
        self.dungeonList = []




class Dungeon:
    """ A class that holds a single dungeon
    Approach - Begin by generating a fully filled in dungeon
    Next - select a random point on map (number of dungeons should also be random maybe)
    Generate a random amount of blocks to be in the cave (normally distributed
    Bore out that map
    Repeat loop where the condition is that the random point cannot be filled already 
    (but caves can connect)
    For now - will just spiral around the initial point and have some consideration for
    if the cave meets the wall
    """

    def __init__(self, height=200, width=200, meanDungeonSize=40):
        '''
        length, width = length, width of dungeon in blocks
        '''
        self.dungeon = []
        self.height = height 
        self.width = width
        self.meanDungeonSize = meanDungeonSize

    def __str__(self):
        for row in self.dungeon:
            print(row)

    def generate_blank_map(self):
        for i in range(self.height):
            self.generate_blank_row()

    def generate_blank_row(self):
        row = []
        for i in range(self.width):
            row.append('X')
        self.dungeon.append(row)
           
    def generate_dungeon_start_point(self):
        startX = random.randint(0, self.width)
        startY = random.randint(0, self.height)
        return startX, startY

    def generate_dungeon_size(self):
        """
        Simple poisson distribution to allow for occasional very large dungeons.
        """
        rng = np.random.default_rng()
        dungeonSize = rng.poisson(self.meanDungeonSize)
        return dungeonSize
        
    def generate_dungeon(self):
        """
        Generates the dungeon map. Current issues are: it can repeat certain steps
        """
        x, y = self.generate_dungeon_start_point()
        dungeonSize = self.generate_dungeon_size()
        while dungeonSize > 0:
            if self.dungeon[y][x] != 'O':
                self.dungeon[y][x] = 'O'
                dungeonSize -= 1
            walkDirection = self.get_walk_direction(x, y)
            x, y = self.update_dungeon_coords(x, y, walkDirection)

    def update_dungeon_coords(self, x, y, walkDirection):
        if walkDirection == 0:
            y += 1
            x += 1
        if walkDirection == 1:
            y += 1
        if walkDirection == 2:
            x += 1
        if walkDirection == 3:
            y -= 1
            x += 1
        if walkDirection == 4:
            y += 1
            x -= 1
        if walkDirection == 5:
            y -= 1
        if walkDirection == 6:
            x -= 1
        if walkDirection == 7:
            y -= 1
            x -= 1
        return x, y
        


    def get_walk_direction(self, x, y):
        if x == 0:
            if y == 0:
                return random.choice([0, 1, 2])
            else:
                return random.choice([0, 1, 2, 3, 5])
        elif y == 0:
            return random.choice([0, 1, 2, 4, 6])
        elif x == self.width:
            if y == self.height:
                return random.choice([5, 6, 7])
            else:
                return random.choice([1, 4, 5, 6, 7])
        elif y == self.height:
            return random.choice([2, 3, 5, 6, 7])
        else:
            return random.randint(0, 7)

