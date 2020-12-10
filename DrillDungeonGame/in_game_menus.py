import arcade

from .entity.mixins import ShotType
from .utility import SCREEN_WIDTH, SCREEN_HEIGHT


def draw_3d_rectangle(center_x, center_y, width, height, face_color,
                      highlight_color, shadow_color, shadow_thickness):
    """
    Draws a rectangle with shadow and thickness

    Parameters
    ----------
    center_x           :  int
        center x coordinate position of rectangle
    center_y           :  int
        center y coordinate position of rectangle
    width              :  int
        width of rectangle
    height             :  int
        height of rectangle
    face_color         :  arcade.color
        colour of rectangle face
    highlight_color    :  arcade.color
        highlight colour of rectangle face
    shadow_color       :  arcade.color
        shadow colour of rectangle face
    shadow_thickness   :  int
        thickness of rectangle
    """
    arcade.draw_rectangle_filled(center_x, center_y, width,
                                 height, face_color)
    # Bottom horizontal
    arcade.draw_line(center_x - width / 2, center_y - height / 2,
                     center_x + width / 2, center_y - height / 2,
                     shadow_color, shadow_thickness)
    # Right vertical
    arcade.draw_line(center_x + width / 2, center_y - height / 2,
                     center_x + width / 2, center_y + height / 2,
                     shadow_color, shadow_thickness)
    # Top horizontal
    arcade.draw_line(center_x - width / 2, center_y + height / 2,
                     center_x + width / 2, center_y + height / 2,
                     highlight_color, shadow_thickness)
    # Left vertical
    arcade.draw_line(center_x - width / 2, center_y - height / 2,
                     center_x - width / 2, center_y + height / 2,
                     highlight_color, shadow_thickness)


