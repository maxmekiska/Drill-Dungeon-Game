from typing import Union

from ..entity import ChildEntity, Entity


class Shield(ChildEntity):
    """

    Represents a shield entity. This is always a child to another entity.

    """

    def __init__(self, base_sprite: str, sprite_scale: float, parent: Entity,
                 relative_x: Union[float, int] = 0.0, relative_y: Union[float, int] = 0.0,
                 angle: float = 0.0) -> None:
        """

        Parameters
        ----------
        base_sprite     :   str
            The path to the file containing the sprite for this entity.
        sprite_scale    :   float
            The scale to draw the sprite for this entity
        parent          :   Entity
            The parent entity.
        relative_x      :   Union[float, int]
            The x position, relative to the parent.
        relative_y      :   Union[float, int]
            The y position, relative to the parent.
        angle           :   float
            The starting rotation angle of the sprite.

        """

        super().__init__(base_sprite, sprite_scale, parent=parent,
                         relative_x=relative_x, relative_y=relative_y, maintain_relative_position=True,
                         angle=angle, maintain_parent_angle=True)
        self.alpha = 200  # Set transparency to about 70%.
