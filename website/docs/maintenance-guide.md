<style>
	div {
		text-align: justify;
		text-justify: inter-word;
		font-family: "Times New Roman";			
	}

	object {
		display: block;
		margin: 0 auto;
	}

  a[title="centre"] {
  display: block;
  width: 100%;
  text-align: center;
}

</style>


# Maintenance Guide

## Overview

Drill Dungeon is made up of three major components: blocks, entities and menus. Blocks are the sprites that make up the map, and many of them interact in similar ways with the player. Entities consists of the player itself and any enemies that the player encounters. Menus include the start game menu and the shop menu.

## Map generation

All files pertaining to map generation are contained in the map directory. The visual map seen on screen when the game starts is generated in several stages. First, the configuration of the blocks (their types, where they are located) is generated in the dungeon_generator.py file. Next, blocks adjacent to air blocks are loaded into a container for all active sprites on the map, held in the block_map.py file. Finally, these blocks are rendered on the screen in the level.py file, which handles the visualisation of the map.

The dungeon_generator.py file contains the MapLayer class, which generates randomised levels for the drill when the game is loaded or the player drills down. This is initially done through the creation of a map layer matrix: a matrix of all the block types and their position relative to one another, in a grid. First, the map layer matrix is created and completely filled with dirt blocks. The width and height of the map layer matrix (in blocks) is determined by the constructor method of the MapLayer class, with default values of 128 for each. From this base template, different components of the map are added to the matrix by different methods.

Features that are generated in clumps randomly throughout the map (coal, gold, drillable zones and cave dungeons) are generated through their respective methods (with names of the form generate_gold()). This is done by selecting a random block in the matrix and changing that to the desired type. A randomised patch size is also created using a Poisson distribution. Then, a random walk direction is taken from update_dungeon_coords() and get_walk_direction(), which assign it a random block adjacent to the current block and changes that to the desired type too. This step is repeated until a patch of the desired size has been generated.

After this is complete, border walls are added. The first and last rows of the matrix are converted from all dirt to all undrillable walls, followed by the first and last blocks of each row in between. Finally, the map's prefabricated dungeon is loaded it using the generate_advanced_dungeons() method, which loads in row-by-row one of the prefabricated dungeons. With the map layer matrix generated, a final step creates a map layer configuration, which is identical to the matrix except each component is a tuple containing the block type and its X and Y coordinates.

The map layer configuration is converted into sprites and manages through the BlockGrid class in the block_grid.py file. This class takes the layer and loads all blocks that are adjacent to air blocks, so the majority of blocks are not rendered at any time. The configuration generated in the MapLayer class is used to load all the initial block sprites required, and manages the deletion and rendering of new blocks. New blocks are rendered using the break_block() method, which loads in any blocks adjacent to it that were not already rendered in the map layer configuration using the initialise_blocks_adjacent_to_air() method.

Blocks loaded from BlockGrid are stored in an instance of the SpriteContainer method, contained in the sprite_container.py file. This class is purely a wrapper for the many types of blocks that are used in the game. The class contains lists for groups of blocks that need to behave differently, as the arcade package used in creating Drill Dungeon requires sprite lists for collision detection. Each level is thus ultimately represented by a SpriteContainer, which is used in the levels.py file to generate the map.

## Running Unit Tests

## Debugging Features

## Extending the Code

## Adding Additional Block Types