class MenuButton:
    """
    Creates grey button used for in game menus.

    Methods
    -------
    add_text(text, font_size)
        Adds text to be displayed on button
    add_image(image, scale=1, angle=0)
        Adds image to be displayed on button
    draw(active=True)
        Displays button and when active is false bisplays button
        that can't be used
    assign_action(function_to_run)
        Assigns the function to be called if button is pressed
    mouse_press(x, y)
        Checks if click is on button
    mouse_release(x, y)
        Checks if click release is on button
    """

    def __init__(self, center_x, center_y, width, height):
        """
        Parameters
        ----------
        center_x    :   int
            Center x position for the button
        center_y    :   int
            Center y position for the button
        width       :   int
            Width of button
        height      :   int
            Heigt of button
        """

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.face_color = arcade.color.LIGHT_GRAY
        self.highlight_color = arcade.color.WHITE
        self.shadow_color = arcade.color.GRAY
        self.shadow_thickness = 2
        self.pressed = False
        self.button_image = None
        self.button_image_scale = 1
        self.button_image_angle = 0
        self.image_x_offset = 0
        self.image_y_offset = 0

        self.action_function = None

        self.text = None
        self.font_size = 1
        self.text_x_offset = 0
        self.text_y_offset = 0

    def add_text(self, text, font_size, x_offset=0, y_offset=0):
        """
        Adds text to be displayed on button
        Either text or image can be displayed on button

        Parameters
        ----------
        text         :   str
            Text to be displayed
        font_size    :   int
            Font size of text
        """
        self.text = text
        self.font_size = font_size
        self.text_x_offset = x_offset
        self.text_y_offset = y_offset

    def add_image(self, image, scale=1, angle=0, x_offset=0, y_offset=0):
        """
        Adds image to be displayed on button
        Either text or image can be displayed on button

        Parameters
        ----------
        image    :   str
            directory of image
        scale    :   int
            scale of image
        angle    :   int
            angle of image
        """
        self.button_image = arcade.load_texture(image)
        self.button_image_scale = scale
        self.button_image_angle = angle
        self.image_x_offset = x_offset
        self.image_y_offset = y_offset

    def draw(self, active=True):
        """
        Displays button on screen

        Parameters
        ----------
        active   :  bool
            Shows the button as inactive when false
        """
        face_color = self.face_color
        if not active:
            self.pressed = True
            face_color = self.shadow_color
            color1 = self.shadow_color
            color2 = self.shadow_color
        elif not self.pressed:
            color1 = self.highlight_color
            color2 = self.shadow_color
        else:
            color1 = self.shadow_color
            color2 = self.highlight_color
        draw_3d_rectangle(self.center_x, self.center_y, self.width, self.height,
                          face_color, color1, color2, self.shadow_thickness)

        if self.button_image != None:
            if not self.pressed:
                self.button_image.draw_scaled(self.center_x+self.image_x_offset-self.shadow_thickness, self.center_y+self.image_y_offset+self.shadow_thickness, self.button_image_scale, self.button_image_angle)
            else:
                self.button_image.draw_scaled(self.center_x+self.image_x_offset, self.center_y+self.image_y_offset, self.button_image_scale, self.button_image_angle)

        if self.text != None:
            if not self.pressed:
                arcade.draw_text(self.text, self.center_x+self.text_x_offset-self.shadow_thickness,
                                 self.center_y+self.text_y_offset+self.shadow_thickness,
                                 arcade.color.BLACK, font_size=self.font_size,
                                 width=self.width, align="center",
                                 anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text(self.text, self.center_x+self.text_x_offset, self.center_y+self.text_y_offset,
                                 arcade.color.BLACK, font_size=self.font_size,
                                 width=self.width, align="center",
                                 anchor_x="center", anchor_y="center")

    def assign_action(self, function_to_run):
        """
        Assigns the function to run when button is pressed

        Parameters
        ----------
        function_to_run   :   function
            Assigns the function
        """
        self.action_function = function_to_run

    def mouse_press(self, x, y):
        """
        Checks if mouse click is on button

        Parameters
        ----------
        x   :   int
            x coordinate mouse input
        y   :   int
            y coordinate mouse input
        """
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return
        self.pressed = not self.pressed


    def mouse_release(self, x, y):
        """
        Checks if mouse click release is on button

        Parameters
        ----------
        x   :   int
            x coordinate mouse input
        y   :   int
            y coordinate mouse input
        """
        self.pressed = False
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return
        if self.action_function != None:
          self.action_function()


class MenuWindow:
  """
  Creates a blank grey window

  Methods
  -------
  draw
      displays window using draw_3d_rectangle to draw
  """

  def __init__(self, center_x, center_y, width, height):
      """
      Parameters
      ----------
      center_x    :   int
          Center x position for the window
      center_y    :   int
          Center y position for the window
      width       :   int
          Width of button
      height      :   int
          Heigt of button
      """
      self.center_x = center_x
      self.center_y = center_y
      self.width = width
      self.height = height
      self.face_color = arcade.color.LIGHT_GRAY
      self.highlight_color = arcade.color.WHITE
      self.shadow_color = arcade.color.GRAY
      self.shadow_thickness = 2

  def draw(self):
      draw_3d_rectangle(self.center_x, self.center_y, self.width, self.height,
                        self.face_color, self.highlight_color, self.shadow_color,
                        self.shadow_thickness)


class InGameMenu(arcade.View):
    """
    Creates a game view with a grey window in center of
    the screen and the previous screen faded in the background

    Methods
    -------
    on_draw()
        draws to screen
    on_key_press(key: int, modifiers: int)
        checks if esc key is pressed; to return to previous screen
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        checks if button is pressed
    on_mouse_release(x: float, y: float, button: int, modifiers: int)
        checks if button is pressed
    """
    def __init__(self, game_view, view, width, height):
        """
        Parameters
        ----------
        window      :   arcade.Window
            arcade window being used; used to get screen dimensions
        game_view   :   arcade.View
            Previous screen arcade.view; used to get and update data from game
            and to return to it after
        view        :   drill_dungeon_game/View
            used to get screen offsets to adjust x and y coordinates
        width       :   int
            width of in-game menu
        height      :   int
            height of in-game menu
        """
        super().__init__()
        self.game_view = game_view
        self.width = width
        self.height = height
        self.view = view
        self.screen_center_x = None
        self.screen_center_y = None
        self.button_list = []
        self.menu_window = None

    def on_show(self):
        self.screen_center_x = self.view.left_offset + SCREEN_WIDTH/2
        self.screen_center_y = self.view.bottom_offset + SCREEN_HEIGHT/2
        self.menu_window = MenuWindow(self.screen_center_x, self.screen_center_y, self.width, self.height)

        self.button_list=[]

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lrtb_rectangle_filled(self.view.left_offset, self.view.left_offset+self.window.width, self.view.bottom_offset+self.window.height, self.view.bottom_offset, arcade.color.GRAY + (100,))
        self.menu_window.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # return to previous view
            self.window.show_view(self.game_view)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for button in self.button_list:
            button.mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

    def on_mouse_release(self, x, y, button, key_modifiers):
        for button in self.button_list:
            button.mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)


