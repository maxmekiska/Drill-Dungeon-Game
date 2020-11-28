from enum import Enum

SCREEN_TITLE = "Welcome to the Drill Dungeon"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
VIEWPOINT_MARGIN = 120

MAP_WIDTH = 2400
MAP_HEIGHT = 2400

BLOCK_PIXEL_SIZE = 32


class FaceDirection(Enum):
    RIGHT = 0
    LEFT = 1
