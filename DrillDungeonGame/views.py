import arcade
import arcade.gui
from arcade.gui import UIManager

from .utility import SCREEN_WIDTH, SCREEN_HEIGHT


class MyFlatButtonStartGame(arcade.gui.UIFlatButton):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
    """

    Class to create a flat button that starts the game.

    Methods
    -------
    on_click()
        Executes logic when button is clicked.

    """
    def on_click(self):
        """

        Changes View to game view (game window starts running).

        """
        self.window.menu_view.start_game()
        
        
class MyFlatButtonStartInstruction(arcade.gui.UIFlatButton):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
    """

    Class to create a flat button that leads to the instruction menu.

    Methods
    -------
    on_click()
        Executes logic when button is clicked.

    """
    def on_click(self):
        """

        Changes View to the instructions window.

        """
        self.window.show_view(self.window.instructions_view)


class MyFlatButtonMenu(arcade.gui.UIFlatButton):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
    """

    Class to create a flat button that leads to the main menu.

    Methods
    -------
    on_click()
        Executes logic when button is clicked.

    """
    def on_click(self):
        """

        Changes View to the main menu.

        """
        self.window.show_view(self.window.menu_view)


class MyFlatButtonObjectives(arcade.gui.UIFlatButton):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
    """

    Class to create a flat button that leads to the main menu.

    Methods
    -------
    on_click()
        Executes logic when button is clicked.

    """
    def on_click(self):
        """

        Changes View to the objectives window.

        """
        self.window.show_view(self.window.objectives_view)


class MyFlatButtonExit(arcade.gui.UIFlatButton):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window

    """

    Class to create a flat button that closes the game.

    Methods
    -------
    on_click()
        Executes logic when button is clicked.

    """
    def on_click(self):
        """

        Closes the game (ends the running program).

        """
        quit()


class MenuView(arcade.View):
    """

    Class that defines the layout and logics of the main menu.

    Methods
    -------
    on_draw()
        Renders the window.
    on_show()
        Displays the window.
    on_hide_view()
        Ui manager button logic initialization.
    start_game()
        Method that starts the game.
    setup()
        Defines the location of the buttons.

    """
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.ui_manager = UIManager()

    def on_draw(self):
        """

        Renders the window for the player.

        """
        arcade.start_render()
        arcade.draw_text("Drill Dungeon Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

    def on_show(self):
        """

        Displays the window, sets up background color.

        """
        self.setup()
        arcade.set_background_color(arcade.color.WHITE)
                         
    def on_hide_view(self):
        """

        Ui manager button logic initialization.

        """
        self.ui_manager.unregister_handlers()

    def start_game(self):
        """

        Method that changes the window to the game window and start the game.

        """
        self.window.show_view(self.window.game_view)

    def setup(self):
        """

        Set up this view.

        """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4

        button_left = MyFlatButtonExit(
            self.window,
            'Exit',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)

        button_right = MyFlatButtonStartInstruction(
            self.window,
            'Instructions',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)
        
        button_upper_right = MyFlatButtonStartGame(
            self.window,
            'Start Game',
            center_x=right_column_x,
            center_y=y_slot * 2,
            width=250,
        )
        self.ui_manager.add_ui_element(button_upper_right)

       
class InstructionView(arcade.View):
    """

    Class that defines the layout and logics of the instruction window.

    Methods
    -------
    on_draw()
        Renders the window.
    on_show()
        Displays the window.
    on_hide_view()
        Ui manager button logic initialization.
    setup()
        Defines the location of the buttons.

    """
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.ui_manager = UIManager()
        
    def on_show(self):
        """

        Displays the window, sets up background color.

        """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """

        Renders the window for the player.

        """
        arcade.start_render()
        arcade.draw_text("Instructions", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("1. Press W, A, S, D to move\n\n2. Click on screen to aim and shoot\n\n3. Press T to drill down\n\n4. Press B to change fire mode\n\n4. Press ESC to pause the game", 
                          SCREEN_WIDTH/SCREEN_WIDTH, SCREEN_HEIGHT/2.4,
                          arcade.color.WHITE, font_size= 25, anchor_x="left")
        
                         
    def on_hide_view(self):
        """

        Ui manager button logic initialization.

        """
        self.ui_manager.unregister_handlers()
     
    def setup(self):
        """

        Set up this view.

        """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4


        button_left = MyFlatButtonMenu(
            self.window,
            'Back',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)
      
        
        button_right = MyFlatButtonObjectives(
            self.window,
            'Next',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)
        
class ObjectivesView(arcade.View):
    """

    Class that defines the layout and logics of the objectives window.

    Methods
    -------
    on_draw()
        Renders the window.
    on_show()
        Displays the window.
    on_hide_view()
        Ui manager button logic initialization.
    setup()
        Defines the location of the buttons.

    """
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.ui_manager = UIManager()
        
    def on_show(self):
        """

        Displays the window, sets up background color.

        """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """

        Renders the window for the player.

        """
        arcade.start_render()
        arcade.draw_text("The Objective", SCREEN_WIDTH/2, SCREEN_HEIGHT/1.2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Text here", 
                          SCREEN_WIDTH/SCREEN_WIDTH, SCREEN_HEIGHT/2.4,
                          arcade.color.WHITE, font_size= 25, anchor_x="left")
        
                         
    def on_hide_view(self):
        """

        Ui manager button logic initialization.

        """
        self.ui_manager.unregister_handlers()
     
    def setup(self):
        """

        Set up this view.

        """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4


        button_left = MyFlatButtonStartInstruction(
            self.window,
            'Back',
            center_x=left_column_x,
            center_y=y_slot * 1,
            width=250,
        )
        self.ui_manager.add_ui_element(button_left)
      
        
        button_right = MyFlatButtonStartGame(
            self.window,
            'Start Game',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
          
        )
        self.ui_manager.add_ui_element(button_right)


 



