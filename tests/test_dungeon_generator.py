import unittest

from DrillDungeonGame.map.dungeon_generator import *


class DungeonGeneratorTestCase(unittest.TestCase):
    def test_get_walk_direction_input(self):
        map_layer = MapLayer()
        self.assertRaises(ValueError, map_layer.get_walk_direction, -10, -10)

    def test_get_walk_direction_output_ranges(self):
        map_layer = MapLayer()
        top_left = map_layer.get_walk_direction(0, map_layer.height - 1)
        top_right = map_layer.get_walk_direction(map_layer.width-1, map_layer.height - 1)
        bottom_left = map_layer.get_walk_direction(0, 0)
        bottom_right = map_layer.get_walk_direction(map_layer.width-1, 0)
        center = map_layer.get_walk_direction(int(map_layer.width/2), int(map_layer.height/2))
        self.assertIn(top_left, [1, 2])
        self.assertIn(top_right, [2, 3])
        self.assertIn(bottom_left, [0, 1])
        self.assertIn(bottom_right, [0, 3])
        self.assertIn(center, [0, 1, 2, 3])

    def test_update_dungeon_coords(self):
        map_layer = MapLayer()
        x = 10
        y = 10
        step_one = map_layer.update_dungeon_coords(x, y, 0)
        step_two = map_layer.update_dungeon_coords(step_one[0], step_one[1], 1)
        step_three = map_layer.update_dungeon_coords(step_two[0], step_two[1], 2)
        step_four = map_layer.update_dungeon_coords(step_three[0], step_three[1], 3)
        self.assertEqual(step_one[1], y+1)
        self.assertEqual(step_two[0], x+1)
        self.assertEqual(step_three[1], y)
        self.assertEqual(step_four[0], x)


    def test_generate_mean_dungeon_size(self):
        map_layer = MapLayer()
        self.assertGreaterEqual(map_layer.generate_patch_size(20), 0)

    def test_generate_random_start_point(self):
        map_layer = MapLayer()
        for _ in range(100):
            self.assertIn(map_layer.generate_random_start_point()[0], range(0, map_layer.width))
            self.assertIn(map_layer.generate_random_start_point()[1], range(0, map_layer.height))

    def test_generate_blank_row(self):
        map_layer = MapLayer()
        map_layer.generate_blank_row()
        self.assertEqual(map_layer.map_layer_matrix[0], ['X' for i in range(map_layer.width)])

    def test_generate_blank_map(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        self.assertEqual(map_layer.map_layer_matrix, [['X' for i in range(map_layer.width)] for j in range(map_layer.height)] )

    def test_generate_border_walls(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_border_walls()
        self.assertEqual(map_layer.map_layer_matrix[0], ['O' for i in range(map_layer.width)])

    def test_generate_shop(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_shop()
        shop_in_map = False
        for row in map_layer.map_layer_matrix:
            if 'S' in row:
                shop_in_map = True
        self.assertTrue(shop_in_map)

    def test_generate_gold(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_gold()
        gold_in_map = False
        for row in map_layer.map_layer_matrix:
            if 'G' in row:
                gold_in_map = True
                break
        self.assertTrue(gold_in_map)

    def test_generate_coal(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_coal()
        coal_in_map = False
        for row in map_layer.map_layer_matrix:
            if 'C' in row:
                coal_in_map = True
                break
        self.assertTrue(coal_in_map)

    def test_generate_dungeon(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_dungeon()
        dungeon_in_map = False
        for row in map_layer.map_layer_matrix:
            if ' ' in row:
                dungeon_in_map = True
        self.assertTrue(dungeon_in_map)

    def test_generate_drillable_zones(self):
        map_layer = MapLayer()
        map_layer.generate_blank_map()
        map_layer.generate_drillable_zones()
        dungeon_in_map = False
        for row in map_layer.map_layer_matrix:
            if 'D' in row:
                dungeon_in_map = True
        self.assertTrue(dungeon_in_map)


