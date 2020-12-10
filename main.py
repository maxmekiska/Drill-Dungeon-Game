from DrillDungeonGame import *


def main() -> None:
    """

    Main function to execute and start the game.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(window.menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
