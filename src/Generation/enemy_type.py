from enum import Enum
from Generation.generator import Generator

class Rarity(Enum):
    """
    This enum class represents the rarity levels for enemy types.
    """
    Common = 1,
    Rare = 2,
    Epic = 3,
    Legendary = 4

class EnemyType:
    """
    This class represents enemy types and their characteristics.

    Attributes:
        race (str): The race of the enemy type.
        name (str): The name of the enemy type.
        rarity (Rarity): The rarity level of the enemy type.
    """
    def __init__(self, race: str, name: str, rarity: Rarity):
        self.race = race
        self.name = name
        self.rarity = rarity
        #self.description: str # TODO: do we need a description?

def generate(race: str) -> list[EnemyType]:
    """
    Generate a list of enemy types for a given race.

    This function takes a 'race' parameter, which represents the race for which enemy types
    need to be generated. It returns a list of EnemyType instances that correspond to the
    specified race.

    Parameters:
    - race (str): A string representing the race for which enemy types should be generated.

    Returns:
    - list: A list of EnemyType instances for the specified race.

    Example:
    >>> generate("Orc")
    [EnemyType("Orc", "Orc Warrior", Rarity.Common), ...]

    >>> generate("Human")
    [EnemyType("Human", "Human Soldier", Rarity.Rare), ...]
    """
    l = []
    generator = Generator("enemy_type")
    successful, data = generator.generate(race=race)
    for key in data:
        if key in Rarity.__members__:
            for name in data[key]:
                l.append(EnemyType(race, name, Rarity[key]))
    return l
