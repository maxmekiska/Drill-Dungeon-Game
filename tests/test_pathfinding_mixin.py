import unittest

import arcade

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.entity.mixins import PathFindingMixin
from DrillDungeonGame.map import DirtBlock
from DrillDungeonGame.sprite_container import SpriteContainer


class FakePathFindingEntity(Entity, PathFindingMixin):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__('resources/images/drills/drill_v3/drill_both_1.png',
                         0.3,
                         x, y)
        PathFindingMixin.__init__(self, vision=kwargs.get('vision'))


class FakeBlockGrid:
    def break_block(self, block, sprites):
        block.remove_from_sprite_lists()


class PathFindingMixinTestCase(unittest.TestCase):

    def test_path_no_obstacles_with_game_loop(self):
        # Spawns two enemies and dirt blocks inbetween them
        e1 = FakePathFindingEntity(-100, 0, speed=1.0, vision=300)
        e2 = FakePathFindingEntity(100, 0, speed=1.0, vision=300)
        block_grid = FakeBlockGrid()
        obstacles = arcade.SpriteList()
        sprites = None
        for y in range(-100, 100, 20):
            obstacles.append(DirtBlock(0, 0, 0, y))

        e1.path_to_entity(e2, obstacles, diagonal_movement=True)
        self.assertFalse(e1.has_line_of_sight_with(e2, obstacles))

        time = 0
        delta_time = 0.1
        frame = 0
        for i in range(1000):  # Game loop mock. iterate 1000 ticks.
            time += delta_time
            frame += 1

            e1.update(time, delta_time, sprites, block_grid)
            e2.update(time, delta_time, sprites, block_grid)

            collisions = arcade.check_for_collision_with_list(e1, obstacles)
            self.assertEqual(collisions, [])

        self.assertAlmostEqual(e1.center_x, e2.center_x, delta=20)
        self.assertAlmostEqual(e1.center_y, e2.center_y, delta=20)

    def test_path_with_obstacles_with_game_loop(self):
        start_position = (50, 50)
        e1 = FakePathFindingEntity(*start_position, speed=10.0, vision=200)
        e2 = FakePathFindingEntity(0, 0, speed=10.0, vision=200)
        block_grid = FakeBlockGrid()
        sprites = None

        e1.path_to_entity(e2, arcade.SpriteList(), diagonal_movement=True)

        time = 0
        delta_time = 0.1
        for i in range(100):  # Game loop mock. iterate 1000 ticks.
            time += delta_time

            e1.update(time, delta_time, sprites, block_grid)
            e2.update(time, delta_time, sprites, block_grid)

        self.assertLess(e1.center_x, start_position[0])
        self.assertLess(e1.center_y, start_position[1])

    def test_path_to_position(self):
        e1 = FakePathFindingEntity(0, 0, speed=1.0, vision=200)
        e2 = FakePathFindingEntity(150, 0, speed=1.0, vision=200)

        self.assertEqual(e1.path, [])
        self.assertEqual(e2.path, [])

        # With diagonal movement and has vision.
        e1.path_to_position(e2.center_x, e2.center_y, arcade.SpriteList(), diagonal_movement=True)
        self.assertGreater(len(e1.path), 2)

        # Without diagonal movement and has vision.
        e1.path_to_position(e2.center_x, e2.center_y, arcade.SpriteList(), diagonal_movement=False)
        self.assertGreater(len(e1.path), 2)

        # With diagonal movement and out of vision range.
        e1.vision = 100
        e1.path_to_position(e2.center_x, e2.center_y, arcade.SpriteList(), diagonal_movement=True)
        self.assertEqual(e1.path, [])

        # Without diagonal movement and out of vision range.
        e1.path_to_position(e2.center_x, e2.center_y, arcade.SpriteList(), diagonal_movement=False)
        self.assertEqual(e1.path, [])

    def test_path_to_entity(self):
        e1 = FakePathFindingEntity(0, 0, speed=1.0, vision=200)
        e2 = FakePathFindingEntity(150, 0, speed=1.0, vision=200)

        self.assertEqual(e1.path, [])
        self.assertEqual(e2.path, [])

        # With diagonal movement and has vision.
        e1.path_to_entity(e2, arcade.SpriteList(), diagonal_movement=True)
        self.assertGreater(len(e1.path), 2)

        # Without diagonal movement and has vision.
        e1.path_to_entity(e2, arcade.SpriteList(), diagonal_movement=False)
        self.assertGreater(len(e1.path), 2)

        # With diagonal movement and out of vision range.
        e1.vision = 100
        e1.path_to_entity(e2, arcade.SpriteList(), diagonal_movement=True)
        self.assertEqual(e1.path, [])

        # Without diagonal movement and out of vision range.
        e1.path_to_entity(e2, arcade.SpriteList(), diagonal_movement=False)
        self.assertEqual(e1.path, [])
