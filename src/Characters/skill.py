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
    def restore_uses(self):
        self.uses_remaining = self.uses
