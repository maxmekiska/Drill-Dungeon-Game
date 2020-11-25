import arcade

from DrillDungeonGame.utility.constants import SCREEN_WIDTH, SCREEN_HEIGHT, VIEWPOINT_MARGIN


class View:
    """

    Class to display and refresh the game window.

    Methods
    -------
    update(centre_sprite: arcade.Sprite)
        Update any changes in the game by updating the view.
    _check_for_scroll_left()
        Scrolls window to the left if player moves to the left.
    _check_for_scroll_right()
        Scrolls window to the right if player moves to the right.
    _check_for_scroll_up()
        Scrolls window up if player moves up.
    _check_for_scroll_down()
        Scrolls window down if player moves down.

    """
    def __init__(self) -> None:
        self.left_offset = 0
        self.bottom_offset = 0
        self._centre_sprite = None
        # TODO store the width/height of the screen. This can then be passed to the Entity.update() function

    def update(self, centre_sprite: arcade.Sprite) -> None:
        """

        Check if drill has reached an edge of the viewport.

        Parameters
        ----------
        centre_sprite: arcade.Sprite
            Center of the screen.

        """
        # Check if the drill has reached the edge of the box
        self._centre_sprite = centre_sprite
        changed = any((self._check_for_scroll_left(), self._check_for_scroll_right(),
                      self._check_for_scroll_up(), self._check_for_scroll_down()))

        self.left_offset = int(self.left_offset)
        self.bottom_offset = int(self.bottom_offset)

        if changed:
            arcade.set_viewport(self.left_offset, SCREEN_WIDTH + self.left_offset,
                                self.bottom_offset, SCREEN_HEIGHT + self.bottom_offset)

    def _check_for_scroll_left(self) -> bool:
        """

        Checks if left scroll is necessary.

        Returns
        -------
        boolean
            True: recenter

        """
        left_boundary = self.left_offset + VIEWPOINT_MARGIN
        if self._centre_sprite.left < left_boundary:
            self.left_offset -= left_boundary - self._centre_sprite.left
            return True
        return False

    def _check_for_scroll_right(self) -> bool:
        """

        Checks if right scroll is necessary.

        Returns
        -------
        boolean
            True: recenter

        """
        right_boundary = self.left_offset + SCREEN_WIDTH - VIEWPOINT_MARGIN
        if self._centre_sprite.right > right_boundary:
            self.left_offset += self._centre_sprite.right - right_boundary
            return True
        return False

    def _check_for_scroll_up(self) -> bool:
        """

        Checks if up scroll is necessary.

        Returns
        -------
        boolean
            True: recenter

        """
        top_boundary = self.bottom_offset + SCREEN_HEIGHT - VIEWPOINT_MARGIN
        if self._centre_sprite.top > top_boundary:
            self.bottom_offset += self._centre_sprite.top - top_boundary
            return True
        return False

    def _check_for_scroll_down(self) -> bool:
        """

        Checks if down scroll is necessary.

        Returns
        -------
        boolean
            True: recenter

        """
        bottom_boundary = self.bottom_offset + VIEWPOINT_MARGIN
        if self._centre_sprite.bottom < bottom_boundary:
            self.bottom_offset -= bottom_boundary - self._centre_sprite.bottom
            return True
        return False
