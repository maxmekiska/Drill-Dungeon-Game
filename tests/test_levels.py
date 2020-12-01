import pytest

from ..DrillDungeonGame.level import *

def test_map_layer_generation():
    level = Level(Drill(10, 10))
    assert len(level.sprites.all_blocks_list) > 0


def test_enemy_generation():
    level = Level(Drill(10, 10))
    assert len(level.sprites.enemy_list) > 0



