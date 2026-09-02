myself (rockymine) and Ruediger_LP spent 5 hours to complete Millrace.

the map authored by the agent provided a great basis. the terrain, spawn platform, spawn house, objetives, canal walls, water levels, bridges, boulders, and most house placements were kept intact. this should allow you to diff the map to learn what changed and what can be done better in the next pass of the map.

we first removed the trees, reshaped the houses on the spawn platform by moving them further back, and separated the individual design elements of the map to re-style them. we masked all surface blocks to add an actual dirt layer beneath, masked the boulders and added new ones to apply a more lively and vibrant style to them. 

i took my time to meticuosly copy the different world edit and arceon (plugin by arcaniax) commands used to do all the theming. essentially all that was done is theming and some dressing. the redesign of the houses and their interior as well as adding a different ship, statue and observer spawn play a big part too. but most comes simply down to better theming and using the custom trees.

canal wall pattern: 
//replace #cell[4][43:8,43,35:8]

added dirt below dirt and grass: 
//replace #below[2,3][3] #frac[4][3,3:1,5:1]

complicated pattern for the stone layer of the terrain. nested patterns and used placeholder blocks. "hand" just stands for one of the wool blocks. i used 159:9 for the white wool iirc.

//r 1,48,4,168,129,98 22
//r 22 #vor[7][35,22]
//r 22 #vor[7][35,22]
//r 35:0 #vor[7][35,22]
//r 22 #vor[5][35:1,35:2]
//r 35:1 #vor[5][35:1,35:2]
//r 35:2 #vor[5][35:1,35:2]
//r 35:1 #turb[5][35:1,35:3]
//gmask 35:3
//replace ~35:1 35:4
//replace ~35:4 35:4
//r 35:1 #turb[5][35:1,35:5]
//gmask
//r 35:1 #turb[5][35:1,35:5]
//r hand 129
//r hand 159:9
//r hand 48
//r hand 1
//r hand 1:5
//r hand 1:6

added numerous new boulders into the river bed: 
//brush boulder 22 7,9 4 5,7 5,7 -a
//replace 22 #frac[3][4,48,129,168]

themed the riverbed: 
//replace 3 #frac[4][3,3:1,5:1,13,1:5]

added paths:
//brush boulder 41 3,4 3 3,4 3,4
//gmask 41&#below[air][1]
//replace #cell[2][70%41,30%[#frac[4][3,3:1,41]]] (added some dirt specs)
//replace #frac[4][1:1,1:2,5:3]

themed the dirt surface:
//gmask 3&#below[air][1]
//replace #frac[4][3,3:1,3:2]
//replace #frac[4][3,3:1,3:2,3,3:1,3:2,2] (second pass to add some grass specs)

themed the grass surface:
//gmask 2&#below[air][1]
//replace #frac[4][2,2,2,3,3:1,3:2]

added fauna above grass:
//gmask 0&#above[2][1]
//s #frac[4][0,31:1,31:2,175:3]

biome pattern: 
//replace #vor[8][[#biome[4],#biome[21]],[#cell[3][#biome[16],#biome[4],#biome[27]]]]

replaced the generator trees by 9 oak and 9 pine trees of my own collection (from inside pgm-studio-mapgen/showcase/tree-showcase)

took the balloon from Slipway as observer spawn. the observer spawn was placed inside of the balloons cage. some symmetry issues on that balloon were fixed and the cage was designed a little more. flower pots and player heads were added. player heads with player data. the whole platform was raised to y70.

added decorative beacons above the destroyables

moved and resized the houses on the spawn platform. the roofs were detailed with some stair blocks to give them a rugged look. chimneys were added made of cobble walls, stone slabs and cobwebs. interior was decorated with numerous blocks (not so important, not the aim of the tool). some wooden boxes were placed on the platform. a wall was added around the platform.

the bridge was made more walkable and smooth by adding slabs at elevation changes. the path also received some slabs.

diorite statue was removed and took room for more trees. the small island instead received the statue sculpture from the opus5-automaton map. the statue is now holding a diamond instead of the abstract iron block shape. the cape and footing use different blocks. for the footing instead of sandstone stone, smooth andesite and double stone steps are used. the statues are team colored in red and blue clay and wool. some blocks were replaced with light gray andd gray wool as well. one house was replaced by that statue.

 the bottom of the world had some holes in it because of the walls that were placed around one of the destroyables and the canal. likely a bug in the script were the walls didnt go all the way through to the bottom of the world. same issue was with the ramp that went into the canal.

speaking of the walls. the wall around the destroyable was broken up a little bit to make it look worn. some broken pieces of wall were added around it.

the destroyables received a sort of "dress". some wool blocks placed around. not part of the destroyable itself, just decoration. pretty old-school style element actually. very old maps used these.

the ship was replaced by a custom more modern ship. it resembles a "Schlepper" that pulls heavy ships.

the enchantments on the diamond pickaxe were removed from the spawnkit.