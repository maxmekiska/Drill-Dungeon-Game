import math
from typing import Union, Tuple

import numpy as np
import random
from DrillDungeonGame.particles.explosion import PARTICLE_COUNT


def generate_next_layer_resource_patch_amount(current_layer, base_amount=20, minimum_patches=5):
    upper_bound = int(base_amount * np.exp(-current_layer / 10))
    lower_bound = int(base_amount * np.exp(-current_layer / 20))
    number_of_resource_patches = random.randint(upper_bound, lower_bound)
    if number_of_resource_patches < minimum_patches:
        number_of_resource_patches = minimum_patches
    return number_of_resource_patches


def generate_next_layer_dungeon_amount(current_layer, base_amount: int = 3, max_amount: int = 10,
                                       initial_max_factor: int = 6) -> int:
    upper_bound = int(max_amount - initial_max_factor * np.exp(-current_layer / 10))
    number_of_dungeons = random.randint(base_amount, upper_bound)
    return number_of_dungeons


def is_near(a_x: float, a_y: float, b_x: float, b_y: float, distance: Union[float, int]) -> bool:
    """Function used in pathfinding. Returns True if entity is in range of a certain point. Else False"""
    length = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2))
    return True if length < distance else False


def make_explosion_particles(particle, position: Tuple[float, float], time: float, sprites) -> None:
    for i in range(PARTICLE_COUNT):
        p = particle(sprites.explosion_list)
        p.position = position
        sprites.explosion_list.append(p)
