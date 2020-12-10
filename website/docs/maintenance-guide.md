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


## Entities

The entity subdirectory, contained within the DrillDungeonGame package contains all classes responsible for creating, containing and moving sprites with logic. Currently, this includes the Drill class, as well as all enemies and bullets. In the future this should also contain friendly AI. All entities inherit from the base class: Entity, or through the ChildEntity class which extends Entity. Examples of when the ChildEntity class should be over Entity is if it forms any moving part for that base entity such as a turret, hand, or bullet. This is essential for bullets so that they do not collide with the entity that fired the bullet as it launches from the barrel.

To implement the simplest Entity possible, all you should need to do is sub-class Entity and pass several parameters to the super function, namely a string containing a path to the sprite, the scale of that sprite as well as an x and y coordinate. The only step left to have this entity drawn to the screen is to call the update() function followed by the draw() function on that entity in each game loop iteration. Both of these functions also recursively update or draw all entity’s that are children to parent that it is called upon. This is made possible through the get_all_children() function, and the opposite is possible by calling get_all_parents() on any given ChildEntity.

The current entity package structure allows for additional logic to be abstracted into mix-in classes, reducing the need for repeated code in different enemies that require identical logic. Some Mixin classes require direct instantiation within the entity’s \__init__() function, while others simply require inheriting to gain access to additional functions. Should the mix-in require instantiation, this can be possible by calling MixinName.\__init__(self, *args, **kwargs). By passing the self-parameter to the mix-in, the mix-in can also access any attributes and functions in the entity class such as health, speed, inventory and so on. Similar to how all children entities are updated when calling the parent.update() function, this also calls the update() function in all mix-ins of every child to the entity it is called upon. This makes using these mix-in classes very low effort and means more time can be spent on developing new features for them. Current functionality which has seen this abstraction to mix-in classes include a PathFindingMixin, DiggingMixin, ShootingMixin and ControllableMixin.

Firstly, the path finding mix-in provides functionality to calculate a path to another given entity or specific position and maintain that path until it is complete or otherwise cancelled. This is done through a path_to_position() function which takes an x and y coordinate as an argument as well as a SpriteList of blockling sprites and a boolean denoting whether diagonal movement is permitted. This function is also wrapped in a path_to_entity() function, which takes another Entity object as a parameter instead of an x, y coordinate and extracts its position. Both functions update an attribute called ‘path’ that contains a list of coordinates to denoting the path to the coordinate requested to path-find to. Each time the mix-in is then updated, it checks to see if this list is populated and if so, pops the first item from the list and calls the move_towards() function, which updates the velocity of the entity to that position.

Next, the digging mix-in allows the entity to break certain blocks which it collides with. This is generally restricted to dirt and ores. The controllable mix-in allows the entity to listen and react to keyboard or mouse presses. Abstracting this movement logic from outside the Drill class provides the foundation required to implement controllable bullets or other controllable friendlies. This mix-in does not require instantiation and simply functions by calling the update method every game loop.

Lastly, the shooting mix-in can be inherited to allow that entity to shoot a projectile. This is made possible with very few functions, namely an aim() function to aim at a given x, y coordinate, as well as a pull_trigger() and release_trigger() function to fire at the position aimed at. The shoot() function can also be used to instantly fire a bullet, but note that this bypasses fire rate limit.

## Running Unit Tests

By running the following command:

#### Windows
```console
python -m unittest discover tests
```

#### Linux, macOS
```console
py -m unittest discover tests
```

Unit test can be run. All unit tests are contained in the tests directory in the top level directory.

## Debugging Features

To make it easier for everyone working on the code, debugging features are added. These features can be activated in-game by pressing specific keys. The debugging features can be found at the following location in the source code: DrillDungeonGame/drill_dungeon_game.py.

```python3
  #DEBUGGING CONTROLS
  elif self.keys_pressed['O']:
      self.vignette.increase_vision()

  elif self.keys_pressed['L']:
      self.vignette.decrease_vision()

  elif self.keys_pressed['K']:
      self.vignette.blind()

  elif self.keys_pressed['SEMICOLON']:
      self.vignette.far_sight()

  elif self.keys_pressed['M']:
      self.window.show_view(self.window.shop_view)
```

## Extending the Code

## Adding Additional Block Types

All map blocks are represented in a map layer matrix, which stores the type of block and its relative position. Block type is represented as a short string (for example, 'X' for dirt or ' ' for an air block). This map layer matrix is later loaded into a map layer configuration, which also stores the X and Y coordinates of the block, which is then loaded into the BlockGrid class, which manages the sprites displayed on the map.

