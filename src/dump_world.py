import sys

from world import load_world

world = load_world(sys.argv[1])

print('#', world.scenario.kingdom.name)
print(world.scenario.kingdom.description, '\n')
print('##', world.scenario.ruler.title, world.scenario.ruler.name)
print(world.scenario.ruler.backstory, '\n')
print(world.scenario.ruler.deeds, world.scenario.ruler.personality, '\n')
print(world.scenario.ruler.governance_style, world.scenario.ruler.evil_deeds, '\n')

print('##', world.scenario.capital.name)
print(world.scenario.capital.architecture, '\n')
print(world.scenario.capital.history)

print('## Regions')
for region in world.scenario.kingdom.regions:
    print('###', region.name)
    print('####', region.description)

print('## Factions')
for faction in world.factions:
    print('###', faction.name, f'- "{faction.motto}"')
    print(faction.overview, faction.beliefs, faction.goals, '\n')
    print('Members:')
    for npc in faction.npcs:
        print('*', f'**{npc.role} {npc.name}**:', npc.background, npc.personality, npc.secrets)
    print()