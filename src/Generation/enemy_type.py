from dataclasses import dataclass
from enum import Enum
from Generation.generator import llm_create

class Rarity(Enum):
    """
    This enum class represents the rarity levels for enemy types.
    """
    Common = 1,
    Rare = 2,
    Epic = 3,
    Legendary = 4

@dataclass
class EnemyType:
    """
    This class represents enemy types and their characteristics.

    Attributes:
        race (str): The race of the enemy type.
        name (str): The name of the enemy type.
        rarity (Rarity): The rarity level of the enemy type.
    """
    race: str
    name: str
    rarity: Rarity

def generate(race: str) -> dict[Rarity, list[EnemyType]]:
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
    {Common: [EnemyType("Orc", "Orc Warrior", Rarity.Common), ...], ...}

    >>> generate("Human")
    {Rare: [EnemyType("Human", "Human Soldier", Rarity.Rare), ...], ...}
    """
    l = {}
    data = llm_create('enemy_type', race=race)[0].dict()
    for key in data:
        if key in Rarity.__members__:
            ekey = Rarity[key]
            if ekey not in l:
                l[ekey] = []
            for name in data[key]:
                l[ekey].append(EnemyType(race, name, Rarity[key]))
    return l
