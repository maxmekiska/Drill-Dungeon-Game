from __future__ import annotations

from typing import Union

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.entity.mixins.bullet_physics_mixin import BulletPhysicsMixin


class Bullet(Entity, BulletPhysicsMixin):
    def __init__(self, center_x: Union[float, int], center_y: Union[float, int],
                 angle: float, speed: Union[float, int] = 7):
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle)
