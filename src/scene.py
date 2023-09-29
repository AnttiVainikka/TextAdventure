# I think each scene should have a reward for the player. Currently the ways the player
# can become stronger are getting exp, finding/looting a new piece of equipment,
# learning some new skill, receiving bonuses to stats (hp,atk,magic) or having
# their hp and/or skill uses restored. New ways can be created but for the time being
# I think we could let the LLM choose one of these rewards for the player as well as
# some challenge for the player to overcome and let that be the foundation for each scene.

# Thoughs from Antti, be free to comment below or in discord

# As an alternative to restoring hp and skill uses as a reward, maybe they could be restored 
# via resting. This could work by having a resting place spawn some way through 
# the dungeon and having e.g. a long or short rest. This would maybe require some resources
# like food and drink to be consumed upon rest but may prove complicated, could be 
# implemented later. This is the "traditional" D&D way of handling it but we don't have to follow
# pre-set rules to a tee.

# Thoughts from Matti

type = "battle"

# Different types can be added, some possible ones are:
# Combat/battle encounter
# Social encounter
# Riddle enconter
# Trap encounter
# Boss encounter

# Potential additional encounters:
# Treasure encounter
# A resting encounter
# A merchant encounter might be useful though cumbersome to implement

size_x = 10
size_y = 10
scene_grid = [[0]*size_x]*size_y

# A scene can be represented via a grid where typically one square 
# represents a 5ft. square

entrance_x = 0
entrance_y = 0
scene_entrance = (entrance_x,entrance_y)
exit_x = 0
exit_y = 0
scene_exit = (exit_x,exit_y)

# All rooms have an entrance where the party spawns
# All rooms apart from the boss room have at least one exit or possibly multiple exits