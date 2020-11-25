import math
from typing import Union, Tuple

import arcade
import numpy as np
import random
from DrillDungeonGame.particles.explosion import PARTICLE_COUNT
import PIL.Image
import PIL.ImageDraw

def generate_next_layer_resource_patch_amount(current_layer, base_amount=20, minimum_patches=5):
    """
    Determines resources placed in next level after drill drills down.

    Parameters:
    -----------
    current_layer   : int
        The layer on which the drill is currently located.
    base_amount     : int
        The base amount of resources that can be found.
    minimum_patches : int
        The minimum amount of resources that can be found.

    Returns:
    --------
    number_of_resource_patches: int
        Number of resources that can be found in the next layer.
    """
    upper_bound = int(base_amount * np.exp(-current_layer / 10))
    lower_bound = int(base_amount * np.exp(-current_layer / 20))
    number_of_resource_patches = random.randint(upper_bound, lower_bound)
    if number_of_resource_patches < minimum_patches:
        number_of_resource_patches = minimum_patches
    return number_of_resource_patches


def generate_next_layer_dungeon_amount(current_layer, base_amount: int = 3, max_amount: int = 10,
                                       initial_max_factor: int = 6) -> int:
    """
    Determines dungeons placed in next level after drill drills down.

    Parameters:
    -----------
    current_layer   : int
        The layer on which the drill is currently located.
    base_amount     : int
        The base amount of dungeons that can be explored.
    max_amount      : int
        The maximum amount of dungeons that can be explored.
    minimum_patches : int
        The minimum amount of dungeons that can be explored.

    Returns:
    --------
    number_of_dungeons: int
        Number of dungeons that can be explored.
    """
    upper_bound = int(max_amount - initial_max_factor * np.exp(-current_layer / 10))
    number_of_dungeons = random.randint(base_amount, upper_bound)
    return number_of_dungeons


def is_near(a_x: float, a_y: float, b_x: float, b_y: float, distance: Union[float, int]) -> bool:
    """
    Function used in pathfinding. Returns True if entity is in range of a certain point. Else False

    Parameters
    ----------
    a_x         : float
        x-coordinate of entity a.
    a_y         : float
        y-coordinate of entity b.
    b_x        : float
        x-coordinate of entity b.
    b_y
        y-coordinate of entity b.
    distance    : Union[float, int]
        The distance between a and b.

    Returns
    -------
    bool
        True if length < distance, else False.
    """
    length = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2))
    return True if length < distance else False


def make_explosion_particles(particle, position: Tuple[float, float], time: float, sprites) -> None:
    """
    Function that creates explosion particle effects.

    Parameters
    ----------
    particle
        Particles generated.
    position    : Tuple[float, float]
        Position of the center of the explosion.
    time        : float
        Time of explosion.
    sprites     : arcade.Sprite
        Sprites affected by the explosion.
    """
    for i in range(PARTICLE_COUNT):
        p = particle(sprites.explosion_list)
        p.position = position
        sprites.explosion_list.append(p)


def make_vignette(diameter: int, color: arcade.Color, vignette_radius, center_alpha: int = 255, outer_alpha: int = 255):
    """
    Returns an arcade.Texture object of the vignette texture produced.

    Notes
    -----
    This is an adaptation of arcade.make_soft_sircle_texture.
    https://arcade.academy/_modules/arcade/texture.html#make_soft_circle_texture
    In our implementation, we want the surrounding vignette to be filled, not empty.
    Otherwise we won't be blocking any
    vision for the drill to see.

    Parameters
    ----------
    diameter        : int
        The diameter of the whole image.
    color           : arcade.color
        The color for the vignette.
    vignette_radius : int
        The radius of the vignette. Must be less than or equal to the diameter // 2. Points in the image beyond this
        vignette_radius are filled with the color and alpha value specified in outer_alpha
    center_alpha    : int
        Alpha color for the circle at its center point. Linearly interpolated between this and the outer_alpha.
    outer_alpha     : int
        Alpha color for the circle at its outer point. Linearly interpolated between this and the inner_alpha.

    Returns
    -------
    arcade.Texture
        The texture with draw_scaled method.
    """
    max_radius = diameter // 2
    assert vignette_radius <= max_radius

    bg_colour = (0, 0, 0, 0)  # Make background transparent.
    image = PIL.Image.new("RGBA", (diameter, diameter), bg_colour)
    draw = PIL.ImageDraw.Draw(image)

    for point in range(max_radius, 0, -1):
        if point < vignette_radius:
            alpha = int(arcade.lerp(center_alpha, outer_alpha, point / vignette_radius))
            point_color = (color[0], color[1], color[2], alpha)
            draw.ellipse((max_radius - point, max_radius - point, max_radius + point -1, max_radius + point - 1),
                         fill=point_color)
        else:
            point_color = (color[0], color[1], color[2], outer_alpha)
            draw.rectangle((max_radius - point, max_radius - point, max_radius + point -1, max_radius + point - 1),
                           fill=point_color)

    name = f"vignette_circle_texture:{diameter}:{color}:{center_alpha}:{outer_alpha}"
    return arcade.Texture(name, image)


