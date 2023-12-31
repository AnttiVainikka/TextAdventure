from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import functools
from multiprocessing.pool import ThreadPool
from Generation.generator import llm_create
from Generation.npc import Character, create_npcs
from Generation.scenario import Scenario
from Journey.utility import to_dict

class InitialStance(Enum):
    FRIENDLY = 'friendly towards the rebellion (our hero will just need to ask)'
    NEUTRAL = 'neutral in regard to the conflict (until persuaded otherwise)'
    SUSPICIOUS = 'dislike the idea of rebellion (though perhaps they could be persuaded)'
    HOSTILE = 'openly support the ruler (good luck convincing them otherwise)'

class Alignment(Enum):
    CHAOTIC_GOOD = 'chaotic good; their motivations are altruistic, but they have done horrible things'
    NEUTRAL_GOOD = 'neutral good; they try to look for others'
    LAWFUL_GOOD = 'lawful good; they want to help, but would prefer not to break the law'
    CHAOTIC_NEUTRAL = 'chaotic neutral; they do whatever needs to be done'
    NEUTRAL = 'true neutral'
    LAWFUL_NEUTRAL = 'lawful neutral; they are unlikely to break law, for any reason'
    CHAOTIC_EVIL = 'chaotic evil; they do whatever they want to, damn the consequences'
    NEUTRAL_EVIL = 'neutral evil; they do whatever needs to be done to meet their selfish goals'
    LAWFUL_EVIL = 'lawful evil; they try to advance their selfish goals legally'

@dataclass
class Faction:
    name: str
    overview: str
    motto: str
    beliefs: str
    goals: str
    needs: str
    alignment: Alignment
    power: str
    power_value: int
    npcs: list[Character]
    favor: int

    @property
    def __dict__(self): # Had to override this because of the enum
        return to_dict(self)

def from_dict(state: dict) -> Faction:
    return _from_dict(state, Faction)

def _from_dict(state, type):
    if getattr(type, "__origin__", None) == list:
        inner_type = getattr(type, "__args__", [])[0]
        return [_from_dict(inner_state, inner_type) for inner_state in state]
    if issubclass(type, Enum): return type(state)
    if not is_dataclass(type): return state
    real_state = {}
    for key, value in state.items():
        field_type = next(field for field in fields(type) if field.name == key).type
        real_state[key] = _from_dict(value, field_type)
    return type(**real_state)

def _create_faction(scenario: Scenario, power: int, stance: InitialStance, alignment: Alignment, count=1):
    if power < 10:
        power_level = 'insignificant in grand scale'
    elif power < 25:
        power_level = 'a small but not insignificant power'
    elif power < 50:
        power_level = 'a significant power within the capital'
    elif power < 100:
        power_level = 'one of the most important powers in kingdom'
    else:
        power_level = 'the most significant military power in the kingdom'

    match stance:
        case InitialStance.FRIENDLY:
            favor = 35
        case InitialStance.NEUTRAL:
            favor = 0
        case InitialStance.SUSPICIOUS:
            favor = -25
        case InitialStance.HOSTILE:
            favor = -50

    results = llm_create('faction', count,
               capital_name=scenario.capital.name,
               kingdom=scenario.kingdom.name,
               ruler=scenario.ruler.name,
               ruler_personality=scenario.ruler.personality,
               ruler_evil=scenario.ruler.evil_deeds,
               governance_style=scenario.ruler.governance_style,
               background_kingdom=scenario.kingdom.description,
               background_capital=f'{scenario.capital.history} {scenario.capital.architecture} {scenario.capital.population}',
               power_level=power_level,
               rebellion_stance=stance.value,
               alignment=alignment.value
               )
    factions = []
    for result in results:
        npcs = []
        faction = Faction(name=result.name, overview=result.overview, motto=result.motto,
                                beliefs=result.beliefs, goals=result.goals, needs=result.needs,
                                alignment=alignment, power=power_level, power_value=power, npcs=npcs, favor=favor)
        factions.append(faction)
        npcs.extend(create_npcs(scenario, faction))
    return factions


def create_factions(scenario: Scenario) -> list[Faction]:
    templates = [
        # Create a few friendly, but not very powerful factions
        (5, InitialStance.FRIENDLY, Alignment.CHAOTIC_GOOD),
        (20, InitialStance.FRIENDLY, Alignment.CHAOTIC_EVIL),
        # Create the neutral factions
        (15, InitialStance.NEUTRAL, Alignment.LAWFUL_GOOD),
        (20, InitialStance.NEUTRAL, Alignment.CHAOTIC_NEUTRAL),
        (25, InitialStance.NEUTRAL, Alignment.NEUTRAL_EVIL),
        # And some potential enemies
        (30, InitialStance.SUSPICIOUS, Alignment.LAWFUL_NEUTRAL),
        (40, InitialStance.SUSPICIOUS, Alignment.NEUTRAL),
        # And very likely enemies
        (70, InitialStance.HOSTILE, Alignment.NEUTRAL_EVIL),
        (125, InitialStance.HOSTILE, Alignment.LAWFUL_EVIL)
    ]

    create_func = functools.partial(_create_faction, scenario)

    factions = []
    with ThreadPool() as pool:
        for faction_list in pool.starmap(create_func, templates):
            factions.extend(faction_list)

    return factions