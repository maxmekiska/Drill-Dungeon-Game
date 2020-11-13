import math
from typing import Union

import numpy as np
import random

def generate_next_layer_resource_patch_amount(current_layer, base_amount=20, minimum_patches=5):
    upper_bound = int(base_amount * np.exp(-current_layer / 10))
    lower_bound = int(base_amount * np.exp(-current_layer / 20))
    number_of_resource_patches = random.randint(upper_bound, lower_bound)
    if number_of_resource_patches < minimum_patches:
        number_of_resource_patches = minimum_patches
    return number_of_resource_patches


def generate_next_layer_dungeon_amount(current_layer, base_amount=3, max_amount=10, initial_max_factor=6):
    upper_bound = int(max_amount - initial_max_factor * np.exp(-current_layer / 10))
    number_of_dungeons = random.randint(base_amount, upper_bound)
    return number_of_dungeons


def is_near(a_x: float, a_y: float, b_x: float, b_y: float, distance: Union[float, int]):
    """Function used in pathfinding. Returns True if entity is in range of a certain point. Else False"""
    length = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2))
    return True if length < distance else False
