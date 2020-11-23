from __future__ import annotations

from typing import Union

import arcade

from DrillDungeonGame.entity.entity import ChildEntity, Entity


class Bullet(ChildEntity):
    def __init__(self, base_sprite: str, sprite_scale: Union[float, int], parent: Entity,
                 relative_x: Union[float, int], relative_y: Union[float, int], speed: Union[float, int],
                 angle: float = 0.0, damage: Union[float, int] = 0):
        super().__init__(base_sprite, sprite_scale, parent, relative_x=relative_x, relative_y=relative_y,
                         speed=speed, angle=angle, maintain_parent_angle=False, maintain_relative_position=False)
        self.damage = damage

    def update(self, time: float, sprites) -> None:
        for sprite_list in (sprites.all_blocks_list, sprites.entity_list, sprites.drill_list):
            collisions = arcade.check_for_collision_with_list(self, sprite_list)

            # We might want to change this behaviour to instead loop over all collisions. The reason we only use the
            # first collision is because otherwise at the end of a gameloop, a bullet could be overlapping with up to
            # 4 (usually at most 3) blocks. One bullet could remove many blocks. We only want 1 bullet to remove 1 block
            if len(collisions) > 0:
                self.on_collision(collisions[0], time, sprites)

        super().update(time, sprites)