from __future__ import annotations

from typing import Callable, Union, Dict, Tuple

import math


class ControllableMixin:
    speed: Union[float, int]
    set_velocity: Callable[[Tuple[float, float]], None]
    look_at: Callable[[float, float], None]
    center_x: float
    center_y: float

    def handle_key_press_release(self, keys: Dict[str, bool]):
        """Handles how the Entity should move/rotate. Handles 8-way directional wasd movement.
        We sum up the x, y velocity vector for each corresponding key press.
        This has the BIG benefit of making two keys opposite in direction (w,s) and (a,d) cancelling out, but
        also means diagonal movement results in being faster. We can fix this by normalizing the vector at the end."""
        x, y = 0, 0
        if keys['W']:
            y += 1
        if keys['A']:
            x -= 1
        if keys['S']:
            y -= 1
        if keys['D']:
            x += 1

        normal = (x * x) + (y * y)
        if normal != 0:
            normal = math.sqrt(abs(normal))
            x = x / normal
            y = y / normal

        x, y = x * self.speed, y * self.speed
        self.set_velocity((x, y))
        if x != 0 or y != 0:
            self.look_at(self.center_x + x, self.center_y + y)
