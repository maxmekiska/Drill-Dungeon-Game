import unittest

import arcade

from DrillDungeonGame.entity.entity import Entity, ChildEntity
from DrillDungeonGame.map import DirtBlock


class EntityTestCase(unittest.TestCase):
    def create_mock_entity(self, x, y, *args, **kwargs):
        sprite_path = 'resources/images/drills/drill_v3/drill_both_1.png'
        sprite_scale = 1.0
        return Entity(sprite_path, sprite_scale, x, y,
                      *args, **kwargs)

    def create_mock_child_entity(self, parent, *args, **kwargs):
        sprite_path = "resources/images/weapons/turret1.png"
        sprite_scale = 0.5
        return ChildEntity(sprite_path, sprite_scale, parent, *args, **kwargs)

    def test_entity_hurt_heal(self):
        max_health = 100
        current_health = 100
        e = self.create_mock_entity(100, 100,
                                    current_health=100, max_health=100)

        e.hurt(5)  # Test damaging works
        current_health -= 5
        self.assertEqual(e.current_health, current_health)
        self.assertEqual(e.max_health, max_health)

        e.heal(3)  # Test healing works.
        current_health += 3
        self.assertEqual(e.current_health, current_health)
        self.assertEqual(e.max_health, max_health)

        e.heal(100)  # Can't overheal
        current_health = max_health
        self.assertEqual(e.current_health, current_health)
        self.assertEqual(e.max_health, max_health)

        sprite_list = arcade.SpriteList()
        sprite_list.append(e)
        self.assertIn(e, sprite_list)
        child = self.create_mock_child_entity(e)
        e.children.append(child)
        self.assertIn(child, e.children)
        self.assertNotIn(child, sprite_list)

        e.hurt(100)  # kill the entity
        current_health = 0
        self.assertNotIn(e, sprite_list)
        self.assertNotIn(child, e.children)


    def test_entity_hurt_heal_invincible(self):
        e = self.create_mock_entity(100, 100,
                                    current_health=-1, max_health=100)
        e.hurt(100)
        self.assertEqual(e.current_health, -1)
        e.heal(99999)
        self.assertEqual(e.current_health, -1)
        self.assertEqual(e.max_health, 100)

        current_health = 100
        e = self.create_mock_entity(100, 100,
                                    current_health=current_health, max_health=-1)
        e.heal(600)
        current_health += 600
        self.assertEqual(e.current_health, current_health)
        self.assertEqual(e.max_health, -1)

        current_health -= 700
        e.hurt(700)
        self.assertEqual(e.current_health, 0)
        self.assertEqual(e.max_health, -1)

    def test_moving(self):
        e = self.create_mock_entity(100, 100,
                                    current_health=100, max_health=100)

        test_vector_data = (
            (1.0, 2.0),
            (-1.3, -4.9),
            (5.2, 0.0),
            (0.0, 0.0),
            (-0.01, -0.5),
        )

        for vector in test_vector_data:
            e.set_velocity(vector)
            self.assertEqual(e.change_x, vector[0])
            self.assertEqual(e.change_y, vector[1])

            e.stop_moving()
            self.assertEqual(e.change_x, 0.0)
            self.assertEqual(e.change_y, 0.0)

    def test_has_line_of_sight(self):
        blocking_sprites = arcade.SpriteList()
        for i in range(-100, 100, 20):
            s = DirtBlock(0, 0, 0, i)
            blocking_sprites.append(s)

        e1 = self.create_mock_entity(x=-100, y=0)
        e2 = self.create_mock_entity(x=100, y=0)

        self.assertFalse(e1.has_line_of_sight_with(e2, blocking_sprites))
        self.assertTrue(e1.has_line_of_sight_with(e2, arcade.SpriteList()))

