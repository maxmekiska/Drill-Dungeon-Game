from typing import Union, Type

from DrillDungeonGame.entity.bullet import Bullet
from DrillDungeonGame.entity.entity import ChildEntity, Entity
from DrillDungeonGame.entity.mixins.shooting_mixin import ShootingMixin, ShotType


class Turret(ChildEntity, ShootingMixin):
    def __init__(self, base_sprite: str, sprite_scale: float, parent: Entity,
                 relative_x: Union[float, int] = 0.0, relative_y: [float, int] = 0.0,
                 speed: Union[float, int] = 1, angle: float = 0.0, bullet_type: Type[Bullet] = None,
                 firing_mode: ShotType = ShotType.SINGLE) -> None:
        super().__init__(base_sprite, sprite_scale, parent=parent,
                         relative_x=relative_x, relative_y=relative_y, maintain_relative_position=True,
                         speed=speed, angle=angle, maintain_parent_angle=False)
        ShootingMixin.__init__(self)

        self.bullet_type = bullet_type
        self.inventory = self.parent.inventory if hasattr(self.parent, 'inventory') else None
        self.firing_mode = firing_mode