In order to add additional block types, first a new string must be assigned to the block type. A method then needs to be added to add the string representing the new block to the map layer matrix. How exactly this is to be implemented depends on the nature of the block and is thus up to the maintainer. As an example, gold and coal blocks are generated in random patches in the methods generate_coal() and generate_gold() in the MapLayer class. However it is implemented, make sure the method to load the blocks into the map layer matrix is called in the get_full_map_layer_configuration() method, as this is what is called when loading in the map layer to the game.

Once the block type string is loaded into the map layer configuration, a new block type has to be defined. The block.py file contains all the block classes, which extend the main block class. Create a new block class following the format of the other ones, ensuring the char attribute is set to the same one that was loaded into the map layer matrix. File is the location of the image that the new block type will take as its sprite, while scale changed the size of the block. Make sure that the block will scale to 20x20 pixels. Finally, add the new block class to the _Block class at the end of the file, which allows for the block classes to be called.

The new block type then needs to be added to the BlockGrid class in the block\textunderscore grid.py file. The exact implementation of this depends on what the intended behaviour of the block is. If the block is purely for visual purposes and never needs to interact with the drill, then it is classified as an air block. To add the new block type as an air block, simply append BLOCK.$<$NEWTYPE$>$ to the if statement to the following for loop on line 102:

```python3
def initialise_blocks_adjacent_to_air(self, sprites):
		for x in range(self.width):
				for y in range(self.height):
						block = self.blocks[x][y]
						if any(type(adjacent_block) in (BLOCK.AIR, BLOCK.DRILLDOWN,
																				BLOCK.FLOOR) for adjacent_block in
																				self._get_adjacent_blocks_to(block)):
								if type(block) in (BLOCK.FLOOR, BLOCK.AIR):
										self.air_blocks.append(block)
								elif type(block) == BLOCK.DRILLDOWN:
										self.air_blocks.append(block)
										if block not in sprites.all_blocks_list:
												self._add_block_to_lists(block, sprites)
								else:
										if block not in sprites.all_blocks_list:
												self._add_block_to_lists(block, sprites)

```

This checks if the block being iterated over is meant to be an air block, and initialises it as such.

If the block needs to interact with the drill, then an elif statement needs to be appended to the _add_block_to_list() method in block_grid.py file:
```python3
def _add_block_to_lists(self, block: Block, sprites) -> None:
    if type(block) == BLOCK.DIRT:
        sprites.destructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)

    elif type(block) == BLOCK.COAL:
        sprites.destructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)

    elif type(block) == BLOCK.GOLD:
        sprites.destructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)

    elif type(block) == BLOCK.SHOP:
        sprites.shop_list.append(block)
        sprites.indestructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)

    elif type(block) == BLOCK.BORDER:
        sprites.indestructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)
        sprites.border_wall_list.append(block)

    elif type(block) == BLOCK.WALL:
        sprites.indestructible_blocks_list.append(block)
        sprites.all_blocks_list.append(block)
        sprites.border_wall_list.append(block)

    elif type(block) == BLOCK.DRILLDOWN:
        sprites.drill_down_list.append(block)
        sprites.all_blocks_list.append(block)

    else:
        raise ValueError(f'Incorrect block type: {type(block)}!')
```
Depending on if the block can be broken or not, it should be appended to the sprites' indestructible_block_list or the destructable_blocks_list. Either way, it should also be added to all_blocks_list.

If the block requires some sort of special interaction with the drill, it may require that a sprite list be appended to the SpriteContainer class. This list can then be called in other methods which will allow just that type of block to be checked for collision or other interactions. To add this list, simply extend the constructor method of the SpriteContainer class in the sprite_container.py file, adding a new sprite list as an argument and class attribute.


## Additional Prefabricated Dungeons

To add additional prefabricated dungeons please navigate to DrillDungeonGame/map/prefab_dungeon_rooms.py. Any dungeon added into this file will later on be displayed in the exact same format as defined here. Prefabricated dungeons are entered via a simple array:


```python3
entrance_room_one =  [['W', 'W', 'W', 'W', 'F', 'F', 'W', 'W', 'W','W', 'W','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F','F', 'F','W'],
['W', 'W', 'W', 'W', 'F', 'F', 'W', 'W', 'W','W', 'W', 'W']]
```

In more detail, the letters in the matrix above stand each for a specific tile in the game. 'W' represents a wall and will be displayed as an indestructible wall when rendered in the game. The other letter, 'F', represents a simple floor tile which matches the style of the indestructible wall tiles.

