from __future__ import annotations

from typing import Union, Tuple

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.particles.explosion import ParticleGold, PARTICLE_COUNT, Smoke, ParticleCoal, ParticleDirt


class Bullet(Entity):
    def __init__(self, center_x: Union[float, int], center_y: Union[float, int],
                 angle: float, speed: Union[float, int] = 7):
        """A base class that bullets should inherit.

        Parameters
        ----------
        center_x: Union[float, int]
            The starting x position in the map for this entity.
        center_y: Union[float, int]
            The starting y position in the map for this entity.
        angle: float
            The starting angle that the bullet should be facing when shot.
        speed: Union[float, int]
            The speed that the bullet will travel at.

        """
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle)
