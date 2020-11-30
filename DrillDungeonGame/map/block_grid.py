from typing import List, Tuple

import arcade

from ..map.block import BLOCK, Block


class BlockGrid:
    def __init__(self, matrix: List[List[Tuple[str, float, float]]], sprites) -> None:
        self.blocks = [[] for _ in range(len(matrix[0]))]
        self.air_blocks = arcade.SpriteList()

        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                b = matrix[y][x]
                char = b[0]
                block_x = b[1]
                block_y = b[2]
                if char == 'X':
                    self.blocks[x].append(BLOCK.DIRT(x, y, block_x, block_y))
                elif char == 'C':
                    self.blocks[x].append(BLOCK.COAL(x, y, block_x, block_y))
                elif char == 'G':
                    self.blocks[x].append(BLOCK.GOLD(x, y, block_x, block_y))
                elif char == 'O':
                    self.blocks[x].append(BLOCK.BORDER(x, y, block_x, block_y))
                elif char == ' ':
                    self.blocks[x].append(BLOCK.AIR(x, y, block_x, block_y))
                elif char == 'S':
                    self.blocks[x].append(BLOCK.SHOP(x, y, block_x, block_y))
                elif char == 'W':
                    self.blocks[x].append(BLOCK.WALL(x, y, block_x, block_y))
                elif char == 'F':
                    self.blocks[x].append(BLOCK.FLOOR(x, y, block_x, block_y))
                elif char == 'D':
                    self.blocks[x].append(BLOCK.DRILLDOWN(x, y, block_x, block_y))
                else:
                    raise ValueError(f'Unknown char, {char} for block type received.')

        self.initialise_blocks_adjacent_to_air(sprites)

    @property
    def height(self) -> int:
        return len(self.blocks)

    @property
    def width(self) -> int:
        return len(self.blocks[0])

    def _add_block_to_lists(self, block: Block, sprites) -> None:
        if type(block) == BLOCK.DIRT:
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.COAL:
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.GOLD:
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.SHOP:
            sprites.shop_list.append(block)
            sprites.indestructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.BORDER:
            sprites.indestructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)
            sprites.border_wall_list.append(block)

        elif type(block) == BLOCK.WALL:
            sprites.indestructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)
            sprites.border_wall_list.append(block)

        elif type(block) == BLOCK.FLOOR:
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.DRILLDOWN:
            sprites.all_blocks_list.append(block)

        else:
            raise ValueError(f'Incorrect block type: {type(block)}!')

    def break_block(self, block: Block, sprites) -> None:
        for adjacent_block in self._get_adjacent_blocks_to(block):
            if type(adjacent_block) != BLOCK.AIR:
                self._add_block_to_lists(adjacent_block, sprites)

        block.remove_from_sprite_lists()
        x, y = block.x, block.y
        center_x, center_y = block.center_x, block.center_y
        new_air_block = BLOCK.AIR(x, y, center_x, center_y)
        self.blocks[x][y] = new_air_block
        self.air_blocks.append(new_air_block)

    def initialise_blocks_adjacent_to_air(self, sprites):
        for x in range(self.width):
            for y in range(self.height):
                block = self.blocks[x][y]
                if any(type(adjacent_block) == BLOCK.AIR or type(adjacent_block) == BLOCK.FLOOR for adjacent_block in self._get_adjacent_blocks_to(block)):
                    if type(block) == BLOCK.AIR:
                        self.air_blocks.append(block)
                    elif type(block) == BLOCK.FLOOR:
                        self.air_blocks.append(block)
                    elif type(block) == BLOCK.DRILLDOWN:
                        self.air_blocks.append(block)
                    else:
                        self._add_block_to_lists(block, sprites)

    def _get_adjacent_blocks_to(self, block: Block) -> List[Block]:
        """Returns a list of blocks (total: 4) that are adjacent to a block. Doesn't include diagonal blocks."""
        adjacent_blocks = []
        for x, y in block.adjacent_positions:
            try:
                adjacent_blocks.append(self.blocks[x][y])
            except IndexError:
                continue
        return adjacent_blocks
