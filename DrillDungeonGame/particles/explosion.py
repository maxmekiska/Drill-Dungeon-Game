import random
import math
import arcade



# How fast to fade the particle
PARTICLE_FADE_RATE = 12

# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5

# How many particles per explosion
PARTICLE_COUNT = 20

# How big the particle
PARTICLE_RADIUS = 3

# Possible particle colors
PARTICLE_COLORS_DIRT = [arcade.color.GOLDEN_BROWN,
                        arcade.color.CHAMOISEE]
                   
PARTICLE_COLORS_COAL = [arcade.color.BLACK]

PARTICLE_COLORS_GOLD = [arcade.color.GOLD,
                        arcade.color.GOLDEN_POPPY,
                        arcade.color.LEMON,
                        arcade.color.MIKADO_YELLOW]

PARTICLE_COLORS_ENEMY = []  # for enemy hits

PARTICLE_SPARKLE_CHANCE = 0.02


SMOKE_START_SCALE = 0.25      
SMOKE_EXPANSION_RATE = 0.03    


SMOKE_FADE_RATE = 8   
SMOKE_RISE_RATE = 0.5     


SMOKE_CHANCE = 0.25  


class Smoke(arcade.SpriteCircle):
    """ Creation of smoke when block is hit, only used for coal blocks """
    def __init__(self, size) -> None:
        super().__init__(size, arcade.color.BLACK, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        if self.alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE
            
    def draw(self):
        for item in self.sprite_list:
            item.draw()


class ParticleDirt(arcade.SpriteCircle):
    """ Explosion particle for dirt blocks """
    def __init__(self, my_list):
        # Choose a random color
        color = random.choice(PARTICLE_COLORS_DIRT)

        # Make the particle
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture

        # Keep track of the list we are in, so we can add a smoke trail
        self.my_list = my_list

        # Set direction/speed
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255

        # What list do we add smoke particles to?
        self.my_list = my_list

    def update(self) -> None:
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y

    def draw(self) -> None:
        for item in self.sprite_list:
            item.draw()
            

class ParticleCoal(arcade.SpriteCircle):
    """ Explosion particle for coal blocks """
    def __init__(self, my_list):
        color = random.choice(PARTICLE_COLORS_COAL)
        super().__init__(PARTICLE_RADIUS, color)
     
        self.normal_texture = self.texture
        self.my_list = my_list
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed
        self.my_alpha = 255
        self.my_list = my_list

    def update(self) -> None:
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            

            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)
                
    def draw(self) -> None:
        for item in self.sprite_list:
            item.draw()


class ParticleGold(arcade.SpriteCircle):
    """ Explosion particle for gold blocks """
    def __init__(self, my_list) -> None:
        color = random.choice(PARTICLE_COLORS_GOLD)
        super().__init__(PARTICLE_RADIUS, color)
        self.normal_texture = self.texture
        self.my_list = my_list
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed
        self.my_alpha = 255
        self.my_list = my_list

    def update(self) -> None:
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
        

            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width), arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

    def draw(self) -> None:
        for item in self.sprite_list:
            item.draw()
