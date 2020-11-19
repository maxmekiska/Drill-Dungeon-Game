import arcade
from DrillDungeonGame.drill_dungeon_game import DrillDungeonGame
from DrillDungeonGame.views import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 2400
MAP_HEIGHT = 2400
SCREEN_TITLE = "Welcome to the Drill Dungeon"

def main() -> None:
   # window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    main_view = MenuView()


    #game_view = DrillDungeonGame(window)

    #game_view.setup()
    #window.show_view(game_view)
    window.show_view(main_view)

    arcade.run()


if __name__ == "__main__":
    main()
