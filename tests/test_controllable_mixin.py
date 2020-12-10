import unittest

import arcade

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.entity.mixins import ControllableMixin
from DrillDungeonGame.map import DungeonWallBlock
from DrillDungeonGame.sprite_container import SpriteContainer


class FakeControllableEntity(Entity, ControllableMixin):
    def __init__(self, *args, **kwargs):
        super().__init__('resources/images/drills/drill_v3/drill_both_1.png',
                         1.0,
                         0.0,
                         0.0)
        ControllableMixin.__init__(self)


class FakeBlockGrid:
    def break_block(self, block, sprites):
        block.remove_from_sprite_lists()


class ControllableMixinTestCase(unittest.TestCase):

    def test_controlling_mixin(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}
        self.assertEqual(e.velocity, [0.0, 0.0])

        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_up_movement(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        keys_pressed['W'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 1.0])

        keys_pressed['W'] = False
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_down_movement(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        keys_pressed['S'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, -1.0])

        keys_pressed['S'] = False
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_right_movement(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        keys_pressed['D'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [1.0, 0.0])

        keys_pressed['D'] = False
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_left_movement(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        keys_pressed['A'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [-1.0, 0.0])

        keys_pressed['A'] = False
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_diagonal_movement(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        keys_pressed['W'] = True
        keys_pressed['D'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertGreater(e.change_x, 0.0)
        self.assertGreater(e.change_y, 0.0)

        keys_pressed['W'] = False
        keys_pressed['D'] = False
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_opposite_keys_cancel(self):
        e = FakeControllableEntity(speed=1.0)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}
        keys_pressed['W'] = True
        keys_pressed['S'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

        keys_pressed['A'] = True
        keys_pressed['D'] = True
        e.handle_key_press_release(keys_pressed)
        self.assertEqual(e.velocity, [0.0, 0.0])

    def test_collidable_walls_with_gameloop(self):
        sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), )

        e = FakeControllableEntity()
        b = DungeonWallBlock(0, 0, 0.0, 100.0)  # One dirt block above the entity
        sprites.indestructible_blocks_list.append(b)
        block_grid = FakeBlockGrid()

        e.setup_collision_engine([sprites.indestructible_blocks_list])
        self.assertIn(b, sprites.indestructible_blocks_list)

        e.set_velocity((0, 1))
        time = 0
        delta_time = 0.1
        frame = 0
        for i in range(1000):  # Game loop mock. iterate 1000 ticks.
            time += delta_time
            frame += 1

            e.update(time, delta_time, sprites, block_grid)

        print(e.position)
        self.assertEqual(e.center_x, 0.0)
        self.assertLess(e.center_y, 50.0)  # Entity has not moved much due to colliding with the wall.

