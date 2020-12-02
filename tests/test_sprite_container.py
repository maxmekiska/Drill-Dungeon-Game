import pytest

from DrillDungeonGame.sprite_container import *
#TODO need to fix this test, it is not really useful at the moment


def test_extend():
    container1 = SpriteContainer(Drill(10, 10), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                 arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), drill_down_list = arcade.SpriteList(arcade.Sprite()))
    print(len(container1.border_wall_list))
    container2 = SpriteContainer(Drill(10, 10), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(),
                                 arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), arcade.SpriteList(), drill_down_list = arcade.SpriteList(arcade.Sprite()))
    container1.extend(container2)
    assert len(container1.drill_down_list) == 0 
