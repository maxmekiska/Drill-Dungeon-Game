import unittest

import arcade

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.entity.mixins import DiggingMixin
from DrillDungeonGame.inventory import Inventory
from DrillDungeonGame.map import DirtBlock, GoldBlock, CoalBlock
from DrillDungeonGame.sprite_container import SpriteContainer


class FakeDiggingEntity(Entity, DiggingMixin):
    def __init__(self, *args, **kwargs):
        super().__init__('resources/images/drills/drill_v3/drill_both_1.png',
                         1.0,
                         100,
                         100)
        DiggingMixin.__init__(self)
        self.inventory = Inventory(coal=0, gold=0)


class FakeBlockGrid:
    def break_block(self, block, sprites):
        block.remove_from_sprite_lists()


class DiggingMixinTestCase(unittest.TestCase):

    def test_digging_with_gameloop(self):
        sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),)
        b = DirtBlock(0, 0, 100, 100)  # One dirt block horizontal
        sprites.destructible_blocks_list.append(b)
        block_grid = FakeBlockGrid()
        e = FakeDiggingEntity()
        e.set_velocity((1, 0))
        self.assertIn(b, sprites.destructible_blocks_list)

        time = 0
        delta_time = 0.1
        frame = 0
        for i in range(1000):  # Game loop mock. iterate 1000 ticks.
            time += delta_time
            frame += 1

            e.update(time, delta_time, sprites, block_grid)

        self.assertNotIn(b, sprites.destructible_blocks_list)

    def test_gold_coal_increment(self):
        sprites = SpriteContainer(None, arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                  arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),)
        b1 = CoalBlock(0, 0, 100, 100)  # One dirt block horizontal
        b2 = GoldBlock(0, 0, 100, 100)  # One dirt block horizontal
        sprites.destructible_blocks_list.append(b1)
        sprites.destructible_blocks_list.append(b2)

        block_grid = FakeBlockGrid()
        e = FakeDiggingEntity()
        e.set_velocity((1, 0))
        self.assertIn(b1, sprites.destructible_blocks_list)
        self.assertIn(b2, sprites.destructible_blocks_list)

        self.assertEqual(e.inventory.coal, 0)
        self.assertEqual(e.inventory.gold, 0)

        time = 0
        delta_time = 0.1
        frame = 0
        for i in range(1000):  # Game loop mock. iterate 1000 ticks.
            time += delta_time
            frame += 1

            e.update(time, delta_time, sprites, block_grid)

        self.assertNotIn(b1, sprites.destructible_blocks_list)
        self.assertNotIn(b2, sprites.destructible_blocks_list)

        self.assertEqual(e.inventory.coal, 1)
        self.assertEqual(e.inventory.gold, 1)