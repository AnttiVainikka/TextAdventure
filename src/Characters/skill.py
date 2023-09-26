class Skill():
    def __init__(self, name :str, multiplier :float, stat :str, uses :int, description :str):
        """
        name: name of the skill
        multiplier: damage of skill = (character_stat + weapon_stat) * multiplier
        stat: which stat is used for damage calculation (atk,magic)
        uses: how many times skill can be used
        description: how the LLM will describe it when asked
        """
        self.name = name
        self.multiplier = multiplier
        self.stat = stat
        self.uses = uses
        self.uses_remaining = uses
        self.description = description
    
    def restore_uses(self):
        self.uses_remaining = self.uses
