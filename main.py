import arcade
from DrillDungeonGame.drill_dungeon_game import DrillDungeonGame


def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
