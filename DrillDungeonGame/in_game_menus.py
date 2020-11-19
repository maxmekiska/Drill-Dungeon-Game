import arcade
from DrillDungeonGame.entity.mixins.shooting_mixin import ShootingMixin, ShotType

def draw_3d_rectangle(center_x, center_y, width, height, face_color,
                      highlight_color, shadow_color, shadow_thickness):
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
    """docstring for MenuWindow."""

    def __init__(self, center_x, center_y, width, height):
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
        self.action_function = None

        self.text = None
        self.font_size = 1

    def add_text(self, text, font_size):
        self.text = text
        self.font_size = font_size

    def add_image(self, image, scale=1, angle=0):
        self.button_image = arcade.load_texture(image)
        self.button_image_scale = scale
        self.button_image_angle = angle


    def draw(self, active=True):
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
                self.button_image.draw_scaled(self.center_x-self.shadow_thickness, self.center_y+self.shadow_thickness, self.button_image_scale, self.button_image_angle)
            else:
                self.button_image.draw_scaled(self.center_x, self.center_y, self.button_image_scale, self.button_image_angle)

        if self.text != None:
            if not self.pressed:
                arcade.draw_text(self.text, self.center_x-self.shadow_thickness, self.center_y+self.shadow_thickness,
                                 arcade.color.BLACK, font_size=self.font_size,
                                 width=self.width, align="center",
                                 anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text(self.text, self.center_x, self.center_y,
                                 arcade.color.BLACK, font_size=self.font_size,
                                 width=self.width, align="center",
                                 anchor_x="center", anchor_y="center")

    def assign_action(self, function_to_run):
        self.action_function = function_to_run

    def mouse_press(self, x, y):
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
  """docstring for MenuWindow."""

  def __init__(self, center_x, center_y, width, height):
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
    """"""

    def __init__(self, window, game_view, view, width, height, color=arcade.color.GRAY):
        super().__init__()
        self.window_width = window
        self.game_view = game_view
        self.width = width
        self.height = height
        self.color = color
        self.view = view
        self.screen_center_x = self.view.left_offset + self.window.width/2
        self.screen_center_y = self.view.bottom_offset + self.window.height/2
        self.button_list = []



    def on_draw(self):

        self.game_view.on_draw()

        arcade.draw_lrtb_rectangle_filled(self.view.left_offset, self.view.left_offset+self.window.width, self.view.bottom_offset+self.window.height, self.view.bottom_offset, arcade.color.GRAY + (100,))
        menu_window = MenuWindow(self.screen_center_x, self.screen_center_y, self.width, self.height)
        menu_window.draw()


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for button in self.button_list:
            button.mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

    def on_mouse_release(self, x, y, button, key_modifiers):
        for button in self.button_list:
            button.mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)


class PauseMenu(InGameMenu):
    """docstring for PauseMenu."""

    def __init__(self, game_view, window, view):
        self.game_view = game_view
        self.width = 300
        self.height = 400
        super().__init__(window, self.game_view, view, self.width, self.height)

    def on_show(self):
        resume_button = MenuButton(self.screen_center_x, self.screen_center_y+110, 200, 60)
        resume_button.add_text("Resume", 16)
        resume_button.assign_action(self.return_to_game)
        self.button_list.append(resume_button)

        main_menu_button = MenuButton(self.screen_center_x, self.screen_center_y+40, 200, 60)
        main_menu_button.add_text("Return to Main Menu", 16)
        main_menu_button.assign_action(self.return_to_main)
        self.button_list.append(main_menu_button)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text("PAUSED", self.screen_center_x, self.screen_center_y+160, arcade.color.BLACK, font_size=20, anchor_x="center")

        for button in self.button_list:
          button.draw()

    def return_to_game(self):
        self.window.show_view(self.game_view)

    def return_to_main(self):
        main_view = MenuView()
        window.show_view(main_view)



