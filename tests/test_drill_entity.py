from DrillDungeonGame.entity.entities import Drill, ShotType
import arcade

import unittest

from DrillDungeonGame.sprite_container import SpriteContainer


class DrillTestCase(unittest.TestCase):
    def test_drill_firing_mode(self):
        d = Drill(0, 0, speed=1)
        keys_pressed = {key: False for key in arcade.key.__dict__.keys() if not key.startswith('_')}

        self.assertEqual(d.children[0].firing_mode, ShotType.SINGLE)
        keys_pressed['B'] = True
        d.handle_key_press_release(keys_pressed)
        self.assertEqual(d.children[0].firing_mode, ShotType.BUCKSHOT)

    def test_drill_mouse_actions(self):
        d = Drill(0, 0, speed=1)
        sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),)

        RIGHT = 4
        LEFT = 1

        self.assertEqual(d.children[0]._trigger_pulled, False)
        d.handle_mouse_click(LEFT)
        self.assertEqual(d.children[0]._trigger_pulled, True)
        d.handle_mouse_release(LEFT)
        self.assertEqual(d.children[0]._trigger_pulled, False)

        self.assertEqual(d.shield_enabled, False)
        self.assertEqual(d._total_shield_uptime, 0.0)

        d.handle_mouse_click(RIGHT)
        self.assertEqual(d.shield_enabled, True)
        d.handle_mouse_release(RIGHT)
        self.assertEqual(d.shield_enabled, False)
