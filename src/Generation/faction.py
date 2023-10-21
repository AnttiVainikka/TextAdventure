from dataclasses import dataclass
from enum import Enum
from Generation.generator import llm_create
from Generation.scenario import Scenario

class InitialStance(Enum):
    FRIENDLY = 'friendly towards the rebellion (our hero will just need to ask)'
    NEUTRAL = 'neutral in regard to the conflict (until persuaded otherwise)'
    SUSPICIOUS = 'dislike the idea of rebellion (though perhaps they could be persuaded)'
    HOSTILE = 'openly support the ruler (good luck convincing them otherwise)'

@dataclass
class Faction:
    name: str
    overview: str
    motto: str
    beliefs: str
    goals: str
    needs: str


def _create_faction(scenario: Scenario, power: int, stance: InitialStance, alignment: str, count=1):
    if power < 10:
        power_level = 'insignificant in grand scale'
    elif power < 25:
        power_level = 'a small but not insignificant power'
    elif power < 50:
        power_level = 'a significant power within the capital'
    elif power < 100:
        power_level = 'one of the most important powers in kingdom'

    results = llm_create('faction', count,
               capital_name=scenario.capital.name,
               kingdom=scenario.kingdom.name,
               tyrant=scenario.ruler.name,
               ruler_personality=scenario.ruler.personality,
               ruler_evil=scenario.ruler.evil_deeds,
               governance_style=scenario.ruler.governance_style,
               background_kingdom=scenario.kingdom.description,
               background_capital=f'{scenario.capital.history} {scenario.capital.architecture} {scenario.capital.population}',
               power_level=power_level,
               rebellion_stance=stance.value,
               alignment=alignment
               )
    return [Faction(name=result.name, overview=result.overview, motto=result.motto, beliefs=result.beliefs, goals=result.goals,
                    needs=result.needs) for result in results]


def create_factions(scenario: Scenario) -> list[Faction]:
    factions = []

    # Create a few friendly, but not very powerful factions
    factions.append(_create_faction(scenario, 5, InitialStance.FRIENDLY, 'chaotic good'))
    factions.append(_create_faction(scenario, 8, InitialStance.FRIENDLY, 'neutral good'))
    factions.append(_create_faction(scenario, 20, InitialStance.FRIENDLY, 'chaotic evil'))

    # Create neutral factions, some weak, some strong
    factions.append(_create_faction(scenario, 15, InitialStance.NEUTRAL, 'lawful good'))
    factions.append(_create_faction(scenario, 20, InitialStance.NEUTRAL, 'true neutral'))
    factions.append(_create_faction(scenario, 30, InitialStance.NEUTRAL, 'lawful neutral'))
    factions.append(_create_faction(scenario, 35, InitialStance.NEUTRAL, 'lawful evil'))

    # TODO rest of the factions

    return factions