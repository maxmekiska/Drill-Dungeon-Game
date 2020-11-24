from typing import Union, Tuple

import arcade

from ..bullet import Bullet
from ..entity import Entity
from ...utility.utility import make_explosion_particles
from DrillDungeonGame.particles.explosion import ParticleGold, Smoke, ParticleCoal, ParticleDirt


class BouncingBullet(Bullet):
    """

    Class to define the collision behaviour of a Bullet.

    Methods
    -------
    on_collision(sprite: arcade.Sprite, time:float, sprites)
        Counts the number of collisions.

    """
    def __init__(self, parent: Entity, relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 angle: float = 0.0, speed: Union[float, int] = 7, max_collisions: int = 1) -> None:
        """

        Parameters
        ----------
        parent          :   Entity
            The Bullet.
        relative_x      :   Union[float, int]
            The x position, relative to the parent.
        relative_y      :   Union[float, int]
            The y position, relative to the parent.
        angle           :   float
            Angle of bullet trajectory.
        speed           :   Union[float, int]
            Speed at what bullet is moving.
        max_collisions  :   int
            Number of maximum collisions until bullet is removed/destroyed.

        Returns
        -------
        None

        """

        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        damage = 15
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, damage=damage)

        # The number of times the bullet can bounce until it explodes
        self.max_collisions = max_collisions
        self._number_of_collisions = 0

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        """

        Method to count number of collisions.

        Parameters
        ----------
        sprite  :   arcade.Sprite
            The sprite that the Entity collided with.
        time    :   float
            The time that the collision happened.
        sprites :   arcade.Sprite
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        Returns
        -------
        None

        """
        self._number_of_collisions += 1
        # if self._number_of_collisions <


class BlueNormalBullet(Bullet):
    def __init__(self, parent: Entity, relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 angle: float = 0.0, speed: Union[float, int] = 3) -> None:
        """

        Represents a basic blue bullet.
        Removed upon collision.
        Damages and makes explosion particles.

        Parameters
        ----------
        parent      :   Entity
            The entity that created fired this bullet.
        relative_x  :   Union[float, int]
            The x position, relative to the parent to spawn the bullet at.
        relative_y  :   Union[float, int]
            The y position, relative to the parent to spawn the bullet at.
        angle       :   float
            The starting angle that the bullet should be facing when shot.
        speed       :   Union[float, int]
            The speed that the bullet will travel at.

        Methods
        -------
        on_collision(sprite:arcade.Sprite, time: float, sprites)
            Bullet specific collision logic.

        """
        base_sprite = ":resources:images/space_shooter/laserBlue01.png"
        sprite_scale = 0.4
        damage = 15
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, damage=damage)

    def on_collision(self, sprite: arcade.Sprite, time: float, sprites) -> None:
        """
        Bullet specific logic to do when it collides with another object.
        This bullet creates explosion particles as well as hurting the colliding sprite if it has a health attribute.

        Parameters
        ----------
        sprite  :   arcade.Sprite
            The sprite that the Entity collided with.
        time    :   float
            The time that the collision happened.
        sprites :   SpriteContainer
            The SpriteContainer class which contains all sprites so we can interact and do calculations with them.

        """
        if sprite in sprites.gold_list:
            make_explosion_particles(ParticleGold, sprite.position, time, sprites)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.coal_list:
            make_explosion_particles(ParticleCoal, sprite.position, time, sprites)
            smoke = Smoke(50)
            smoke.position = sprite.position
            sprites.explosion_list.append(smoke)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.dirt_list:
            make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
            sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        elif sprite in sprites.indestructible_blocks_list:
            make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
            self.remove_from_sprite_lists()

        # The second and statement here makes sure the bullet doesnt belong to the sprite that shot it.
        elif sprite in (*sprites.enemy_list, sprites.drill):
            # Little check to make sure the bullet isn't hitting the turret or any parent. Bullets spawn inside this.
            if sprite not in self.get_all_parents:
                make_explosion_particles(ParticleDirt, sprite.position, time, sprites)
                smoke = Smoke(50)
                smoke.position = sprite.position
                sprites.explosion_list.append(smoke)

                self.remove_from_sprite_lists()
                if hasattr(sprite, 'hurt'):
                    sprite.hurt(self.damage)
