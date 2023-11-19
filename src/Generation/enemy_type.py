from dataclasses import dataclass
from enum import Enum
from Generation.generator import llm_create
import random

class EnemyRarity(Enum):
    """
    This enum class represents the rarity levels for enemy types.
    """
    Common = 1
    Rare = 2
    Epic = 3
    Legendary = 4

class EnemyType:
    """
    This class represents enemy types and their characteristics.

    Attributes:
        race (str): The race of the enemy type.
        name (str): The name of the enemy type.
        rarity (EnemyRarity): The rarity level of the enemy type.
    """
    def __init__(self, race: str, name: str, description:str, rarity: EnemyRarity):
        self.race = race
        self.name = name
        self.description = description
        self.rarity = rarity

    def __init_from_dict__(self, state: dict):
        self.race = state["race"]
        self.name = state["name"]
        self.description = state["description"]
        self.rarity = EnemyRarity(state["rarity"])

    def create_from_dict(state: dict) -> "EnemyType":
        if state == None: return None
        enemy_type = EnemyType.__new__(EnemyType)
        enemy_type.__init_from_dict__(state)
        return enemy_type
    
    def to_dict(self) -> dict:
        return {
            "race": self.race,
            "name": self.name,
            "description": self.description,
            "rarity": self.rarity.value
        }

def generate_from_race(race: str) -> dict[EnemyRarity, list[EnemyType]]:
    """
    Generate a dict of enemy types for a given race.

    This function takes a 'race' parameter, which represents the race for which enemy types
    need to be generated. It returns a dict of EnemyType instances that correspond to the
    specified race.

    Parameters:
    - race (str): A string representing the race for which enemy types should be generated.

    Returns:
    - dict: A dict of enemy types where the keys are the rarities and the values are lists of enemy types

    Example:
    >>> generate("Orc")
    {Common: [EnemyType("Orc", "Orc Warrior", EnemyRarity.Common), ...], ...}

    >>> generate("Human")
    {Rare: [EnemyType("Human", "Human Soldier", EnemyRarity.Rare), ...], ...}
    """
    l = {}
    data = llm_create('enemy_type/from_race', race=race)[0].dict()
    for key in data:
        if key in EnemyRarity.__members__:
            ekey = EnemyRarity[key]
            if ekey not in l:
                l[ekey] = []
            for name in data[key]:
                l[ekey].append(EnemyType(race, name, EnemyRarity[key]))
    return l

def generate_from_region(region_name: str,
                         region_description: str,
                         area_name: str,
                         area_description: str,
                         nr: int = 2) -> list[EnemyType]:
    enemy_types = llm_create('enemy_type/from_region/name', region_name=region_name,
                                                            region_description=region_description,
                                                            area_name=area_name,
                                                            area_description=area_description,
                                                            number_of_enemy_types=nr)[0].enemy_types

    descriptions = []
    for enemy_type in enemy_types:
        descriptions.append(llm_create('enemy_type/from_region/description', region_name=region_name,
                                                                             region_description=region_description,
                                                                             area_name=area_name,
                                                                             area_description=area_description,
                                                                             enemy_type=enemy_type)[0].enemy_type_description)
    
    races = []
    for (enemy_type, description) in zip(enemy_types, descriptions):
        races.append(llm_create('enemy_type/from_region/race', enemy_type=enemy_type, description=description)[0].enemy_race)

    return [EnemyType(race, name, description, random.choice([EnemyRarity.Common, EnemyRarity.Rare]))
            for (race, name, description) in zip(races, enemy_types, descriptions)]

def generate_epic_enemy(region_name: str,
                        region_description: str,
                        area_name: str,
                        area_description: str,
                        enemy_type: EnemyType) -> EnemyType:
    data = llm_create('enemy_type/epic', region_name=region_name,
                                         region_description=region_description,
                                         area_name=area_name,
                                         area_description=area_description,
                                         enemy_type=enemy_type.name,
                                         enemy_type_description=enemy_type.description)[0]
    return EnemyType(enemy_type.race, data.unique_name, data.description, EnemyRarity.Epic)

def generate_boss(region_name: str, area_name: str, area_context: str, mission_quest: str) -> EnemyType:
    data = llm_create('enemy_type/boss', region_name=region_name,
                                         area_name=area_name,
                                         area_context=area_context,
                                         mission_quest=mission_quest)[0]
    return EnemyType(data.boss_race, data.boss_name, data.boss_description, EnemyRarity.Legendary)
