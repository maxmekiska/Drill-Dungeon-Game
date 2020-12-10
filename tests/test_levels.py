import unittest


from DrillDungeonGame.level import *


class LevelTestCase(unittest.TestCase):
    def test_map_layer_generation(self):
        level = Level(Drill(10, 10))
        self.assertGreater(len(level.sprites.all_blocks_list), 0)

    def test_enemy_generation(self):
        level = Level(Drill(10, 10))
        self.assertGreater(len(level.sprites.enemy_list), 0)



