import pytest
from DrillDungeonGame.main import *

def test_fill_map_with_terrain_blockWidth_error():
    dungeonGame = DrillDungeonGame()
    with pytest.raises(ValueError):
        dungeonGame.fill_map_with_terrain(19, 20)


def test_fill_map_with_terrain_blockHeight_error():
    dungeonGame = DrillDungeonGame()
    with pytest.raises(ValueError):
        dungeonGame.fill_map_with_terrain(20, 19)
    
