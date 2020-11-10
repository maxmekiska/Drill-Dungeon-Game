# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:12:48 2020

"""
from DrillDungeonGame.drill_dungeon_game import DrillDungeonGame
import arcade


def main():
    window = DrillDungeonGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
