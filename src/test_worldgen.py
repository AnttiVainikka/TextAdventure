import sys
from Generation.faction import create_factions
from Generation.generator import llm_create
from Generation.npc import create_npcs
from Generation.scenario import new_scenarios
from world import GameWorld, save_world


print('Generating scenarios...')
scenarios = new_scenarios(3)

print('Choose a scenario:')
for idx, scenario in enumerate(scenarios):
    print(f'{idx}. {scenario.capital.name}, Kingdom of {scenario.kingdom.name}')
    print(f'Ruled by: {scenario.ruler.title} {scenario.ruler.name}')
    print(scenario.kingdom.description, '\n')
    print(scenario.ruler.governance_style, scenario.ruler.evil_deeds)
    for region in scenario.kingdom.regions:
        print(f'Region {region.name}')
        print(region.description)

selected = int(input('Choose the scenario: '))
scenario = scenarios[selected]

print('Generating factions...')
factions = create_factions(scenario)

print('Saving the world...')
world = GameWorld(scenario, factions)
save_world(sys.argv[1], world)
