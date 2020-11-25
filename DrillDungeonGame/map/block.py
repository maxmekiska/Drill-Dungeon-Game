from __future__ import annotations

import abc
from typing import List, Tuple, Union

import arcade


class Block(arcade.Sprite):
    def __init__(self, x: int, y: int, center_x: Union[float, int], center_y: Union[float, int]) -> None:
        super().__init__(filename=self.file, scale=self.scale, center_x=center_x, center_y=center_y)
        self.x, self.y = x, y
        self.is_visible = False

    @property
    @abc.abstractmethod
    def file(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def scale(self) -> float:
        pass

    @property
    @abc.abstractmethod
    def char(self) -> str:
        pass

    def __repr__(self):
        return self.char


class AirBlock(Block):
    file = "resources/images/material/brown.png"
    scale = 0.25
    char = ' '


class DirtBlock(Block):
    file = ":resources:images/tiles/grassCenter.png"
    scale = 0.16
    char = 'X'


class CoalBlock(Block):
    file = "resources/images/material/Coal_square2.png"
    scale = 0.04  # 0.03
    char = 'C'


class GoldBlock(Block):
    file = "resources/images/material/Gold_square.png"
    scale = 0.03
    char = 'G'


class BorderBlock(Block):
    file = ":resources:images/tiles/Lava.png"
    scale = 0.18
    char = 'O'


class _Block:
    AIR = AirBlock
    DIRT = DirtBlock
    COAL = CoalBlock
    GOLD = GoldBlock
    BORDER = BorderBlock


BLOCK = _Block


class BlockGrid:
    def __init__(self, matrix: List[List[Tuple[str, float, float]]], sprites) -> None:
        self.blocks = [[] for _ in range(len(matrix[0]))]
        self.air_blocks = arcade.SpriteList()

        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                b = matrix[x][y]
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
                elif char == 'E':
                    self.blocks[x].append(BLOCK.AIR(x, y, block_x, block_y))  # TODO spawn enemies.
                else:
                    raise ValueError(f'Unknown char, {char} for block type received.')

        self.initialise_visible_blocks(sprites)

    @property
    def height(self) -> int:
        return len(self.blocks)

    @property
    def width(self) -> int:
        return len(self.blocks[0])

    def _add_block_to_lists(self, block: Block, sprites) -> None:
        if type(block) == BLOCK.DIRT:
            sprites.dirt_list.append(block)
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.COAL:
            sprites.coal_list.append(block)
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.GOLD:
            sprites.gold_list.append(block)
            sprites.destructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)

        elif type(block) == BLOCK.BORDER:
            sprites.indestructible_blocks_list.append(block)
            sprites.all_blocks_list.append(block)
            sprites.border_wall_list.append(block)

        else:
            raise ValueError(f'Incorrect block type: {type(block)}!')

    def break_block(self, block: Block, sprites) -> None:
        for adjacent_block in self._get_adjacent_blocks_to(block):
            if type(adjacent_block) != BLOCK.AIR:
                adjacent_block.is_visible = True
                if type(block) != BLOCK.AIR:
                    self._add_block_to_lists(adjacent_block, sprites)

        block.remove_from_sprite_lists()
        x, y = block.x, block.y
        center_x, center_y = block.center_x, block.center_y
        new_air_block = BLOCK.AIR(x, y, center_x, center_y)
        self.blocks[x][y] = new_air_block
        self.air_blocks.append(new_air_block)

    def initialise_visible_blocks(self, sprites):
        for x in range(self.width):
            for y in range(self.height):
                block = self.blocks[x][y]
                if any(type(block) == BLOCK.AIR for block in self._get_adjacent_blocks_to(block)):
                    block.is_visible = True
                    if type(block) != BLOCK.AIR:
                        self._add_block_to_lists(block, sprites)
                    else:
                        self.air_blocks.append(block)

    def _get_adjacent_blocks_to(self, block: Block) -> List[Block]:
        """Returns a list of blocks (total: 8) that are adjacent to a block. Includes diagonal blocks."""
        adjacent_blocks = []
        adjacent_positions = (
            (block.x, block.y + 1),
            (block.x, block.y - 1),
            (block.x + 1, block.y),
            (block.x - 1, block.y),
        )
        for adjacent_position in adjacent_positions:
            x, y = adjacent_position
            try:
                adjacent_blocks.append(self.blocks[x][y])
            except IndexError:
                continue
        return adjacent_blocks
