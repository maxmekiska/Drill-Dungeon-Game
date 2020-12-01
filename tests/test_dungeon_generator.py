import pytest

from ..DrillDungeonGame.map.dungeon_generator import *


def test_get_walk_direction_input():
    map_layer = MapLayer()
    with pytest.raises(ValueError):
        walk_direction = map_layer.get_walk_direction(-10, -10)



def test_get_walk_direction_output_ranges():
    map_layer = MapLayer()
    top_left = map_layer.get_walk_direction(0, map_layer.height - 1)
    top_right = map_layer.get_walk_direction(map_layer.width-1, map_layer.height - 1)
    bottom_left = map_layer.get_walk_direction(0, 0)
    bottom_right = map_layer.get_walk_direction(map_layer.width-1, 0)
    center = map_layer.get_walk_direction(int(map_layer.width/2), int(map_layer.height/2))
    assert (top_left in [1, 2] and top_right in [2, 3] and bottom_left in [0, 1] and bottom_right in [0, 3] and center in [0, 1, 2, 3])
    
def test_update_dungeon_coords():
    map_layer = MapLayer()
    x = 10
    y = 10
    step_one = map_layer.update_dungeon_coords(x, y, 0)
    step_two = map_layer.update_dungeon_coords(step_one[0], step_one[1], 1)
    step_three = map_layer.update_dungeon_coords(step_two[0], step_two[1], 2)
    step_four = map_layer.update_dungeon_coords(step_three[0], step_three[1], 3)
    assert (step_one[1] == y+1 and step_two[0] == x+1 and step_three[1] == y and step_four[0] == x)


def test_generate_mean_dungeon_size():
    map_layer = MapLayer()
    assert map_layer.generate_patch_size(20) >= 0

def test_generate_random_start_point():
    map_layer = MapLayer()
    assert map_layer.generate_random_start_point()[0] in range(0, map_layer.width-1) and  map_layer.generate_random_start_point()[1] in range(0, map_layer.height-1)

def test_generate_blank_row():
    map_layer = MapLayer()
    map_layer.generate_blank_row()
    assert map_layer.map_layer_matrix[0] == ['X' for i in range(map_layer.width)]

def test_generate_blank_map():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    assert map_layer.map_layer_matrix == [['X' for i in range(map_layer.width)] for j in range(map_layer.height)] 
    
def test_generate_border_walls():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_border_walls()
    assert map_layer.map_layer_matrix[0] == ['O' for i in range(map_layer.width)]

def test_generate_shop():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_shop()
    shop_in_map = False
    for row in map_layer.map_layer_matrix:
        if 'S' in row:
            shop_in_map = True
    assert shop_in_map == True

def test_generate_gold():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_gold()
    gold_in_map = False
    for row in map_layer.map_layer_matrix:
        if 'G' in row:
            gold_in_map = True
            break
    assert gold_in_map == True

def test_generate_coal():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_coal()
    coal_in_map = False
    for row in map_layer.map_layer_matrix:
        if 'C' in row:
            coal_in_map = True
            break
    assert coal_in_map == True

def test_generate_dungeon():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_dungeon()
    dungeon_in_map = False
    for row in map_layer.map_layer_matrix:
        if ' ' in row:
            dungeon_in_map = True
    assert dungeon_in_map == True

def test_generate_drillable_zones():
    map_layer = MapLayer()
    map_layer.generate_blank_map()
    map_layer.generate_drillable_zones()
    dungeon_in_map = False
    for row in map_layer.map_layer_matrix:
        if 'D' in row:
            dungeon_in_map = True
    assert dungeon_in_map == True


