from __future__ import annotations
import typing
from DrillDungeonGame.entity import Entity
from DrillDungeonGame.entity.mixins import DiggingMixin


class Bullet(Entity, DiggingMixin):
    def __init__(self, center_x: typing.Union[float, int], center_y: typing.Union[float, int],
                 angle: float, speed: typing.Union[float, int] = 7):
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle)