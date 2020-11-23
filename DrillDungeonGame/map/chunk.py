import arcade
from DrillDungeonGame.sprite_container import SpriteContainer


class Chunk:

    def __init__(self, chunk_matrix: list):
        self.chunk_matrix = chunk_matrix
        self.chunk_sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList()) 
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

