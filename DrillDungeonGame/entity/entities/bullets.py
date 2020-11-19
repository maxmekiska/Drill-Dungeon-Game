from typing import Union, Tuple

import arcade

from ..bullet import Bullet
from ..entity import Entity
from DrillDungeonGame.particles.explosion import ParticleGold, PARTICLE_COUNT, Smoke, ParticleCoal, ParticleDirt


class BouncingBullet(Bullet):
    def __init__(self, parent: Entity, relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 angle: float = 0.0, speed: Union[float, int] = 7, max_collisions: int = 1) -> None:
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        damage = 15
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, damage=damage)

        # The number of times the bullet can bounce until it explodes
        self.max_collisions = max_collisions
        self._number_of_collisions = 0

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        self._number_of_collisions += 1
        # if self._number_of_collisions <


class BlueNormalBullet(Bullet):
    def __init__(self, parent: Entity, relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 angle: float = 0.0, speed: Union[float, int] = 7) -> None:
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        damage = 15
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, damage=damage)

    @staticmethod
    def _make_explosion_particles(particle, position: Tuple[float, float], time: float, sprites) -> None:
        for i in range(PARTICLE_COUNT):
            p = particle(sprites.explosion_list)
            p.position = position
            sprites.explosion_list.append(p)

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        if sprite in sprites.gold_list:
            self._make_explosion_particles(ParticleGold, sprite.position, time, sprites)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.coal_list:
            self._make_explosion_particles(ParticleCoal, sprite.position, time, sprites)
            smoke = Smoke(50)
            smoke.position = sprite.position
            sprites.explosion_list.append(smoke)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.dirt_list:
            self._make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.indestructible_blocks_list:
            self._make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
            self.remove_from_sprite_lists()

        # The second and statement here makes sure the bullet doesnt belong to the sprite that shot it.
        elif sprite in (*sprites.enemy_list, sprites.drill):
            # Little check to make sure the bullet isn't hitting the turret or any parent. Bullets spawn inside this.
            if sprite not in self.parents:
                self._make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
                smoke = Smoke(50)
                smoke.position = sprite.position
                sprites.explosion_list.append(smoke)

                self.remove_from_sprite_lists()
                if hasattr(sprite, 'hurt'):
                    sprite.hurt(self.damage)
