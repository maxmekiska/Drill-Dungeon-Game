from typing import Union, Type

from DrillDungeonGame.entity.bullet import Bullet
from DrillDungeonGame.entity.entity import ChildEntity, Entity
from DrillDungeonGame.entity.mixins.shooting_mixin import ShootingMixin, ShotType


class Turret(ChildEntity, ShootingMixin):
    """

    Represents a turret entity. This is always a child to another entity.

    """
    def __init__(self, base_sprite: str, sprite_scale: float, parent: Entity,
                 relative_x: Union[float, int] = 0.0, relative_y: [float, int] = 0.0,
                 angle: float = 0.0, speed: Union[float, int] = 1, bullet_type: Type[Bullet] = None,
                 firing_mode: ShotType = ShotType.SINGLE, firing_rate: Union[float, int] = 0.2) -> None:
        """

        Parameters
        ----------
        base_sprite     :   str
            The path to the file containing the sprite for this entity.
        sprite_scale    :   float
            The scale to draw the sprite for this entity
        parent          :   Entity
            The entity that created/fired this bullet.
        relative_x      :   Union[float, int]
            The x position, relative to the parent to spawn the bullet at.
        relative_y      :   Union[float, int]
            The y position, relative to the parent to spawn the bullet at.
        angle           :   float
            The starting angle that the bullet should be facing when shot.
        speed           :   Union[float, int]
            The speed that the bullet will travel at.
        bullet_type     :   Type[Bullet]
            The bullet that this turret shoots.
        firing_mode     :   ShotType
            The type of shot to fire the bullet in. Defaults to ShotType.SINGLE. ShotType.BUCKSHOT is another option.
        firing_rate     :   Union[float, int]
            The firing rate of the turret in seconds.

        Returns
        -------
        None

        """

        super().__init__(base_sprite, sprite_scale, parent=parent,
                         relative_x=relative_x, relative_y=relative_y, maintain_relative_position=True,
                         speed=speed, angle=angle, maintain_parent_angle=False)
        ShootingMixin.__init__(self)

        self.bullet_type = bullet_type
        self.inventory = self.parent.inventory if hasattr(self.parent, 'inventory') else None
        self.firing_mode = firing_mode
        self.firing_rate = firing_rate
