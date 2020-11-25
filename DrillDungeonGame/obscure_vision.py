import math
from typing import Union

from .utility.constants import SCREEN_HEIGHT, SCREEN_WIDTH, VIEWPOINT_MARGIN
import arcade

from DrillDungeonGame.utility import make_vignette


class ObscuredVision:
    """
    Represents an image which overlays the screen to limit how far the player can see. Can be centered to the camera xy.

    Methods
    -------
    draw(self, center_x: Union[float, int], center_y: Union[float, int])
        Draws the image that obscures vision of the underlying screen centered on the given coordinates.
    increase_vision(self, amount: int = 50)
        Increases the vision by a given amount.
    decrease_vision(self, amount: int = 50)
        Decreases the vision by a given amount.
    blind(self)
        Fills the vision with a black image so that you can't see anything.
    far_sight(self)
        Makes the image completely transparent so that there is no limit to how far you can see.

    """
    def __init__(self, vision: int = 200, max_vision: int = 500) -> None:
        """

        Parameters
        ----------
        vision     : int
            The starting distance that the camera can see.
        max_vision : int
            The maximum distance that the camera can see. This only limits decrease_vision and doesn't stop
            far_sight() from being called.

        """
        if vision > max_vision:
            raise ValueError(f"vision: {vision} cannot be greater than max_vision: {max_vision}")

        self._vignette_radius = vision
        self._max_vision = max_vision
        self._center_alpha = 0
        self._outer_alpha = 255
        self._image_diagonal_diameter = int(math.sqrt(pow(SCREEN_HEIGHT + (VIEWPOINT_MARGIN * 2), 2) +
                                                      pow(SCREEN_WIDTH + (VIEWPOINT_MARGIN * 2), 2)))
        self._image = None
        self._reload_image()

    def draw(self, center_x: Union[float, int], center_y: Union[float, int]) -> None:
        """Draws the image that obscures vision of the underlying screen.

        center_x : Union[float, int]
            The x value to center the the image on.
        center_y : Union[float, int]
            The y value to center the the image on.

        """
        self._image.draw_scaled(center_x, center_y, scale=1.0, angle=0, alpha=255)

    def increase_vision(self, amount: int = 50) -> None:
        """Increases the vision by a given amount.

        Parameters
        ----------
        amount : int
            The radius to increase the vision by. Defaults to +50

        """
        self._outer_alpha = 255
        self._center_alpha = 0
        new_radius = self._vignette_radius + amount
        self._vignette_radius = min(self._image_diagonal_diameter // 2, new_radius, self._max_vision)
        self._reload_image()

    def decrease_vision(self, amount: int = 50) -> None:
        """Decreases the vision by a given amount.

        Parameters
        ----------
        amount : int
            The radius to increase the vision by. Defaults to -50

        """
        self._outer_alpha = 255
        self._center_alpha = 0
        new_radius = self._vignette_radius - amount
        self._vignette_radius = max(0, new_radius)
        self._reload_image()

    def blind(self) -> None:
        """Fills the vision with a black image so that you can't see anything."""
        self._outer_alpha = 255
        self._center_alpha = 255
        self._reload_image()

    def far_sight(self) -> None:
        """Makes the image completely transparent so that there is no limit to how far you can see."""
        self._outer_alpha = 0
        self._center_alpha = 0
        self._reload_image()

    def _reload_image(self) -> None:
        self._image = make_vignette(diameter=self._image_diagonal_diameter,
                                    color=arcade.color.BLACK,
                                    vignette_radius=self._vignette_radius,
                                    center_alpha=self._center_alpha,
                                    outer_alpha=self._outer_alpha)
