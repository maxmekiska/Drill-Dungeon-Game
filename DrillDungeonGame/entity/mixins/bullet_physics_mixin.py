import arcade

from DrillDungeonGame.particles.explosion import ParticleDirt, PARTICLE_COUNT, ParticleCoal, Smoke, ParticleGold

from typing import Callable


class BulletPhysicsMixin:
    remove_from_sprite_lists: Callable[[None], None]

    def update(self, time: float, sprites) -> None:
        # START COLLISION CHECKING
        hit_list_wall = arcade.check_for_collision_with_list(self, sprites.dirt_list)
        hit_list_coal = arcade.check_for_collision_with_list(self, sprites.coal_list)
        hit_list_gold = arcade.check_for_collision_with_list(self, sprites.gold_list)
        # remove bullet
        if len(hit_list_wall) > 0:
            self.remove_from_sprite_lists()

        # remove hit wall
        for wall in hit_list_wall:
            # explosion and smoke when wall hit
            for i in range(PARTICLE_COUNT):
                particle = ParticleDirt(sprites.explosion_list)
                particle.position = wall.position
                sprites.explosion_list.append(particle)
                wall.remove_from_sprite_lists()

        if len(hit_list_coal) > 0:
            self.remove_from_sprite_lists()
        for coal in hit_list_coal:
            for i in range(PARTICLE_COUNT):
                particle = ParticleCoal(sprites.explosion_list)
                particle.position = coal.position
                sprites.explosion_list.append(particle)

            smoke = Smoke(50)
            smoke.position = coal.position
            sprites.explosion_list.append(smoke)
            coal.remove_from_sprite_lists()

        if len(hit_list_gold) > 0:
            self.remove_from_sprite_lists()

        for gold in hit_list_gold:
            for i in range(PARTICLE_COUNT):
                particle = ParticleGold(sprites.explosion_list)
                particle.position = gold.position
                sprites.explosion_list.append(particle)

                gold.remove_from_sprite_lists()

        # later also add for enemies