``` python3
wing_room_one =  [['F', 'W', 'W', 'W', 'W', 'W', 'F'] ,
['LW', 'F', 'F', 'F', 'F', 'F',  'RW'] ,
['LW', 'F', 'F', 'F', 'F', 'F',  'RW'] ,
['LW', 'F', 'F', 'G', 'G', 'F',  'RW'] ,
['LW', 'F', 'F', 'G', 'G', 'F',  'RW'] ,
['LW', 'F', 'F', 'F', 'F', 'F',  'RW'] ,
['LW', 'F', 'F', 'F', 'F', 'C',  'RW'] ,
['LW', 'F', 'F', 'F', 'C', 'C',  'RW'] ,
['LW', 'W', 'W', 'W', 'W', 'W', 'RW']]
```

Other available options can be seen in the above wing room example. In fact, LW and RW represent left walls and right walls which are a specific design version of a normal wall. Other elements can be added such as gold blocks or coal blocks ('G', 'C').

## Automated Dungeon Generation

Automated dungeon generation is more of an open ended addition, and can be implemented in several ways. In theory, the only thing requires is some way to alter the map layer matrix to add some floor and dungeon wall tiles, represented by characters 'F' and 'W' respectively.

Two methods were attempted for this iteration of the game, but were both shelved due to balancing difficulties. These can be re-added by the maintainer and improved if they so wish. The first method used the same basic principle of the generate\_coal() and generate\_gold() methods, instead adding floor blocks. Then, the map layer matrix should then be iterated over, adding wall blocks to any blocks adjacent to floors which are not also floor tiles.

The other method which was attempted was constructing new dungeons from several prefabricated rooms. This is similar to the prefabricated method, but more open ended.



## Extending the Entity class
The entity class may be extended to include extra features such as animations. There are 2 main default animations you can add to the entity which are the idle animations and moving animations. The idle animation loop when the character is not moving while the moving animations loop when character is in motion. To add any of these include a list of the images to loop through in the subclass initialisation. This list should then be passed when initialising the parent class Entity. The idle images should be passed as idle\_textures and the moving images should be passed as moving\_textures. Lastly a time value would also need to be passed to the Entity initialisation as \time\_between\_animation\_texture\_updates. This determines the time it takes before switching the pictures.

More animations may be added but this would require overriding the update\_animation method. To implement them, add the list with images as before but instead of calling it with the parent initialisation create an attribute for the textures. The images can be loaded into the texture list using load\_mirrored\_textures, which loads all images into the created attribute. The load\_mirrored\_textures needs to be imported from DrillDungeonGame/utility.py. The update\_animation method can then be adjusted to change the animations based on the certain conditions for the animation being added.

An Entity can have multiple children including a Turret object used by most enemies and the drill. The Entity class has a children attribute which is a list to store all ChildEntity's.

To add specific functionality to the class the update method can be overridden. When this is done ensure to call the parents update method. In this update specific functions such as checking line of sight, aiming, firing can be added.

The Enemy class is a subset of the Entity class. It adds functionality to the Entity class such as, a health bar displayed under the character, sounds for when they attack or are attacked, and initialised variables to be used for bot implementation such as '\_has\_line\_of\_sight\_with\_drill'.

To create an enemy in the game a subclass of the Enemy class should be made instead of the Entity. The subclass can then also inherit the mix-ins DiggingMixin and PathFindingMixin. The PathFindingMixin is necessary in eneabling them to find a route to the drill and the DiggingMixin enables them to remove dirt blocks in their way. To enable this the update function needs to be overridden to include code that checks if enemy has a line of sight with the drill and also code to follow, aim and fire at the drill.


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

## Adding Shop Items and Tabs

In order to add a new item to the shop menu the DrillDungeonGame/in_game_menus.py file needs to be edited. In this file the ShopMenu class inherits from a InGameMenu class. The InGameMenu class is an arcade.view class which fogs the game screen and displays a grey box for a menu. The InGameMenu class is initialised in the ShopMenu class with dimentions for the shop menu.

To add an item to the shop a ShopItem  object needs to be  added. The ShopItem class needs to be initialised in ShopMenu, in the on\_show method, with the following:

- shop\_menu, which is the shop menu the item would be added to.
- center\_x, which is the x-axis screen location for the item
- item\_name, the name of the item you want to add.
- cost, how much the item would cost
- image, the image used when displaying item
- reusablility, set this to true if item can be bought multiple times
- button\_function, add method to be executed when item bought
- function\_inputs, if method requires input it here otherwise it's set to none.

An item needs to be added to a tab. Currently there are 2 tabs in the game, upgrades and ammo. To add a new tab a ShopTab object needs to be added . The ShopTab class needs to be initialised in ShopMenu, in the on\_show method, with the following:

- tab\_name, name of the tab
- start\_center\_y, the y-axis location to start listing items in tab.

With the tab and item objects defined in the on\_show method, the items then need to be added to the tabs using the tabs add\_item method. After all items have been added to their respective tabs the tab\_list attribute of the ShopMenu class needs to be extended with the tabs created.