class PauseMenu(InGameMenu):
    """
    Creates a pause menu game view

    Methods
    -------
    on_show()
        runs when view is loaded; creates buttons
    on_draw()
        draws to screen
    return_to_game()
        changes view back to game
    return_to_main()
        changes view back to main menu
    """
    def __init__(self, game_view, view):
        """
        Parameters
        ----------
        game_view   :   arcade.View
            Previous screen arcade.view; used to get and update data from game
            and to return to it after
        window      :   arcade.Window
            arcade window being used; used to get screen dimensions
        view        :   drill_dungeon_game/View
            used to get screen offsets to adjust x and y coordinates
        """
        self.game_view = game_view
        self.width = 300
        self.height = 300
        super().__init__(self.game_view, view, self.width, self.height)

    def on_show(self):
        super().on_show()
        resume_button = MenuButton(self.screen_center_x, self.screen_center_y+50, 200, 60)
        resume_button.add_text("Resume", 16)
        resume_button.assign_action(self.return_to_game)
        self.button_list.append(resume_button)

        main_menu_button = MenuButton(self.screen_center_x, self.screen_center_y-20, 200, 60)
        main_menu_button.add_text("Return to Main Menu", 16)
        main_menu_button.assign_action(self.return_to_main)
        self.button_list.append(main_menu_button)

        quit_button = MenuButton(self.screen_center_x, self.screen_center_y-90, 200, 60)
        quit_button.add_text("Exit Game", 16)
        quit_button.assign_action(self.quit_game)
        self.button_list.append(quit_button)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text("PAUSED", self.screen_center_x, self.screen_center_y+100, arcade.color.BLACK, font_size=20, anchor_x="center")

        for button in self.button_list:
          button.draw()

    def return_to_game(self):
        self.window.show_view(self.game_view)

    def return_to_main(self):
        self.window.show_view(self.window.menu_view)

    def quit_game(self):
        quit()

class ShopItem:
    """
    Creates an item to be displayed in the shop

    Methods
    -------
    setup_button(center_y)
        sets up button used to buy and show cost
    buy()
        deducts gold and performs function
    can_afford()
        checks if player can afford item
    draw(center_y)
        displays item block on menu
    """

    def __init__(self, shop_menu, center_x, item_name, cost, image, reusablility, button_function, function_inputs=None):
        """
        Parameters
        ----------
        shop_menu        :  ShopMenu
            shop menu view
        center_x         :  int
            center x position of item
        item_name        :  str
            Name of item
        cost             :  int
            Cost of item
        image            :  str
            image directory
        reusablility     :  bool
            allows user to purchase multiple times if true
        button_function  :  function
            function to execute if bought
        function_input   :  any
            input for function to execute if any
        """
        self.center_x = center_x
        self.item_name = item_name
        self.cost = cost
        self.item_image = arcade.load_texture(image)
        self.button_function = button_function
        self.function_inputs=function_inputs
        # self.gold_available = gold_available
        self.shop_menu = shop_menu
        self.buy_button = None
        self.reusable=reusablility
        self.available = True

    def setup_button(self, center_y):
        """
        Parameters
        ----------
        center_y        :  int
            center y position of item
        """
        self.buy_button = MenuButton(self.center_x+196, center_y, 55, 48)
        button_text = "Buy ("+str(self.cost)+")"
        self.buy_button.add_text(button_text, 10)
        self.buy_button.assign_action(self.buy)




    def buy(self):
        if (self.shop_menu.game_view.drill.inventory.gold >= self.cost) and self.available:
            if not self.reusable:
                self.available = False
            self.shop_menu.game_view.drill.inventory.gold -= self.cost
            if self.function_inputs != None:
                self.button_function(self.function_inputs)
            else:
                self.button_function()

    def can_afford(self):
        if self.shop_menu.game_view.drill.inventory.gold >= self.cost:
            return True
        else:
            return False


    def draw(self, center_y):
        draw_3d_rectangle(self.center_x, center_y, 450, 50, arcade.color.LIGHT_GRAY, arcade.color.WHITE, arcade.color.GRAY, 2)
        if self.can_afford() and self.available:
          self.buy_button.draw()
        else:
          self.buy_button.draw(False)

        self.item_image.draw_scaled(self.center_x-204, center_y, 0.6)
        arcade.draw_text(self.item_name, self.center_x-70, center_y,
                         arcade.color.BLACK, font_size=13,
                         width=200, align="left",
                         anchor_x="center", anchor_y="center")


