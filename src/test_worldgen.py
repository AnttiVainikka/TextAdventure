from Generation.faction import create_factions
from Generation.npc import create_npcs
from Generation.scenario import new_scenarios


scenario = new_scenarios(1)[0]
print(create_factions(scenario))
