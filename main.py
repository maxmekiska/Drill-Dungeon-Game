import arcade

from DrillDungeonGame.views import window, MenuView


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
   # window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    main_view = MenuView()


    #game_view = DrillDungeonGame(window)

    #game_view.setup()
    #window.show_view(game_view)
    window.show_view(main_view)

    arcade.run()


if __name__ == "__main__":
    main()
