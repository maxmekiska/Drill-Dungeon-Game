import unittest

import arcade

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.entity.mixins import ControllableMixin


class FakeControllableEntity(Entity, ControllableMixin):
    def __init__(self, *args, **kwargs):
        super().__init__('resources/images/drills/drill_v3/drill_both_1.png',
                         1.0,
                         100,
                         100)
        ControllableMixin.__init__(self)


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