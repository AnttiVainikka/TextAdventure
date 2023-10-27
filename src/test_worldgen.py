from Generation.faction import create_factions
from Generation.scenario import new_scenarios


scenario = new_scenarios(1)[0]
print(scenario)
print(create_factions(scenario))