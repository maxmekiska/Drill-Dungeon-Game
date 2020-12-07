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

All map blocks are represented in a map layer matrix, which stores the type of block and its relative position. Block type is represented as a short string (for example, 'X' for dirt or ' ' for an air block). This map layer matrix is later loaded into a map layer configuration, which also stores the X and Y coordinates of the block, which is then loaded into the BlockGrid class, which manages the sprites displayed on the map.

In order to add additional block types, first a new string must be assigned to the block type. A method then needs to be added to add the string representing the new block to the map layer matrix. How exactly this is to be implemented depends on the nature of the block and is thus up to the maintainer. As an example, gold and coal blocks are generated in random patches in the methods generate_coal() and generate_gold() in the MapLayer class. However it is implemented, make sure the method to load the blocks into the map layer matrix is called in the get_full_map_layer_configuration() method, as this is what is called when loading in the map layer to the game.

Once the block type string is loaded into the map layer configuration, a new block type has to be defined. The block.py file contains all the block classes, which extend the main block class. Create a new block class following the format of the other ones, ensuring the char attribute is set to the same one that was loaded into the map layer matrix. File is the location of the image that the new block type will take as its sprite, while scale changed the size of the block. Make sure that the block will scale to 20x20 pixels. Finally, add the new block class to the _Block class at the end of the file, which allows for the block classes to be called.

Finally, the new block type needs to be added to the BlockGrid class in the block_grid.py file. The exact implementation of this depends on what the intended behaviour of the block is. If the block is purely for visual purposes and never needs to interact with the drill, then it is classified as an air block. To add the new block type as an air block, simply append BLOCK.$<$ NEWTYPE$>$ to the if statement on line 102. This checks if the block being iterated over is meant to be an air block, and initialises it as such.

If the block needs to interact with the drill, then an elif statement needs to be appended to the _add_block_to_list() method in block_grid.py file. Depending on if the block can be broken or not, it should be appended to the sprites' indestructible_block_list or the destructable_blocks_list. Either way, it should also be added to all_blocks_list.

If the block requires some sort of special interaction with the drill, it may require that a sprite list be appended to the SpriteContainer class. This list can then be called in other methods which will allow for just that type of block to be checked for collision or other interactions. To add this list, simply extend the constructor method of the SpriteContainer class in the sprite_container.py file, adding a new sprite list as an argument and class attribute.


## Adding Additional Prefabricated Dungeons


## Automated Dungeon Generation

Automated dungeon generation is more of an open ended addition, and can be implemented in several ways. In theory, the only thing requires is some way to alter the map layer matrix to add some floor and dungeon wall tiles, represented by characters 'F' and 'W' respectively.

Two methods were attempted for this iteration of the game, but were both shelved due to balancing difficulties. These can be re-added by the maintainer and improved if they so wish. The first method used the same basic principle of the generate_coal() and generate_gold() methods, instead adding floor blocks. Then, the map layer matrix should then be iterated over, adding wall blocks to any blocks adjacent to floors which are not also floor tiles.

The other method which was attempted was constructing new dungeons from several prefabricated rooms. This is similar to the prefabricated method, but more open ended.

## Adding Additional Explosion Effects

Adding additional tailored explosion effects are recommended to create when new blocks, enemies or other objects are added to the game. To do so, please navigate to DrillDungeonGame/particles/explosion.py file. The file begins by defining a list of constants that control how the explosion will be rendered onto the screen. These constants are universally used by all explosion classes. If for a particular explosions this behaviour is not wished, it is recommended to create a new constant and manually add it into the specific particle class. As an example, this specific tailoring approach is applied to the explosion particles colours. Each currently available block in the game has its own explosion particle colour list.
[Here](https://arcade.academy/arcade.color.html) you can see the full library provided colour list.

The general structure of the file consists of a general Smoke class and multiple individual particle classes. The smoke class can be used by each particle class to cause a smoke effect upon a particle explosion. A good example of a particle class using the smoke class is the ParticleCoal class. In the update() method of the ParticleCoal class, a smoke object is created which in turn generates the smoke effect:

``` python3
if random.random() <= SMOKE_CHANCE:
    smoke = Smoke(5)
    smoke.position = self.position
    self.my_list.append(smoke)
```

To generate a new particle explosion, follow the example of the other particle classes. If you wish to add the smoke effect, add into the newly created particle classes update() method the code block above.

## Main Menu Modifications

Modifying or adding new elements to the main menu is possible by navigating to the following python file: DrillDungeonGame/views.py. The general structure of this file consist first of button classes and second of view classes. First, button classes (inherent from arcade.gui.UIFlatButton) define the behaviour of what happens when a particular button is pressed. Second, View classes define (inherent from arcade.View) the general structure of the window and graphical representation. Each view class contains a setup() method that is used to place the buttons to the preferred location. It further, creates a button objects to add the preferred logic to the buttons placed onto the window.
