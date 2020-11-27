from __future__ import annotations

import abc
from typing import Union

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
    file = "resources/images/material/dungeon_wall.png"
    scale = 1.2
    char = 'O'


class ShopBlock(Block):
    file = "resources/images/shop/shop.png"
    scale = 0.18
    char = 'S'


class DungeonWallBlock(Block):
    file = "resources/images/material/dungeon_wall.png"
    scale = 1.2
    char = 'W'


class DungeonWallTopper(Block):
    file = "resources/images/material/wall_topper.png"
    scale = 1.2
    char = 'W'


class DungeonWallRight(Block):
    file = "resources/images/material/right_wall.png"
    scale = 1.2
    char = 'RW'

class DungeonWallLeft(Block):
    file = "resources/images/material/left_wall.png"
    scale = 1.2
    char = 'LW'

class _Block:
    AIR = AirBlock
    DIRT = DirtBlock
    COAL = CoalBlock
    GOLD = GoldBlock
    SHOP = ShopBlock
    BORDER = BorderBlock
    WALL = DungeonWallBlock
    WALLTOPPER = DungeonWallTopper
    RIGHTWALL = DungeonWallRight
    LEFTWALL = DungeonWallLeft


BLOCK = _Block