class ShopTab:
    """
    Creates an tab of ShopItem items

    Methods
    -------
    add_item(item)
        add ShopItem to tab
    setup()
        setup tab
    draw()
        draw to screen
    check_mouse_press(x, y)
        check if mouse pressed for button in tab
    check_mouse_release(x, y)
        check if mouse released for button in tab
    """

    def __init__(self, tab_name, start_center_y):
        """
        Parameters
        ----------
        tab_name        :  str
            Name of tab
        start_center_y  :  int
            center y position of first item in tab; rest added sequentially
        """
        self.tab_name = tab_name
        self.item_list = []
        self.start_center_y = start_center_y
        self.button_list = []

    def add_item(self, item):
        self.item_list.append(item)

    def setup(self):
        for i in range(len(self.item_list)):
            self.item_list[i].setup_button(self.start_center_y-(55*i))
            self.button_list.append(self.item_list[i].buy_button)

    def draw(self):
        for i in range(len(self.item_list)):
            self.item_list[i].draw(self.start_center_y-(55*i))

    def check_mouse_press(self, x, y):
        for button in self.button_list:
            button.mouse_press(x, y)

    def check_mouse_release(self, x, y):
        for button in self.button_list:
            button.mouse_release(x, y)


class ShopMenu(InGameMenu):
    """
    Creates the shop menu view

    Methods
    -------
    add_ammo(amount)
        adds ammo
    upgrade_to_buckshot()
        buckshot upgrade
    upgrade_speed()
        upgrades vehicle speed
    on_show()
        runs when view loads
    change_to_left_tab()
        change to left shop tab
    change_to_right_tab()
        change to right shop tab
    return_to_game()
        return to game window
    on_draw()
        draws to screen
    on_update(delta_time)
        Method is called by the arcade library every iteration.
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        checks if button is pressed
    on_mouse_release(x: float, y: float, button: int, modifiers: int)
        checks if button is pressed
    """

    def __init__(self, game_view, view):
        """
        Parameters
        ----------
        game_view   :   arcade.View
            Previous screen arcade.view; used to get and update data from game
            and to return to it after
        window      :   arcade.Window
            arcade window being used; used to get screen dimensions
        view        :   drill_dungeon_game/View
            used to get screen offsets to adjust x and y coordinates
        """
        self.game_view = game_view
        self.width = 500
        self.height = 400
        super().__init__(self.game_view, view, self.width, self.height)

        self.tab_list = []
        self.tab_position = 0

        self.repair_button = None
        self.repair_cost = 1

    def add_ammo(self, amount):
        self.game_view.drill.inventory.ammunition += amount

    def upgrade_to_buckshot(self):
        self.game_view.drill.children[0].firing_mode = ShotType.BUCKSHOT

    def upgrade_speed(self):
        self.game_view.drill.speed = self.game_view.drill.speed*1.5

    def repair_drill(self):
        if self.game_view.drill.inventory.gold >= self.repair_cost:
            self.game_view.drill.inventory.gold -= self.repair_cost
            self.game_view.drill.current_health = self.game_view.drill.max_health

    def shield_upgrade(self):
        self.game_view.drill._shield_duration = 12.0

    def on_show(self):
        super().on_show()
        self.upgrades_tab = ShopTab("Upgrades", self.screen_center_y+40)
        self.ammo_tab = ShopTab("Ammo", self.screen_center_y+40)
        close_button = MenuButton(self.screen_center_x-230, self.screen_center_y+180, 28, 28)
        close_button.add_image("resources/images/gui/cross.png", 0.2, 180)
        close_button.assign_action(self.return_to_game)
        self.button_list.append(close_button)

        left_button = MenuButton(self.screen_center_x-209, self.screen_center_y+110, 28, 28)
        left_button.add_image("resources/images/gui/arrow.png", 0.2, 180)
        left_button.assign_action(self.change_to_left_tab)
        self.button_list.append(left_button)
        right_button = MenuButton(self.screen_center_x+209, self.screen_center_y+110, 28, 28)
        right_button.add_image("resources/images/gui/arrow.png", 0.2)
        right_button.assign_action(self.change_to_right_tab)
        self.button_list.append(right_button)

        self.repair_button = MenuButton(self.screen_center_x+180, self.screen_center_y+150, 90, 40)
        self.repair_button.add_image("resources/images/shop/repair.png", 0.4, 0, -20)
        self.repair_button.add_text("1", 15, 10)
        self.repair_button.assign_action(self.repair_drill)


        ammo_10 = ShopItem(self, self.screen_center_x, "Ammo (x10)", 1,
                          ":resources:images/space_shooter/laserBlue01.png", True, self.add_ammo, 10)
        ammo_20 = ShopItem(self, self.screen_center_x, "Ammo (x20)", 2,
                          ":resources:images/space_shooter/laserBlue01.png", True, self.add_ammo, 20)
        buckshot = ShopItem(self, self.screen_center_x, "Buckshot", 1,
                          "resources/images/shop/buckshot.png", False, self.upgrade_to_buckshot)
        speed1 = ShopItem(self, self.screen_center_x, "+50% Speed", 2,
                          "resources/images/shop/speed.png", False, self.upgrade_speed)
        light = ShopItem(self, self.screen_center_x, "Increase Visibility", 1,
                          "resources/images/shop/light.png", False, self.game_view.vignette.increase_vision)
        shield = ShopItem(self, self.screen_center_x, "Shield Level Up", 1,
                          "resources/images/shop/shield.png", False, self.shield_upgrade)
        self.upgrades_tab.add_item(buckshot)
        self.upgrades_tab.add_item(speed1)
        self.upgrades_tab.add_item(light)
        self.upgrades_tab.add_item(shield)
        self.ammo_tab.add_item(ammo_10)
        self.ammo_tab.add_item(ammo_20)

        self.tab_list.extend([self.upgrades_tab, self.ammo_tab])
        for tab in self.tab_list:
            tab.setup()

    def change_to_left_tab(self):
        if self.tab_position > 0:
            self.tab_position -= 1
        else:
            self.tab_position = len(self.tab_list)-1
    def change_to_right_tab(self):
        if self.tab_position < len(self.tab_list)-1:
            self.tab_position += 1
        else:
            self.tab_position = 0
    def return_to_game(self):
        self.window.show_view(self.game_view)

    def on_draw(self):
        super().on_draw()

        arcade.draw_text("Shop", self.screen_center_x, self.screen_center_y+160, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Gold: "+str(self.game_view.drill.inventory.gold), self.screen_center_x-210, self.screen_center_y+135, arcade.color.BLACK, font_size=16, anchor_x="center")

        arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y+110, 450, 30, arcade.color.GRAY)
        arcade.draw_text(self.tab_list[self.tab_position].tab_name, self.screen_center_x, self.screen_center_y+98, arcade.color.BLACK, font_size=18, anchor_x="center")

        for button in self.button_list:
            button.draw()

        if self.game_view.drill.current_health < self.game_view.drill.max_health:
            if self.self.game_view.drill.inventory.gold < self.repair_cost:
                self.repair_button.draw(False)
            else:
                self.repair_button.draw()


        self.tab_list[self.tab_position].draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for button in self.button_list:
            button.mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

        self.repair_button.mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

        self.tab_list[self.tab_position].check_mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

    def on_mouse_release(self, x, y, button, key_modifiers):
        for button in self.button_list:
            button.mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)

        self.repair_button.mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)

        self.tab_list[self.tab_position].check_mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)


