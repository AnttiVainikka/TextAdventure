import random
from typing import TYPE_CHECKING
from attr import dataclass
from Characters import character
from Characters.create import create_character

from Generation.generator import llm_create

if TYPE_CHECKING:
    from Generation.scenario import Scenario
    from Generation.faction import Faction


@dataclass
class Character:
    name: str
    role: str
    personality: str
    background: str
    secrets: str

    def game_character(self) -> character.Character:
        return create_character(self.name, f'{self.role} {self.personality} {self.background} {self.secrets}', 'warrior', 1, 1)

def _create_names(scenario: 'Scenario', faction: 'Faction') -> list[str]:
    result = llm_create('npc_names',
                        faction=faction.name,
                        faction_desc=faction.overview,
    )[0]
    return result.names

def _create_roles(scenario: 'Scenario', faction: 'Faction') -> list[str]:
    details = llm_create('npc_roles',
               capital_name=scenario.capital.name,
               kingdom=scenario.kingdom.name,
               ruler=scenario.ruler.name,
               ruler_personality=scenario.ruler.personality,
               ruler_evil=scenario.ruler.evil_deeds,
               governance_style=scenario.ruler.governance_style,
               background_kingdom=scenario.kingdom.description,
               faction=faction.name,
               faction_desc=f'{faction.overview} {faction.beliefs} {faction.goals} The faction is {faction.power}.',
    )[0]
    return details.roles

def _create_npc(name: str, role: str, scenario: 'Scenario', faction: 'Faction') -> Character:
    result = llm_create('npc',
               capital_name=scenario.capital.name,
               kingdom=scenario.kingdom.name,
               ruler=scenario.ruler.name,
               ruler_personality=scenario.ruler.personality,
               ruler_evil=scenario.ruler.evil_deeds,
               governance_style=scenario.ruler.governance_style,
               background_kingdom=scenario.kingdom.description,
               faction=faction.name,
               faction_desc=f'{faction.overview} {faction.beliefs} {faction.goals} The faction is {faction.power}.',
               npc_name=name,
               npc_role=role
    )[0]
    return Character(name, role, result.personality, result.background, result.secrets)

def _take_random(items: list):
    idx = random.randint(0, len(items) - 1)
    return items.pop(idx)

def create_npcs(scenario: 'Scenario', faction: 'Faction', count=3) -> list[Character]:
    if count < 1:
        return []

    names = _create_names(scenario, faction)
    roles = _create_roles(scenario, faction)

    npcs = [_create_npc(_take_random(names), 'leader', scenario, faction)]
    for _ in range(count - 1):
        npcs.append(_create_npc(_take_random(names), _take_random(roles), scenario, faction))
    
    return npcs