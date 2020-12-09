import unittest

import arcade

from DrillDungeonGame.entity.entities import BlueNormalBullet
from DrillDungeonGame.entity.entity import Entity, ChildEntity
from DrillDungeonGame.entity.mixins import ShootingMixin, ShotType
from DrillDungeonGame.map import BlockGrid
from DrillDungeonGame.sprite_container import SpriteContainer

from tests.test_entity import create_mock_entity, create_mock_child_entity


class FakeShootableEntity(Entity, ShootingMixin):
    def __init__(self, *args, **kwargs):
        super().__init__('resources/images/drills/drill_v3/drill_both_1.png',
                         1.0,
                         100,
                         100)
        self.firing_mode = ShotType.SINGLE
        self.bullet_type = BlueNormalBullet
        self.firing_rate = 1
        ShootingMixin.__init__(self)


class ShootingMixinTestCase(unittest.TestCase):

    def test_init(self):
        e = FakeShootableEntity()

        self.assertEqual(e._trigger_pulled, False)
        self.assertEqual(e._last_shoot_time, 0)

        e.pull_trigger()
        self.assertEqual(e._trigger_pulled, True)
        e.pull_trigger()
        self.assertEqual(e._trigger_pulled, True)
        e.release_trigger()
        self.assertEqual(e._trigger_pulled, False)

    def test_shooting_with_gameloop(self):
        angle = 100.0
        e = FakeShootableEntity(angle)
        sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),)

        time = 0
        delta_time = 0.1
        frame = 0
        bullets_shot = 0
        for i in range(1200):  # Game loop mock
            time += delta_time
            frame += 1

            if frame < 1000:
                if frame % 100 == 0:
                    e.shoot(ShotType.SINGLE)
                    bullets_shot += 1

                if frame + 50 % 100 == 0:
                    e.shoot(ShotType.BUCKSHOT)
                    bullets_shot += 3

            else:
                if frame == 1000:
                    e.pull_trigger()

                if frame == 1100:
                    e.release_trigger()
                    # Should have shot 5 bullets. 0.1 delta time. fire rate is 1.0
                    bullets_shot += 10

            e.update(time, delta_time, sprites, None)

        for bullet in e.children:
            self.assertEqual(bullet.angle, e.angle)  # Bullet angle should match parent.
            self.assertNotEqual(bullet.position, e.position)  # Bullets should have moved
        self.assertEqual(len(e.children), bullets_shot)