class ShopItem:
    """docstring for ShopItem."""

    def __init__(self, shop_menu, center_x, item_name, cost, image, reusablility, button_function, function_inputs=None):
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
        self.buy_button = MenuButton(self.center_x+196, center_y, 55, 48)
        button_text = "Buy ("+str(self.cost)+")"
        self.buy_button.add_text(button_text, 10)
        self.buy_button.assign_action(self.buy)




    def buy(self):
        if (self.shop_menu.gold >= self.cost) and self.available:
            if not self.reusable:
                self.available = False
            self.shop_menu.gold -= self.cost
            if self.function_inputs != None:
                self.button_function(self.function_inputs)
            else:
                self.button_function()

    def can_afford(self):
        if self.shop_menu.gold >= self.cost:
            return True
        else:
            return False


    def draw(self, center_y):
        draw_3d_rectangle(self.center_x, center_y, 450, 50, arcade.color.LIGHT_GRAY, arcade.color.WHITE, arcade.color.GRAY, 2)
        if self.can_afford() and self.available:
          self.buy_button.draw()
        else:
          self.buy_button.draw(False)

        self.item_image.draw_scaled(self.center_x-204, center_y, 0.6,90)
        arcade.draw_text(self.item_name, self.center_x-130, center_y,
                         arcade.color.BLACK, font_size=13,
                         width=100, align="center",
                         anchor_x="center", anchor_y="center")


class ShopTab:
    """docstring for ShopTab."""

    def __init__(self, tab_name, start_center_y):
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
    """docstring for ShopMenu."""

    def __init__(self, game_view, window, view):
        self.game_view = game_view
        self.width = 500
        self.height = 400
        super().__init__(window, self.game_view, view, self.width, self.height)
        self.gold = game_view.sprites.drill.inventory.gold

        self.upgrades_tab = ShopTab("Upgrades", self.screen_center_y+40)
        self.ammo_tab = ShopTab("Ammo", self.screen_center_y+40)
        self.tab_list = []
        self.tab_position = 0

    def add_ammo(self, amount):
        self.game_view.sprites.drill.inventory.ammunition += amount

    def upgrade_to_buckshot(self):
        self.game_view.firing_mode = ShotType.BUCKSHOT

    def upgrade_speed(self):
        self.game_view.sprites.drill.speed = self.game_view.sprites.drill.speed*1.5

    def on_show(self):
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

        ammo_10 = ShopItem(self, self.screen_center_x, "Ammo (x10)", 1,
                          ":resources:images/space_shooter/laserBlue01.png", True, self.add_ammo, 10)
        ammo_20 = ShopItem(self, self.screen_center_x, "Ammo (x20)", 2,
                          ":resources:images/space_shooter/laserBlue01.png", True, self.add_ammo, 20)
        buckshot = ShopItem(self, self.screen_center_x, "Buckshot", 1,
                          "resources/images/shop/buckshot.png", False, self.upgrade_to_buckshot)
        speed1 = ShopItem(self, self.screen_center_x, "+50% Speed", 2,
                          "resources/images/shop/speed.png", False, self.upgrade_speed)
        self.upgrades_tab.add_item(buckshot)
        self.upgrades_tab.add_item(speed1)
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
        arcade.draw_text("Gold: "+str(self.gold), self.screen_center_x-210, self.screen_center_y+135, arcade.color.BLACK, font_size=16, anchor_x="center")

        arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y+110, 450, 30, arcade.color.GRAY)
        arcade.draw_text(self.tab_list[self.tab_position].tab_name, self.screen_center_x, self.screen_center_y+98, arcade.color.BLACK, font_size=18, anchor_x="center")

        for button in self.button_list:
          button.draw()

        self.tab_list[self.tab_position].draw()

    def on_update(self, delta_time):
        self.game_view.sprites.drill.inventory.gold = self.gold

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for button in self.button_list:
            button.mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

        self.tab_list[self.tab_position].check_mouse_press(x+self.view.left_offset, y+self.view.bottom_offset)

    def on_mouse_release(self, x, y, button, key_modifiers):
        for button in self.button_list:
            button.mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)

        self.tab_list[self.tab_position].check_mouse_release(x+self.view.left_offset, y+self.view.bottom_offset)
