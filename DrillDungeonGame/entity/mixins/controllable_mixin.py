from __future__ import annotations

import math
from typing import Callable, Union, Dict, Tuple


class ControllableMixin:
    """
    Class to handle all controls over the drill.

    Methods
    -------
    handle_key_press_release(keys: Dict[str, bool])
        Handles 8 way movement of drill.
    handle_mouse_click(self, button: int)
        Executes logic when mouse buttons are pressed.
    handle_mouse_release(button: int)
        Executes logic when mouse buttons are released.

    """
    speed: Union[float, int]
    set_velocity: Callable[[Tuple[float, float]], None]
    look_at: Callable[[float, float], None]
    center_x: float
    center_y: float
    distance_moved: float
    change_x: float
    change_y: float

    def handle_key_press_release(self, keys: Dict[str, bool]) -> None:
        """
        Called when a key is pressed or released. Handles how the Entity should move/rotate. Uses 8-way directional
        wasd movement.

        Notes
        -----
        We sum up the x, y velocity vector for each corresponding key press.
        This has the big benefit of making two keys opposite in direction (w,s) and (a,d) cancelling out, but
        also means diagonal movement results in being faster. We can fix this by normalizing the vector at the end.

        Parameters
        ----------
        keys: Dict[str, bool]
            A dictionary of all keys and a bool corresponding to whether it is pressed or not.

        """

        x, y = 0, 0
        if keys['W']:
            y += 1
        if keys['A']:
            x -= 1
        if keys['S']:
            y -= 1
        if keys['D']:
            x += 1

        normal = (x * x) + (y * y)
        if normal != 0:
            normal = math.sqrt(abs(normal))
            x = x / normal
            y = y / normal

        x, y = x * self.speed, y * self.speed
        self.set_velocity((x, y))
        if any([keys['W'], keys['A'], keys['S'], keys['D']]):
            self.look_at(self.center_x + x, self.center_y + y)

    def handle_mouse_click(self, button: int) -> None:
        """
        Called when left or right mouse button are pressed.

        Notes
        -----
        Override this function in a subclass to provide functionality here.

        Parameters
        ----------
        button: int
            The button pressed. 1 = Left click, 4 = Right click.

        """
        pass

    def handle_mouse_release(self, button: int) -> None:
        """
        Called when left or right mouse button are released.

        Notes
        -----
        Override this function in a subclass to provide functionality here.

        Parameters
        ----------
        button: int
            The button pressed. 1 = Left click, 4 = Right click.
        """
        pass
