from enum import Enum
from Journey.utility import to_dict

class SkillRarity(Enum):
    Common = 1
    Rare = 2
    Epic = 3
    Legendary = 4

class Skill():
    def __init__(self, name :str, multiplier :float, stat :str, uses :int, description :str, ally: bool, aoe: bool):
        """
        name: name of the skill
        multiplier: damage of skill = (character_stat + weapon_stat) * multiplier
        stat: which stat is used for damage calculation (atk,magic)
        uses: how many times skill can be used
        description: how the LLM will describe it when asked
        ally: is the skill cast on allies (True) or enemies (False)
        aoe: does the skill affect all allies/enemies
        """
        self.name = name
        self.multiplier = multiplier
        self.stat = stat
        self.uses = uses
        self.uses_remaining = uses
        self.description = description
        self.ally = ally
        self.aoe = aoe

    def __init_from_dict__(self, state: dict):
        self.name = state["name"]
        self.multiplier = state["multiplier"]
        self.stat = state["stat"]
        self.uses = state["uses"]
        self.uses_remaining = state["uses_remaining"]
        self.description = state["description"]
        self.ally = state["ally"]
        self.aoe = state["aoe"]

    def create_from_dict(state: dict) -> "Skill":
        skill = Skill.__new__(Skill)
        skill.__init_from_dict__(state)
        return skill
    
    def to_dict(self) -> dict:
        return {
            "name": to_dict(self.name),
            "multiplier": to_dict(self.multiplier),
            "stat": to_dict(self.stat),
            "uses": to_dict(self.uses),
            "uses_remaining": to_dict(self.uses_remaining),
            "description": to_dict(self.description),
            "ally": to_dict(self.ally),
            "aoe": to_dict(self.aoe)
        }

    def restore_uses(self):
        self.uses_remaining = self.uses
