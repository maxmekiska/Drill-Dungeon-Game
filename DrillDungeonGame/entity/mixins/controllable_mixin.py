from __future__ import annotations
import arcade
import typing
import math


class ControllableMixin:
    speed: typing.Union[float, int]
    set_velocity: typing.Callable[[typing.Tuple[float, float]], None]
    look_at: typing.Callable[[float, float], None]

    def update_keys(self, keys: typing.Dict[str, bool]):
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
        # print(f"{x}, {y}")
        self.set_velocity((x, y))
        self.look_at(self.center_x + x, self.center_y + y)