class GameOverMenu(InGameMenu):
    """
    Creates a game over screen which displays score and options to go back
    to main menu or exit game

    Methods
    -------
    on_show()
        runs when view is loaded; creates buttons
    on_draw()
        draws to screen
    return_to_game()
        changes view back to game
    return_to_main()
        changes view back to main menu
    """
    def __init__(self, game_view, view):
        """
        Parameters
        ----------
        game_view   :   arcade.View
            Previous screen arcade.view; used to get and update data from game
            and to return to it after
        window      :   arcade.Window
            arcade window being used; used to get screen dimensions
        view        :   drill_dungeon_game/View
            used to get screen offsets to adjust x and y coordinates
        """
        self.game_view = game_view
        self.width = 500
        self.height = 200
        super().__init__(self.game_view, view, self.width, self.height)

    def on_show(self):
        super().on_show()
        main_menu_button = MenuButton(self.screen_center_x-110, self.screen_center_y-50, 200, 60)
        main_menu_button.add_text("Return to Main Menu", 16)
        main_menu_button.assign_action(self.return_to_main)
        self.button_list.append(main_menu_button)

        quit_button = MenuButton(self.screen_center_x+110, self.screen_center_y-50, 200, 60)
        quit_button.add_text("Exit Game", 16)
        quit_button.assign_action(self.quit_game)
        self.button_list.append(quit_button)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text("Game Over", self.screen_center_x, self.screen_center_y+40, arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Score:", self.screen_center_x-100, self.screen_center_y, arcade.color.BLACK, font_size=15, anchor_x="center")
        arcade.draw_text(str(self.game_view.score), self.screen_center_x, self.screen_center_y, arcade.color.BLACK, font_size=15, anchor_x="center")

        for button in self.button_list:
          button.draw()

    def return_to_main(self):
        self.window.show_view(self.window.menu_view)

    def quit_game(self):
        quit()
