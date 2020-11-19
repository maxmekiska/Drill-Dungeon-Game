import arcade

from DrillDungeonGame.drill_dungeon_game import DrillDungeonGame

import arcade.gui
from arcade.gui import UIManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_TITLE = "Welcome to the Drill Dungeon"

window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)




class MyFlatButtonStartGame(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        MenuView.start_game()
        
        
class MyFlatButtonStartInstruction(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        instructions_view = InstructionView()
        window.show_view(instructions_view)
        
class MyFlatButtonMenu(arcade.gui.UIFlatButton):
    """
    
    """
    def on_click(self):
        menu_view = MenuView()
        window.show_view(menu_view)
class MyFlatButtonObjectives(arcade.gui.UIFlatButton):
    """
    
    """
    def on_click(self):
        objectives_view = ObjectivesView()
        window.show_view(objectives_view)
        
class MyFlatButtonExit(arcade.gui.UIFlatButton):
    """
    To capture a button click, subclass the button and override on_click.
    """
    def on_click(self):
        quit()
        
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Drill Dungeon Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.WHITE)
                         
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
        
          
    def start_game():
        game=DrillDungeonGame(window)
        game.setup()
        window.show_view(game)

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4


        button_left = MyFlatButtonExit(
            'Exit',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)
      
        
        button_right = MyFlatButtonStartInstruction(
            'Instructions',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)
        
        button_upper_right = MyFlatButtonStartGame(
            'Start Game',
            center_x=right_column_x,
            center_y=y_slot * 2,
            width=250,
        )
        self.ui_manager.add_ui_element(button_upper_right)

       
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        
    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("1. Press W, A, S, D to move\n\n2. Click on screen to aim and shoot\n\n3. Press T to drill down\n\n4. Press B to change fire mode\n\n4. Press ESC to pause the game", 
                          SCREEN_WIDTH/SCREEN_WIDTH, SCREEN_HEIGHT/2.4,
                          arcade.color.WHITE, font_size= 25, anchor_x="left")
        
                         
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
     
    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4


        button_left = MyFlatButtonMenu(
            'Back',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)
      
        
        button_right = MyFlatButtonObjectives(
            'Next',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)
        
class ObjectivesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        
    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("The Objective", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Text here", 
                          SCREEN_WIDTH/SCREEN_WIDTH, SCREEN_HEIGHT/2.4,
                          arcade.color.WHITE, font_size= 25, anchor_x="left")
        
                         
    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
     
    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4


        button_left = MyFlatButtonStartInstruction(
            'Back',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)
      
        
        button_right = MyFlatButtonStartGame(
            'Start Game',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)


 



