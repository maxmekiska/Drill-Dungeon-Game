from __future__ import annotations

from typing import Union

from DrillDungeonGame.entity.entity import Entity
from DrillDungeonGame.particles.explosion import ParticleGold, PARTICLE_COUNT, Smoke, ParticleCoal, ParticleDirt


class Bullet(Entity):
    def __init__(self, center_x: Union[float, int], center_y: Union[float, int],
                 angle: float, speed: Union[float, int] = 7):
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        super().__init__(base_sprite, sprite_scale, center_x, center_y, speed=speed, angle=angle)

    def update_physics_engine(self, time: float, sprites) -> None:
        collision_list = []
        for engine in self._physics_engines:
            collision_list = engine.update()

        for block in collision_list:
            if block in sprites.gold_list:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleGold(sprites.explosion_list)
                    particle.position = block.position
                    sprites.explosion_list.append(particle)

            elif block in sprites.coal_list:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleCoal(sprites.explosion_list)
                    particle.position = block.position
                    sprites.explosion_list.append(particle)

                smoke = Smoke(50)
                smoke.position = block.position
                sprites.explosion_list.append(smoke)

            elif block in sprites.dirt_list:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleDirt(sprites.explosion_list)
                    particle.position = block.position
                    sprites.explosion_list.append(particle)

            elif block in sprites.indestructible_blocks_list:
                for i in range(PARTICLE_COUNT):
                    particle = ParticleDirt(sprites.explosion_list)
                    particle.position = block.position
                    sprites.explosion_list.append(particle)

            self.remove_from_sprite_lists()
            if block not in sprites.indestructible_blocks_list:
                block.remove_from_sprite_lists()
