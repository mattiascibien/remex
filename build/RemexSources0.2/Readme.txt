Remex
Version 0.2
===============================================================================

Author: Rastagong Librato (rastagong.net)

Licensed under the Expat License (the "MIT license"). Refer to License.txt.

1 About Remex
-------------------------------------------------------------------------------
Remex is a set of tools which facilitate the use of RPG Maker-compatible
autotiles outside RPG Maker, in your own game engine. Remex works with 
the automapping feature from Tiled map editor too (http://mapeditor.org).

It features:

* An autotile expander. It turns the compact autotiles from RPG Maker 
  into readily-usable grids of 48 tiles with all the possible 
  tile configurations.
* A script which generates a Tileset for Tiled using an expanded autotile.
* A script which generates an automapping rule for Tiled using the expanded
  the corresponding tileset. It enables you to use the automapping feature of
  Tiled without having to setup anything.

Note #1: Remex works only with autotiles made for RPG Maker VX and VX Ace.

2 Legal issues
-------------------------------------------------------------------------------
**Please ensure that you have the legal rights to modify the resources you
want to use with the software. The author shall not be held responsible for 
the consequences of your usage of the resources.**

*Pro-tip if you care about law and stuff like that:*

Don't use the autotiles from the RTP shipped with RPG Maker VX/VX Ace.
The End-User License Agreement (EULA) states that they are meant to be used
"only for the purpose **to play the game created and distributed with 
RPG Maker**". It also states that "Licensee shall not reverse engineer, 
de-compile, or **disassemble** the Software. Further, Licensee shall not sell,
assign, lease, sublicense, encumber, or otherwise **transfer the Software
without the written consent of ENTERBRAIN.**"

Use free resources that you have the right to use instead.
You may also buy resources packs from Enterbrain for a non-RM usage.
Refer to http://www.rpgmakerweb.com/product/modern-day-tiles.

3 General instructions
-------------------------------------------------------------------------------
Remex can be used either through the command-line, either through a GUI. The
command-line version features a few more advanced options. It may be useful if
you want to include Remex in your own scripts too.

To use the GUI, launch gui.exe. To use the command-line version, launch 
main.exe in a terminal.

Please refer to the following sections for more detailed instructions:
1. Instructions for the GUI
2. Instructions for the command-line
3. Instructions for the integration usage in Tiled


4 Instructions for the GUI
------------------------------------------------------------------------------
On the main menu, you can choose between the autotile expander, the tileset
generator and the rule maker. 

###Autotile expander
1. Choose an autotile to expand. PNG only, 64 per 96 pixels. It must use 
   the TileA2 format from VX / VX Ace.
2. Expand your tileset with "Expand the tileset!".
3. Save your tileset with "Save as".

###Tileset generator
1. Choose an expanded autotile to make a tileset with. PNG only, 256 per 
   192 pixels. You can expand an autotile from RPG Maker VX / VX Ace with
   this software (Main menu > Expand an autotile).
2. Make your tileset with "Make your tileset!"
3. Save your tileset with "Save as".

###Rule maker
1. Choose a Tileset for Tiled to make an automapping rule with.It must be a 
   .tsx file referring to an expanded autotile. You can make a tileset with 
   Remex (Main menu > Generate a tileset).
2. Choose the map layer which will be considered by Tiled during the 
   automapping. By default, its "Tile Layer 1". You can only choose a layer 
   per rule, so you need to make another rule if you want another layer 
   to be considered too.
3. Make sure that the correct version of Tiled is chosen. Remex can make
   tilesets for both Tiled 0.9 and 0.8.
4. Make an automapping rule by with "Make an automapping rule!". It may take
   a few seconds.
5. Save your rule with "Save as". Please note that the code which is shown
   is not the final code, so you shouldn't copy it. 
Note: The rule maker will an image named "automappingRegions.png" in the
folder in which you saved the rule. Both work together.

5 Instructions for the command-line
------------------------------------------------------------------------------

###General usage
Usage: main.exe [-h] {expand,maketileset,makerule} ...

optional arguments:
  -h, --help            show this help message and exit

Commands:
  The command to execute

  {expand,maketileset,makerule}
    expand              Autotile Expander. Expands an autotile from RPG Maker
                        VX or VX Ace into a grid containing all the possible
                        cases.
    maketileset         Tileset Generator. Generates a tileset for Tiled map
                        editor with an expanded autotile. You can use it
                        directly (but manually) in your maps, or use it with
                        the Rule Maker to make an automatic automapping rule.
    makerule            Rule Maker. Generates an automapping rule for Tiled
                        map editor using a tileset of an expanded autotile. It
                        enables you to map autotiles automatically, without
                        worrying about the precise case to use.

###Expand command
usage: main.exe expand [-h] [-o outputAutotile] [-f] [-v] inputAutotile

positional arguments:
  inputAutotile         The autotile to expand. It must follow a few rules. It
                        must be a PNG image, 64 * 96 wide. It must use RPG
                        Maker VX or VX Ace's TileA2 formatting.

optional arguments:
  -h, --help            show this help message and exit
  -o outputAutotile, --output outputAutotile
                        The output file (the expanded autotile). By default,
                        it is "expandedAutotile.png", located in the directory
                        in which you launch the script. The script will ask
                        you whether it should overwrite the file if it already
                        exists, unless you used the force option.
  -f, --force           Forces the script to be executed without asking you
                        anything. The script will overwrite the output file
                        without warning you if it already exists. Furthermore,
                        it won't ask add an extension to the output file if it
                        lacks.
  -v, --verbose         Starts the program in verbose mode: it prints detailed
                        information on the process.

###Maketileset command
usage: main.exe maketileset [-h] [-o outputTileset] [-f] [-r] [-v]
                           inputExpandedAutotile

positional arguments:
  inputExpandedAutotile
                        The expanded autotile to make a tileset with. It must
                        be a PNG image, 256 * 192 wide. To get this expanded
                        autotile, use the autotile expander featured with
                        Remex (with the command "expand").

optional arguments:
  -h, --help            show this help message and exit
  -o outputTileset, --output outputTileset
                        The output file (the tileset). By default, it is
                        "expandedAutotileTileset.tsx", located in the
                        directory in which you launch the script. The script
                        will ask you whether it should overwrite the file if
                        it already exists, unless you used the force option.
  -f, --force           Forces the script to be executed without asking you
                        anything. The script will overwrite the output file
                        without warning you if it already exists. Furthermore,
                        it won't ask add an extension to the output file if it
                        lacks.
  -r, --relative        In the tileset file, use a relative path to the image
                        itself. Warning: the same relative path will be used
                        in the rulemap if you generate one with this tileset.
                        To avoid any problem regarding paths, you should put
                        your tilesets, maps and images in the same folder.
  -v, --verbose         Starts the program in verbose mode: it prints detailed
                        information on the process.

###Makerule command
usage: main.exe makerule [-h] [-o outputRule] [-l mapLayer]
                        [-r regionsLocation] [-8] [-f] [-v]
                        inputTileset

positional arguments:
  inputTileset          The tileset for Tiled to make an automapping rule
                        with. It must be a tsx file referring to an expanded
                        autotile. To get the expanded autotile, use the
                        autotile expander featured with Remex (with the
                        command "expand"). To get the tileset, use the tileset
                        maker featured with Remex (with the command
                        "maketileset").

optional arguments:
  -h, --help            show this help message and exit
  -o outputRule, --output outputRule
                        The output file (the automapping rule). By default, it
                        is "automappingrule.tmx", located in the directory in
                        which you launch the script. The script will ask you
                        whether it should overwrite the file if it already
                        exists, unless you used the force option.
  -l mapLayer, --layer mapLayer
                        The name of the map layer to consider during the
                        automapping. By default, it is "Tile Layer 1". You can
                        only choose a layer per rule, so you need to make 
                        another rule if you want another layer to be 
                        considered too.
  -r regionsLocation, --regions regionsLocation
                        The rulemap requires an additional image to work
                        properly. By default, the image is always created in
                        the folder of the rulemap. But if you want to, you can
                        set another location.
  -8, --v08             Formats the rulemap for the 0.8 version of Tiled. By
                        default, the rulemaker formats the rule for the 0.9
                        version.
  -f, --force           Forces the script to be executed without asking you
                        anything. The script will overwrite the output file
                        without warning you if it already exists. Furthermore,
                        it won't ask add an extension to the output file if it
                        lacks.
  -v, --verbose         Starts the program in verbose mode: it prints detailed
                        information on the process.

Instructions for the integration in Tiled
------------------------------------------------------------------------------
Using automapping in Tiled is very easy with Remex:
1. Grab an autotile from RPG Maker VX / VX Ace and expand it with Remex.
2. With Remex, make a tileset from this expanded autotile.
3. Still with Remex, make an automapping rule with this tileset.
4. In the same folder, create a file named "rules.txt". Open it and write the
   name of your tileset (for instance "automappingRule.tmx"). Save it and
   close it.
4. In Tiled, create a new map (save it in the same folder as well). 
5. Click on the menu Map > Add an external tileset. Choose the tileset that
   you have created from an expanded autotile.
5. Start mapping! Add any other tileset that you need. When you use the tileset
   created with Remex, you don't have to choose the tile with the correct 
   shape: just design your map with a single tile. For instance, if you've 
   expanded a grass autotile, design the fields without worrying about the
   corners, the borders, etc. You can draw some big green blocks.
6. When you are done and want the autotiles to shape properly, press A (or click
   on Map > AutoMap). 
7. ???
8. Profit!
