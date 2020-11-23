"""
What methods do these classes need to have?
1 - A way to load a quad tree from the map - should be done by dividing the map into 4s - honestly 16 by 16 might even be TOO BIG!!!! - But also depends on how we feed through collisions
2 - A way to navigate chunks based on relative location - trying to keep it nice.
"""


class QuadTree:

    def __init__(self, max_levels=3):
        self.max_levels = 3
        self.root = QuadTree()


    def _load_tree_from_map_config(self, map_layer_config):
        """
        Generates a tree based on the given map configuration
        Might only contain sprite lists in the bottom nodes for memory reasons.
        This is because I will only ever be returning the bottom level nodes
        """
        pass

    def return_active_nodes(self, drill_x, drill_y):
        """
        Parses the quadtree and returns the active chunks
        """
        pass

    def load_node_sprite_list(self):
        """
        Loads a sprite list for a single node
        """
        pass







class QuadNode:

    def __init__(self):
        self.children = {}
        self.x_range = None
        self.y_range = None
        self.sprite_list = None


