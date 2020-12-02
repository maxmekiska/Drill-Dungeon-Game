from DrillDungeonGame.obscure_vision import ObscuredVision
import unittest
import logging


class ObscureVisionTestCase(unittest.TestCase):

    def test_obscure_vision_init(self):
        test_data = [
            (100, 200, True),
            (200, 100, False),
            (50, 100.5, True),
            (-1, 100, False),
            (100, -50, False),
            (1000, -25, False),
            (200, 500, True),
            (100, 101, True)
        ]

        for vision, max_vision, passes in test_data:
            logging.debug(f'{vision}, {max_vision}, {passes}')

            if not passes:
                self.assertRaises(ValueError, ObscuredVision, vision, max_vision)
                continue

            # Only valid data now
            o = ObscuredVision(vision, max_vision)
            self.assertEqual(o.vision, vision)
            self.assertEqual(o._max_vision, max_vision)
            self.assertEqual(o._center_alpha, 0)
            self.assertEqual(o._outer_alpha, 255)

            increase_amount = 30
            new_vision = min(vision + 30, max_vision, o._image_diagonal_diameter)
            o.increase_vision(increase_amount)
            self.assertEqual(o.vision, new_vision)

            o.vision = vision  # Reset vision
            self.assertEqual(o.vision, vision)

            default_dv = 50
            new_vision = max(0, vision - default_dv)
            o.decrease_vision()
            self.assertEqual(o.vision, new_vision)

            o.vision = vision  # Reset vision
            self.assertEqual(o.vision, vision)

            o.far_sight()
            self.assertEqual(o._outer_alpha, 0)
            self.assertEqual(o._center_alpha, 0)
            self.assertEqual(o.vision, vision)

            o.blind()
            self.assertEqual(o._outer_alpha, 255)
            self.assertEqual(o._center_alpha, 255)
            self.assertEqual(o.vision, vision)
