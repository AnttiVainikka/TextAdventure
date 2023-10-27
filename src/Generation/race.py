from enum import Enum
from Generation.generator import llm_create

class Hostility(Enum):
    """
    This enum class represents the hostility levels for races.
    """
    Friendly = 1,
    Neutral = 2,
    Aggressive = 3

class Race:
    """
    This class represents races in the game.

    Attributes:
        name (str): The name of the race.
        name (str): The name of the enemy type.
        hostility (Hostility): The hostility of the race towards the player.
    """
    def __init__(self, name: str, hostility: Hostility):
        self.name = name
        self.hostility = hostility
        #self.description: str # TODO: do we need a description?

def generate() -> dict[Hostility, list[Race]]:
    """
    Generate a dict of races in the game.

    Returns:
    - dict: A dict of races where the keys are the hostilities and the values are lists of races

    Example:
    >>> generate()
    {Friendly: [Race("Human", Hostility.Friendly), ...], Neutral: [Race("Minotaur", Hostility.Neutral), ...], ... }
    """
    l = {}
    data = llm_create('race')[0].model_dump()
    for key in data:
        if key in Hostility.__members__:
            ekey = Hostility[key]
            if ekey not in l:
                l[ekey] = []
            for name in data[key]:
                l[ekey].append(Race(name, ekey))
    return l