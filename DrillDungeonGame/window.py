from .drill_dungeon_game import DrillDungeonGame
from .in_game_menus import PauseMenu
from .views import MenuView, InstructionView, ObjectivesView
import arcade




class Window(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_view = DrillDungeonGame(self)
        self.menu_view = MenuView(self)
        self.instructions_view = InstructionView(self)
        self.objectives_view = ObjectivesView(self)

        self.pause_view = PauseMenu(self.game_view, self, self.game_view.view)
